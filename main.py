import json
import requests

url = 'https://ts20.x2.america.travian.com'

payload = {'name': 'atpstealer', 'password': '123qweasd'}

auth_res = requests.post(url + "/api/v1/auth/login", data=payload)
code_str = auth_res.content.decode("UTF-8")
code = json.loads(code_str)['code']

auth_res = requests.get(url + "/api/v1/auth?response_type=redirect&code=" + code)

response_with_cookie = requests.get(url + "/dorf2.php", cookies=auth_res.cookies)


pass
