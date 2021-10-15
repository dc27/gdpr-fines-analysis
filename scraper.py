import requests
from bs4 import BeautifulSoup
import re
import json

base = 'https://www.privacyaffairs.com/'
route = 'gdpr-fines/'
url =  base + route

with open('data/user_agent.json') as json_file:
    headers = json.load(json_file)['headers']

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, features='html.parser')

all_scripts = soup.find_all('script')

info_script = all_scripts[6]

find = re.finditer(r'\[', info_script.text)

starts = [m.start() for m in re.finditer(r'\[', info_script.text)]
ends = [m.end() for m in re.finditer(r'\]', info_script.text)]

formatted_info = []

if len(starts) <= len(ends):
    for i in range(len(starts)):
        formatted_info.append(json.loads(info_script.text[starts[i]:ends[i]]))
else:
    for i in range(len(ends)):
        formatted_info.append(json.loads(info_script.text[starts[i]:ends[i]]))

# pattern to extract everything in between html tags:
pat = r'(?<=\>)(.+?)(?=\<)'

for i in range(len(formatted_info)):
    for j in range(len(formatted_info[i])):
        s = formatted_info[i][j]['summary']
        match = re.search(pat, s)
        formatted_info[i][j]['summary'] = match.group(1)

data = {
    'allItems':formatted_info[0],
    'allItemsPriceGrouped':formatted_info[1]
}

with open('data/scraped_fines.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)