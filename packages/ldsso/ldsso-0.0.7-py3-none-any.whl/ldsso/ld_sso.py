import os
from urllib.parse import quote, unquote, urljoin

import requests
from flask import Request, Response, abort, make_response
from requests.sessions import HTTPAdapter


class SSO:
    LD_SSO_SERVICE_API = os.environ.get("LD_SSO_SERVICE_API")
    LD_KEYCLOAK_CLIENT_ID = os.environ.get("LD_KEYCLOAK_CLIENT_ID")
    LD_NAMESPACE = os.environ.get("LD_NAMESPACE")
    LD_HOSTNAME = os.environ.get("HOSTNAME", "")
    URI_USERINFO = "userinfo"
    URI_JUDGE = "judge"
    URI_POLICY = "policies"

    def __init__(
        self, token, host=None, api_prefix="/api/access-policy/", max_retries=3
    ):
        assert token, "token must be provided"
        if not host:
            host = self.LD_SSO_SERVICE_API
        assert host, f"environment variable $LD_SSO_SERVICE_API not set"
        self.sso_url = urljoin(host, api_prefix)
        if not self.sso_url.endswith("/"):
            self.sso_url = self.sso_url + "/"
        self.r = requests.Session()
        self.r.mount("http://", HTTPAdapter(max_retries=max_retries))
        self.r.mount("https://", HTTPAdapter(max_retries=max_retries))
        self.r.headers = {
            "Content-Type": "application/vnd.api+json",
            "Authorization": token,
        }
        self.userinfo = self.get_userinfo(token)

    def __handle_response(self, response: Response, success_code=200):
        status_code = response.status_code
        if status_code != success_code:
            try:
                error_message = response.json()["error_message"]
            except:
                error_message = response.text
            abort(status_code, error_message)

    def get_userinfo(self, token=None):
        """获取用户信息"""
        url = urljoin(self.sso_url, self.URI_USERINFO)
        headers = self.r.headers
        if token:
            headers = {**headers, "Authorization": token}
        response = self.r.get(url, headers=headers)
        self.__handle_response(response)
        return response.json()

    def judge_api(self, ld_project, api_url, method):
        """检测用户是否允许请求服务"""
        url = urljoin(self.sso_url, self.URI_JUDGE)
        headers = {**self.r.headers, "Ld-Project": quote(ld_project)}
        params = {"url": api_url, "method": method}
        response = self.r.get(url, params=params, headers=headers)
        self.__handle_response(response)
        res = response.json()
        return res["effect"] == "allow", res

    def judge_resource(self, action, resource):
        """检测用户是否允许请求数据"""
        url = urljoin(self.sso_url, self.URI_JUDGE)
        data = [{"action": action, "resource": resource}]
        response = self.r.post(url, json=data)
        self.__handle_response(response)
        res = response.json()
        return res["effect"] == "allow", res

    def create_policy(
        self,
        name: str,
        statements: list[dict[str, str]],
        description: str = None,
        version: str = None,
    ):
        """
        创建policy声明
        statements: [
            {
                "sid": "xxxxx",
                "effect": "Allow",
                "action": ["x"],
                "resource": ["x"],
            }
        ]
        """

        url = urljoin(self.sso_url, self.URI_POLICY)
        if description is None:
            description = name
        if version is None:
            version = "v1"
        assert statements, '"statements" must be provided'
        data = {
            "name": name,
            "description": description,
            "statements": {"Version": version, "Statement": statements},
        }
        response = self.r.post(url, json=data)
        self.__handle_response(response)
        return response.json()

    @classmethod
    def decorator_judge_api(
        cls,
        client_name: str = None,
        api_url: str = None,
        **sso_kwargs,
    ):
        """装饰器, 检测用户是否允许请求当前接口.
            - 从被装饰函数的Request参数中解析method.
            - 从环境变量LD_NAMESPACE中提取ld_project.

        Args:
            client_name (str, optional): 默认从环境变量LD_KEYCLOAK_CLIENT_ID中提取client_name.

            api_url (str, optional): 应与action的apis中一致. 默认从pod的hostname中解析, 本地调试请手动传入该参数.

        Returns:
            装饰后,Request参数会追加ld_account,ld_roles,ld_userinfo属性
        """
        if not api_url:
            if cls.LD_HOSTNAME.startswith("func-"):
                api_url = f'/api/{"_".join(cls.LD_HOSTNAME.split("-")[:-2])}'
        assert api_url, '"api_url" is required'
        ld_namespace = cls.LD_NAMESPACE
        assert ld_namespace, "ENV $LD_NAMESPACE is required"

        func = None
        if client_name and callable(client_name):
            func = client_name
            client_name = None
        if not client_name:
            client_name = cls.LD_KEYCLOAK_CLIENT_ID
        assert client_name, f"ENV $LD_KEYCLOAK_CLIENT_ID is required"

        def decorator(func):
            def wrapper(*args, **kwargs):
                req = None
                for req in (*args, *kwargs.values()):
                    if isinstance(req, Request):
                        break
                    if getattr(req, "request", None) and isinstance(
                        req.request, Request
                    ):
                        req = req.request
                        break
                method = getattr(req, "method", None)
                assert method, "decorated function must have a Request argument"
                token = req.headers.get("Authorization")
                assert token, "Authorization is required"
                sso = cls(token=token, **sso_kwargs)
                api_allowed, res = sso.judge_api(unquote(ld_namespace), api_url, method)
                assert api_allowed, f"Deny. Sid: {res['sid']}"
                account = sso.userinfo["preferred_username"]
                all_roles = (
                    sso.userinfo["resource_access"]
                    .get(client_name, {})
                    .get("roles", [])
                )
                setattr(req, "ld_account", account)
                setattr(req, "ld_roles", all_roles)
                setattr(req, "ld_userinfo", sso.userinfo)
                return func(*args, **kwargs)

            return wrapper

        if func and callable(func):
            return decorator(func)

        return decorator

    @classmethod
    def decorator_cors(cls, func):
        """装饰器. 修改view返回的Response的headers, 允许所有跨域请求"""

        def wrapper(*args, **kwargs):
            req = None
            for req in (*args, *kwargs.values()):
                if isinstance(req, Request):
                    break
                if getattr(req, "request", None) and isinstance(req.request, Request):
                    req = req.request
                    break
            assert req, "Decorated function must have a Request argument"
            response_headers = {
                "Access-Control-Allow-Origin": req.headers.get("Origin") or "*",
                "Access-Control-Allow-Headers": "Ld-Client,Ld-Project,Content-Type,Content-Length,User-Agent,Authorization,Accept,X-Requested-With",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
                "Access-Control-Allow-Credentials": "true",
            }
            view_res = func(*args, **kwargs)
            resp = make_response(view_res)
            for h, v in response_headers.items():
                resp.headers[h] = v
            return resp

        return wrapper


if __name__ == "__main__":
    token = "Bearer eyJhbO5jIn0.eyJleHAiOjExNjk4MjAwzMtOTM2Ni05qCH5rOo566h55CG5bmz5Y.PmbMgnZk6uefT7qK"
    sso = SSO(token, host="http://sso.127.0.0.1.nip.io")
    print(sso.userinfo)
    print(sso.judge_api("任务管理统计", "/api/func_list_task", "GET"))
    print(
        sso.judge_resource(
            "DeleteDatasets", "lrn:service:dms:project:base:dataset:LD93d9fa06"
        )
    )
    # print(
    #     sso.create_policy(
    #         name="aaaa",
    #         statements=[
    #             {
    #                 "sid": "aaaa",
    #                 "effect": "Deny",
    #                 "action": ["custom:DeleteDatasets"],
    #                 "resource": ["*"],
    #             }
    #         ],
    #     )
    # )
