"""
Tests for Multi-Agent File Assistant
"""

import os
from file_summarizer_agent import run_file_summarizer
from multi_agent_assistant import run_multi_agent_assistant


def test_file_summarizer():
    """Test the file summarizer agent creates good summaries."""
    # Test summarizing a file
    summary = run_file_summarizer("myfiles/beethoven.md")
    
    # Check that summary contains expected elements
    assert "summary:" in summary.lower() or "beethoven" in summary.lower()
    assert len(summary) > 50  # Should be a meaningful summary


def test_multi_agent_search_summarize():
    """Test the multi-agent assistant can search and summarize."""
    # Request to find and summarize music files
    response = run_multi_agent_assistant(
        """
        Find files about music in the myfiles directory and 
        tell me which music-related people were discussed in those files.
        """
    )
    
    # Check that response mentions finding files
    response_lower = response.lower()
    assert any(
        word in response_lower for word in
        ["beyonce", "beethoven", "evans"]
    )
    
    
def test_multi_agent_complex():
    """Test handling a complex multi-step request."""
    # Create a test output file path
    output_file = "myfiles/test_summary.txt"
    
    # Request a complex task
    response = run_multi_agent_assistant(
        f"""
        Search for files about finance in myfiles and write 
        a file-by file summary to {output_file}, formatted 
        in markdown, with each header being the topic of the file, and the file-path
        """
    )
    
    # Check the response indicates completion
    assert "wrote" in response.lower() or "created" in response.lower() or "finance" in response.lower()

    # Check that the output file contains expected finance-related terms
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            content = f.read().lower()
        assert "budget" in content
        assert "investment" in content
        assert "debt" in content

    # Cleanup if file was created
    if os.path.exists(output_file):
        os.remove(output_file)