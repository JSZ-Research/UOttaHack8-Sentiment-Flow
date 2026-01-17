import requests

# 填入参数
TOKEN = "VoT9W4PuK0AzA.xUGQSK2qNvPU8VgIGnaC-LOKkqPy3ID5lD8K6Aos8hVWUdQtYCXNo9Yc1UUJYy.7f.7AFYbYQSEz7nO7uF8sOpjc12cqbttxGvK-hacBdlN8DMVTv4"
SURVEY_ID = "421216831"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 2. 获取问卷详情（包含所有问题信息）
url = f"https://api.surveymonkey.com/v3/surveys/{SURVEY_ID}/details"

try:
    response = requests.get(url, headers=headers).json()
    # 遍历所有页面的所有问题
    for page in response['pages']:
        for question in page['questions']:
            q_id = question['id']
            q_heading = question['headings'][0]['heading']
            print(f"✅ 找到问题: '{q_heading}'")
            print(f"👉 它的 Question ID 是: {q_id}\n")
except Exception as e:
    print(f"❌ 获取失败: {e}")