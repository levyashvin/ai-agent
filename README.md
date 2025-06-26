# AI Coding Agent

This repository contains an AI-powered coding agent that leverages Google's Gemini LLM to answer questions, plan function calls, and interact with a Python codebase. The agent can list files, read file contents, execute Python scripts, and write files, all within a secure working directory.

## Features

- **Natural Language Interface:** Ask coding questions or make requests in plain English.
- **Function Calling:** The agent can plan and execute function calls such as reading files, writing files, and running Python scripts.
- **Extensible Functions:** Modular function system (see the `functions/` directory) for file operations and code execution.
- **Calculator Example:** Includes a sample `calculator/` project for demonstration and testing.
- **Verbose Mode:** Optional verbose output for debugging and transparency.

### Key Directories

- **functions/**: Contains modules for file operations and code execution:
  - `get_files_info.py`
  - `get_file_content.py`
  - `write_file.py`
  - `run_python_file.py`
- **calculator/**: Example Python project with its own `main.py` and `tests.py`.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/levyashvin/ai-agent/
   cd ai-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment:**
   - Create a `.env` file in the root directory with your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

## Usage

Run the agent with a natural language prompt:

```bash
python main.py "How does the calculator render an output?"
```

- Add `--verbose` to enable verbose output:
  ```bash
  python main.py "List all files in the calculator directory" --verbose
  ```

## Configuration

Edit `config.py` to adjust:
- Model version (`MODEL`)
- System prompt (`SYSPROMPT`)
- Working directory (`WORKDIR`)
- Max iterations, timeout, and verbosity

## Testing

Run the included tests for function modules:

```bash
python tests.py
```

## Extending

To add new capabilities, implement a new function in the `functions/` directory and register its schema in `call_function.py`.

## License

[MIT License](LICENSE) (add a LICENSE file if you want to specify this)
