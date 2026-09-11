import os
import requests
from openai import OpenAI

FLOWABLE_URL = "http://localhost:8080/flowable-rest/service/runtime/tasks"
FLOWABLE_USER = "rest-admin"
FLOWABLE_PASSWORD = "test"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def get_flowable_tasks():
    response = requests.get(
        FLOWABLE_URL,
        auth=(FLOWABLE_USER, FLOWABLE_PASSWORD)
    )
    response.raise_for_status()
    return response.json()["data"]


def generate_ai_response(task):
    task_name = task["name"]
    priority = task["priority"]
    assignee = task["assignee"]

    prompt = f"""
You are an assistant integrated with Flowable.

Analyze this workflow task and give a short useful recommendation.

Task name: {task_name}
Priority: {priority}
Assignee: {assignee or "Unassigned"}

Mention:
1. The current task status
2. What should be done next

Keep the response concise.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


def main():
    tasks = get_flowable_tasks()

    print(f"Flowable returned {len(tasks)} task(s).")

    for task in tasks:
        print()
        print(f"Task: {task['name']}")
        print(f"Task ID: {task['id']}")
        print()
        print("AI Assistant:")
        print(generate_ai_response(task))


if __name__ == "__main__":
    main()