import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@app.route("/task-created", methods=["POST"])
def task_created():
    task = request.get_json()

    task_name = task.get("name", "Unknown task")
    task_id = task.get("id", "Unknown ID")
    priority = task.get("priority", 50)
    assignee = task.get("assignee") or "Unassigned"

    prompt = f"""
You are an AI assistant integrated with a Flowable workflow engine.

A new workflow task has been created.

Task name: {task_name}
Task ID: {task_id}
Priority: {priority}
Assignee: {assignee}

Give a short recommendation for what should happen next.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    recommendation = response.output_text

    print("\nNew Flowable task received!")
    print(f"Task: {task_name}")
    print(f"Task ID: {task_id}")
    print("\nAI Assistant:")
    print(recommendation)
    print("-" * 50)

    return jsonify({
        "task_id": task_id,
        "recommendation": recommendation
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)