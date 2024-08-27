import requests
from requests import session

# cookies = {"sessioncookie": "123456789"}
# r = requests.get(
#     "http://httpbin.org/cookies/set?sessioncookie=123456789", cookies=cookies
# )
# print(r.text)
# # print(r.json())
# r = requests.get("http://httpbin.org/cookies")
# print(r.text)

s1 = requests.Session()
r = s1.get("http://httpbin.org/cookies/set?sessioncookie=123456789")
print(r.text)
r = s1.get("http://httpbin.org/cookies")
print(r.text)

s2 = requests.Session()
r = s2.get("http://httpbin.org/cookies", cookies={"sessioncookie": "123456789"})
print(r.text)
r = s2.get("http://httpbin.org/cookies")
print(r.text)
