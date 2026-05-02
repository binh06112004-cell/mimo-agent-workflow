import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("MIMO_API_KEY"),
    base_url="https://api.xiaomimimo.com/v1"
)

class WorkflowAgent:
    def __init__(self):
        self.memory = []
        self.iteration = 0
        self.max_iterations = 5

    def think(self, task):
        self.memory.append({"role": "user", "content": task})
        response = client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "You are an autonomous workflow agent. Break down tasks, reason step by step, and execute actions."},
                *self.memory
            ]
        )
        result = response.choices[0].message.content
        self.memory.append({"role": "assistant", "content": result})
        return result

    def run(self, task):
        print(f"[Agent] Starting task: {task}\n")
        while self.iteration < self.max_iterations:
            self.iteration += 1
            print(f"[Iteration {self.iteration}]")
            output = self.think(task)
            print(f"[Agent Output]\n{output}\n")
            if "DONE" in output or "COMPLETE" in output:
                print("[Agent] Task completed.")
                break
        return self.memory

if __name__ == "__main__":
    agent = WorkflowAgent()
    agent.run("Analyze current market trends and summarize key insights for a business report.")
