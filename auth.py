import json
import requests


class Request:
    def __init__(self):
        self.url = 'https://ts20.x2.america.travian.com'
        self.payload = {'name': 'atpstealer', 'password': '123qweasd'}
        self.cookie = self.auth()

    def auth(self):
        auth_res = requests.post(self.url + "/api/v1/auth/login", data=self.payload)
        code_str = auth_res.content.decode("UTF-8")
        code = json.loads(code_str)['code']
        auth_res = requests.get(self.url + "/api/v1/auth?response_type=redirect&code=" + code)
        response_with_cookie = requests.get(self.url + "/dorf2.php", cookies=auth_res.cookies)
        return response_with_cookie.cookies

    def request(self, location):
        return requests.get(self.url + location, cookies=self.cookie)


