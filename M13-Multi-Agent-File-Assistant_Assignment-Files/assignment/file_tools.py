"""
Task 5-6-7: Basic File Tools
These are already implemented from previous exercises.
"""

import os
from langroid.pydantic_v1 import Field
import langroid as lr


class ListDirTool(lr.ToolMessage):
    """Tool to list files and directories in a given path."""
    
    request: str = "list_dir"
    purpose: str = "List files and directories in a given path"
    
    path: str = Field(..., description="The directory path to list contents from")
    
    def handle(self) -> str:
        """List directory contents."""
        try:
            if not os.path.exists(self.path) or not os.path.isdir(self.path):
                return f"Error: Invalid directory path '{self.path}'"
            
            return "\n".join(sorted(os.listdir(self.path)))
            
        except Exception as e:
            return f"Error: {str(e)}"


class ReadFileTool(lr.ToolMessage):
    """Tool to read file contents."""
    
    request: str = "read_file"
    purpose: str = "Read the contents of a file"
    
    path: str = Field(
        ...,
        description="The FULL file path to read, relative to the current working directory"
    )
    
    def handle(self) -> str:
        """Read file contents."""
        try:
            with open(self.path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return f"""
            Error: File not found '{self.path}', maybe you 
            forgot to use the FULL path?
            """
        except IsADirectoryError:
            return f"Error: '{self.path}' is a directory, not a file"
        except Exception as e:
            return f"Error: {str(e)}"


class WriteFileTool(lr.ToolMessage):
    """Tool to write content to a file."""
    
    request: str = "write_file"
    purpose: str = "Write content to a file"
    
    path: str = Field(..., description="The file path to write to")
    content: str = Field(..., description="The content to write to the file")
    
    def handle(self) -> str:
        """Write content to file."""
        try:
            with open(self.path, "w") as f:
                f.write(self.content)
            return f"Successfully wrote to {self.path}"
        except Exception as e:
            return f"Error: {str(e)}"