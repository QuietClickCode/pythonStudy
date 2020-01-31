import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
}
#user_id = 'andy_pan'
user_id = 'zhu-jian-jun-54-95'
zhihu_api = f'https://www.zhihu.com/api/v4/members/{user_id}?include=follower_count,voteup_count,favorited_count,thanked_count'
html = requests.get(zhihu_api, headers=headers)
user = html.json()
print(user)

