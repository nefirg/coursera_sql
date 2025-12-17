"""
Task 5-6-7: File Search Tool
This is already implemented from previous exercises.
"""

import langroid as lr
from langroid.pydantic_v1 import Field
from file_search_agent import file_search_agent


class FileSearchTool(lr.ToolMessage):
    """Tool to search for files based on a query by delegating to FileSearchAgent."""
    
    request: str = "file_search"
    purpose: str = "Search for files in a directory based on a query"
    
    directory: str = Field(..., description="Directory to search in")
    query: str = Field(..., description="Search query to find relevant files")
    
    def handle(self) -> str:
        """Search for files by delegating to FileSearchAgent."""
        # Create a Task with the file_search_agent
        task = lr.Task(file_search_agent, interactive=False)
        
        # Create a clear prompt for the FileSearchAgent
        prompt = f"Search in directory: {self.directory}\nQuery: {self.query}"
        
        # Run the task and get the result
        result = task.run(prompt)
        
        # Extract and return the content from the result
        return result.content if hasattr(result, 'content') else str(result)