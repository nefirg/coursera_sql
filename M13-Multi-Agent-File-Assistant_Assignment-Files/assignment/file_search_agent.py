"""
Task 5-6-7: File Search Agent
This is already implemented from previous exercises.
"""

import os
from dotenv import load_dotenv
import langroid as lr
import langroid.language_models as lm
from langroid.agent.tools.orchestration import DoneTool
from file_tools import ListDirTool, ReadFileTool

# Load environment variables from .env file
load_dotenv()

# Get model from environment, default to Gemini if not set
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gemini-2.5-flash")


class FileSearchAgentConfig(lr.ChatAgentConfig):
    """Configuration for the file search specialist agent."""
    
    name: str = "FileSearchAgent"
    llm: lm.OpenAIGPTConfig = lm.OpenAIGPTConfig(
        chat_model=CHAT_MODEL,
    )
    # IMPORTANT -- this nudges the agent to use tools when it forgets
    handle_llm_no_tool:str = f"""
    You FORGOT to use one of your TOOLs! Remember that:
    - You must use a combination of {ListDirTool.name()} and {ReadFileTool.name()} 
        to search for files;
    - You should use {DoneTool.name()} to return your results;
    """

    system_message: str = f"""You are a file search specialist. Your job is to search for files
    that match a given query by examining their contents.
    
    When given a directory and search query, follow these steps:
    1. Use {ListDirTool.name()} to list all files in the directory
    2. For each file found, use {ReadFileTool.name()} to read its contents
    3. Check if the file content is relevant to the search query
    4. Keep track of all files that match the query
    
    A file matches if:
    - It contains keywords from the query
    - Its content is related to the query topic
    - It has information relevant to what the user is looking for
    
    Be thorough in your search and check all files in the directory.
    
    When you find matching files, use `{DoneTool.name()}` to return your results.
    In the `content` field, provide:
    - The names of files that match the query
    - A brief explanation of WHY each file matches (what relevant content it contains)
    - Format your response clearly with each file on its own line
    
    IMPORTANT: If no files match, use `{DoneTool.name()}` with content = EMPTY string!
    """


# Export the agent for use by other modules
file_search_agent = lr.ChatAgent(FileSearchAgentConfig())
file_search_agent.enable_message([ListDirTool, ReadFileTool, DoneTool])


def run_file_search(directory: str, query: str) -> str:
    """
    Create and run a file search agent to find files matching a query.
    
    Args:
        directory: The directory to search in
        query: The search query to match against file contents
        
    Returns:
        A string listing the matching files, or a message if no matches
    """
    # Use the global file_search_agent instance
    # Create the search task
    task = lr.Task(file_search_agent, interactive=False)
    
    # Create a clear prompt for the agent
    prompt = f"""Search for files in the directory '{directory}' that match this query: '{query}'
    
    Please search through all files in the directory and identify which ones are relevant to the query."""
    
    # Run the task and get the result
    result = task.run(prompt)
    
    return result.content if hasattr(result, 'content') else str(result)