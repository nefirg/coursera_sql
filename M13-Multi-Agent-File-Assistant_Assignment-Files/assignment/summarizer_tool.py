"""
Task 5-6-7 Part 2: File Summarizer Tool

Wrap the FileSummarizerAgent as a tool that can be used by other agents.
This enables delegation - other agents can ask for file summaries.

Complete the TODOs below to implement the summarizer tool.
"""

import langroid as lr
from pydantic import Field
from file_summarizer_agent import file_summarizer_agent  # TODO 1: Import agent

class FileSummarizerTool(lr.ToolMessage):
    # TODO 2: Set the request name for this tool
    request: str = "file_summarize"

    # TODO 3: Add a clear purpose description
    purpose: str = "Summarizes the contents of a file using the summarizer agent"

    # TODO 4: Add a file_path field with description
    file_path: str = Field(
        ...,
        description="Path to the file to summarize"
    )

    def handle(self) -> str:
        # TODO 5: Create a Task with the file_summarizer_agent
        task = lr.Task(agent=file_summarizer_agent, interactive=False, 		  		    tools=[file_summarizer_agent], max_steps = 10
	)

        # TODO 6: Create a prompt for the agent
        prompt = f"Please summarize the file: {self.file_path}"

        # TODO 7: Run the task and get the result
        result = task.run(prompt)

        # TODO 8: Return the content from the result
        return getattr(result, "content", "") or ""