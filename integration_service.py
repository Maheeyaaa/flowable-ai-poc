import os
import time
import requests
from openai import OpenAI

FLOWABLE_URL = "http://localhost:8080/flowable-rest/service/runtime/tasks"
FLOWABLE_USER = "rest-admin"
FLOWABLE_PASSWORD = "test"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

seen_tasks = set()


def get_flowable_tasks():
    response = requests.get(
        FLOWABLE_URL,
        auth=(FLOWABLE_USER, FLOWABLE_PASSWORD)
    )
    response.raise_for_status()
    return response.json()["data"]


def ask_ai(task):
    prompt = f"""
You are an AI assistant integrated with a Flowable workflow engine.

A new workflow task has been detected.

Task name: {task["name"]}
Priority: {task["priority"]}
Assignee: {task["assignee"] or "Unassigned"}

Give a short recommendation for what should happen next.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


def main():
    print("Flowable AI Integration Service started.")
    print("Waiting for new tasks...\n")

    while True:
        tasks = get_flowable_tasks()

        for task in tasks:
            task_id = task["id"]

            if task_id not in seen_tasks:
                seen_tasks.add(task_id)

                print("New Flowable task detected!")
                print(f"Task: {task['name']}")
                print(f"Task ID: {task_id}")
                print("\nAI Assistant:")
                print(ask_ai(task))
                print("\n" + "-" * 50)

        time.sleep(5)


if __name__ == "__main__":
    main()