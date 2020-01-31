#知乎问题
import re
import requests
# 知乎有反爬虫，加入http headers伪装浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"
}
# 知乎问题id
question_id = 281185483
interval = 20
offset = 0
rank = 100
#dict() 函数用于创建一个字典。
novels_count = dict()
# r"" 的作用是去除转义字符.
p = re.compile(r'《.+?》')# 正则匹配被《》括起来的书名
while True:
    print(f'答案数{offset} 到 {offset + interval}')
# 知乎获取回答分页API
    url = f'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=content&limit={interval}&offset={offset}&sort_by=default'
    html = requests.get(url, headers = headers)
    answers = html.json()['data']
    if len(answers) == 0:
        break
    for answer in answers:
        results = set(re.findall(p, answer['content']))
        for novels_name in results:
            if novels_name in novels_count:
                novels_count[novels_name] += 1
            else:
                novels_count[novels_name] = 1
    offset += interval
#把结果按提名次数从高到低排序
novels_rank_list = sorted(novels_count.items(), key=lambda x: x[1], reverse=True)
print(f'提名电影总数:{len(novels_rank_list)}')

# 打印前50
for i, novel in enumerate(novels_rank_list):
    if i > rank - 1:
        break
    name = novel[0]
    num = novel[1]
    print(f'{i + 1}.{name}提名{num}次')
