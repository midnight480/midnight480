import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import re

posts = []

# midnight480のフィード取得と解析
response = requests.get('https://midnight480.com/feed')
root = ET.fromstring(response.content)

for item in root.findall('.//item'):
    posts.append({
        'title': item.find('title').text,
        'date': datetime.strptime(item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S'),
        'url': item.find('link').text
    })

# 日付でソート
posts.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)

# 最新10件を取得してマークダウン形式に変換
dist_md = ''
for post in posts[:10]:
    dist_md += f"- [{post['title']}]({post['url']})\n"

# README.mdの更新
with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(
    r'<!--\[START POSTS\]-->.*<!--\[END POSTS\]-->', 
    f"<!--[START POSTS]-->\n{dist_md}<!--[END POSTS]-->",
    content,
    flags=re.DOTALL
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_content)