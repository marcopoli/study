"""Run the 12 tool-use tasks through the UniVox agent and record the first tool call.

Adapted from the original evaluation runner (study_buddy/evaluation/run_evaluation.py):
for each task, the agent is invoked once and the first tool call it emits is stored
as the prediction. Run from the repository root:
    python evaluation/tool_use/run_tool_tasks.py
"""
import asyncio
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.append(os.path.join(REPO_ROOT, "system"))

from study_buddy.agent import compiled_graph  # noqa: E402

TASKS_PATH = os.path.join(SCRIPT_DIR, "tool_tasks.json")
RESULTS_PATH = os.path.join(SCRIPT_DIR, "tool_use_results.json")


async def run_agent(task_input, config):
    tool_calls = []
    async for event in compiled_graph.astream(
        {"messages": [{"role": "user", "content": task_input}]}, config=config
    ):
        for key, value in event.items():
            if key == "agent" and value.get("messages"):
                message = value["messages"][-1]
                if getattr(message, "tool_calls", None):
                    tool_calls.extend(message.tool_calls)
    return tool_calls


async def main():
    with open(TASKS_PATH, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    results = []
    for task in tasks:
        config = {"configurable": {"thread_id": task["id"]}}
        tool_calls = await run_agent(task["task"], config)
        predicted = (
            {"tool_name": tool_calls[0].get("name"), "arguments": tool_calls[0].get("args")}
            if tool_calls else None
        )
        results.append({
            "id": task["id"],
            "type": task["type"],
            "task": task["task"],
            "ground_truth": task["ground_truth"],
            "predicted_output": {"tool_call": predicted},
        })
        print(f"{task['id']}: {predicted}")

    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(results)} results to {RESULTS_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
