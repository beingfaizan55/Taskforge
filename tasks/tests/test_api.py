import requests

url = "http://127.0.0.1:8000/api/predict-task/"
data = {
    "task_text": "Need to integrate Stripe payment gateway for user subscriptions"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())