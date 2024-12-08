import xml.etree.ElementTree as ET
import requests
from datetime import datetime, timezone
import re

posts = []

# midnight480のフィード取得と解析
response = requests.get('https://midnight480.com/feed')
root = ET.fromstring(response.content)

for item in root.findall('.//item'):
    try:
        # 日付文字列を取得してパース
        pub_date = item.find('pubDate').text
        date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S GMT')
        # UTCタイムゾーンを設定
        date_obj = date_obj.replace(tzinfo=timezone.utc)
        
        posts.append({
            'title': item.find('title').text,
            'date': date_obj.strftime('%Y-%m-%d %H:%M:%S'),
            'url': item.find('link').text
        })
    except (ValueError, AttributeError) as e:
        print(f"Error processing item: {e}")
        print(f"Problematic date string: {item.find('pubDate').text}")
        continue

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