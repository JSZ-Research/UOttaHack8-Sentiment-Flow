import requests

TOKEN = "VoT9W4PuK0AzA.xUGQSK2qNvPU8VgIGnaC-LOKkqPy3ID5lD8K6Aos8hVWUdQtYCXNo9Yc1UUJYy.7f.7AFYbYQSEz7nO7uF8sOpjc12cqbttxGvK-hacBdlN8DMVTv4"
SURVEY_ID = "421216831"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.surveymonkey.com/v3/surveys/{SURVEY_ID}/details"

try:
    response = requests.get(url, headers=headers).json()
    for page in response['pages']:
        print(f"📄 找到页面！Page ID 是: {page['id']}") # <--- 重点看这个
        for question in page['questions']:
            print(f"  ❓ 问题: {question['headings'][0]['heading']}")
            print(f"  👉 Question ID 是: {question['id']}\n")
except Exception as e:
    print(f"❌ 失败: {e}")