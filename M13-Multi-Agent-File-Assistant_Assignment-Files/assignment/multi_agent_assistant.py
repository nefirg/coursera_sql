"""
Task 5-6-7 Part 3: Multi-Agent File Assistant

Create the main orchestrator agent that coordinates multiple specialized agents
to handle complex file operations. This agent uses both FileSearchTool and
FileSummarizerTool to fulfill user requests.

Complete the TODOs below to implement the multi-agent assistant.
"""

import os
from dotenv import load_dotenv
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import DoneTool
from file_tools import ListDirTool, ReadFileTool, WriteFileTool
from search_tool import FileSearchTool
from summarizer_tool import FileSummarizerTool
from pydantic import Field

# Load environment variables from .env file
load_dotenv()

CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


class MultiAgentFileAssistantConfig(lr.ChatAgentConfig):
    # TODO 2: Set a descriptive name for the orchestrator agent - NO SPACES!
    name: str = "multi_agent_file_assistant"

    # TODO 3: Configure the LLM
    llm: lm.OpenAIGPTConfig = Field(
        default=lm.OpenAIGPTConfig(
            chat_model=CHAT_MODEL,
            temperature=0.1,
        )
    )

    # TODO 4: Remind LLM about using tools
    handle_llm_no_tool: str = f"""
    You FORGOT to use one of your TOOLs! Remember that:
    - Use '{ListDirTool.name()}' and '{ReadFileTool.name()}' for basic file operations
    - Use 'file_search' to find files
    - Use 'file_summarize' to summarize files
    - Use '{WriteFileTool.name()}' to write outputs
    - Use '{DoneTool.name()}' to finish
    """

    # TODO 5: Write a comprehensive system message
    system_message: str = f"""
    You are a multi-agent file assistant. Your job is to help the user with file requests.
    1. Use '{ListDirTool.name()}' and '{ReadFileTool.name()}' for basic file operations.
    2. Use 'file_search' to find files matching queries.
    3. Use 'file_summarize' to summarize files.
    4. Use '{WriteFileTool.name()}' to save outputs if needed.
    5. Use '{DoneTool.name()}' to return final results.

    CRITICAL: You CANNOT use multiple tools at once! Use ONE tool at a time,
    wait for the result, then decide what to do next.
    """


def run_multi_agent_assistant(prompt: str) -> str:
    # TODO 6: Create the MultiAgentFileAssistantConfig
    config = MultiAgentFileAssistantConfig()

    # TODO 7: Create the ChatAgent
    agent = lr.ChatAgent(config)

    # TODO 8: Enable the agent to use all required tools
    agent.enable_message([ListDirTool, ReadFileTool, WriteFileTool, FileSearchTool, FileSummarizerTool, DoneTool])

    # TODO 9: Create a Task with interactive=False
    task = lr.Task(
        agent=agent,
        interactive=False,
        tools=[ListDirTool, ReadFileTool, WriteFileTool, FileSearchTool, FileSummarizerTool, DoneTool], max_steps = 10
    )

    # TODO 10: Run the task with the prompt
    result = task.run(prompt)

    # TODO 11: Return the result
    return getattr(result, "content", "") or ""