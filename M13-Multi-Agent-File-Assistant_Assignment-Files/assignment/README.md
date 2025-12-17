# Task 5-6-7: Multi-Agent File Assistant

## Setup Instructions

### Step 1: Navigate to Assignment Folder
```bash
cd <this folder>
```

### Step 2: Set up API Keys
Create a `.env` file in this directory with your API keys:
```bash
# Create .env file
touch .env
```

Add the following to your `.env` file:
```
# Required: Set the LLM model for your class
OPENAI_CHAT_MODEL=your-model-here

# Add the appropriate API key based on your model:
# For OpenAI models:
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_BASE=your-openai-api-base-here

# For Gemini models:
GEMINI_API_KEY=your-gemini-api-key-here

# For other providers, add their specific keys
```

**Important**: 
- Ask your instructor which model to use for `OPENAI_CHAT_MODEL`
- For course LLM setup, ensure both `OPENAI_API_KEY` and `OPENAI_API_BASE` are set based on values provided in the course
- Only add the API key for the provider you're using
- Never commit your `.env` file to version control

### Step 3: Install UV (if not already installed)
```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip:
pip install uv
```

### Step 4: Navigate to the assignment folder and create a virtual environment

**⚠️ CRITICAL**: All scripts and tests MUST be run from the assignment folder. Do not run them from parent directories or other locations.

```bash
# First, navigate to the assignment folder (if not already there)
cd <assignment-folder>

# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 5: Install Dependencies
```bash
uv sync
```

### Step 6: Complete the Exercise
Complete the TODOs in the Python files.

### Step 7: Run Tests

You must continue implementing your code until all tests pass.

```bash
pytest test.py -v
```

You can also override the model at test time using the --model option:
```bash
# Example: Use a specific model for tests
pytest test.py -v --model gemini-2.5-flash
```

#### Debugging Tip

When running your agents, Langroid generates HTML logs that are extremely useful for debugging. Look for log messages like:

```
WARNING - 📊 HTML Log: file:///Users/.../logs/MultiAgentFileAssistant.html
```

This path is clickable in most terminals:
- **Mac**: Hold Cmd and click the path
- **Windows**: Ctrl+click the path
- **Linux**: Ctrl+click or right-click and select "Open Link"
- **If clicking doesn't work**: Copy the entire path and paste it into your browser

These HTML logs show:
- The complete system message sent to the LLM
- All LLM outputs and responses
- Tool calls made by the agent
- Results returned from tool calls
- The full conversation history

Open these HTML files in your browser to see exactly what your agent is doing and help debug any issues.

### Step 8: Verify Your Work
When complete, your implementation should:
- Summarize file contents using the FileSummarizerAgent
- Wrap the summarizer agent as a tool
- Orchestrate multiple agents (search + summarize) through a main assistant

## Your Task

This final exercise brings everything together in a multi-agent system:

1. **Create a file summarizer agent** that reads and summarizes files
2. **Wrap the summarizer as a tool** for delegation
3. **Build a multi-agent orchestrator** that coordinates search and summarization

You'll implement:
- `file_summarizer_agent.py`: Agent that summarizes file contents (Part 1)
- `summarizer_tool.py`: Tool wrapper for the summarizer agent (Part 2)
- `multi_agent_assistant.py`: Main agent that orchestrates everything (Part 3)

The multi-agent system should:
- Use the search tool to find files by content
- Use the summarizer tool to summarize found files
- Coordinate these operations based on user requests
- Handle complex queries like "Find all music files and summarize them"

**Note**: The file search agent, search tool, and basic file tools are already provided from previous assignments. Focus on implementing the summarizer and orchestrator.

See the TODO comments in the code files for specific implementation details.
