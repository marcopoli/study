# Tool-use evaluation

- `tool_tasks.json`: 12 tasks, each with the expected tool and arguments.
- `tool_use_results.json`: the first tool call emitted by the agent for each task (recorded run).
- `run_tool_tasks.py`: re-runs the tasks through the agent and overwrites the results file.
- `score_tool_use.py`: a call is correct only if the tool name and the full argument dictionary match exactly.

Recorded result: 12/12 correct (95% Clopper-Pearson CI 73.5% to 100%).

Notes: the recorded run used a development version of the tool registry that also exposed
`google_scholar_search` and `google_books_search`. Personal and institutional names in two
task prompts were replaced with placeholders for anonymised review.
