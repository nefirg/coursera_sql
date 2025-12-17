"""
Task 5-6-7 Part 1: File Summarizer Agent

Create an agent that can read files and provide concise summaries.
This agent will be used by other agents to quickly understand file contents.

Complete the TODOs below to implement the file summarizer.
"""

import os
from dotenv import load_dotenv
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import DoneTool
from file_tools import ReadFileTool
from pydantic import Field

# Load environment variables from .env file
load_dotenv()

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


class FileSummarizerAgentConfig(lr.ChatAgentConfig):
    # TODO 1: Set a descriptive name for the agent - NO SPACES!
    name: str = "file_summarizer_agent"

    # TODO 2: Configure the LLM
    llm: lm.OpenAIGPTConfig = Field(
        default=lm.OpenAIGPTConfig(
            chat_model=CHAT_MODEL,
            temperature=0.3
        )
    )

    # IMPORTANT: This nudges the LLM to use a tool when it forgets
    handle_llm_no_tool: str = f"""
    You forgot to use one of your TOOLs!. Remember that:
    - You must use `{ReadFileTool.name()}` to read file contents;
    - You should use `{DoneTool.name()}` to return your summary;    
    """

    # TODO 3: Write a system message
    system_message: str = f"""
    You are a file summarization specialist. Your task is:
      • Read the file using '{ReadFileTool.name()}'
      • Summarize content with 2-3 sentence overview
      • Provide key points as bullet points
      • Use '{DoneTool.name()}' to return the final summary
    """


def run_file_summarizer(file_path: str) -> str:
    # TODO 4: Create the FileSummarizerAgentConfig
    config = FileSummarizerAgentConfig()

    # TODO 5: Create the ChatAgent
    agent = lr.ChatAgent(config)

    # TODO 6: Enable the agent to use the tools
    agent.enable_message([ReadFileTool, DoneTool])

    # TODO 7: Create a Task with interactive=False
    task = lr.Task(agent=agent, interactive=False, tools=[ReadFileTool, DoneTool], 	 	max_steps=10
    )

    # TODO 8: Create a prompt asking to summarize the file
    prompt = f"Please summarize the file: {file_path}"

    # TODO 9: Run the task and get the result
    result = task.run(prompt)

    # TODO 10: Return the result content
    return getattr(result, "content", "") or ""


# TODO 11: Create and export the agent for use by other modules
file_summarizer_agent = lr.ChatAgent(FileSummarizerAgentConfig())
file_summarizer_agent.enable_message([ReadFileTool, DoneTool])
