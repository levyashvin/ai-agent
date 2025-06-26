# AI Coding Agent

This repository contains an AI-powered coding agent that leverages Google's Gemini LLM to answer questions, plan function calls, and interact with a Python codebase. The agent can list files, read file contents, execute Python scripts, and write files, all within a secure working directory.

## Features

- **Natural Language Interface:** Ask coding questions or make requests in plain English.
- **Function Calling:** The agent can plan and execute function calls such as reading files, writing files, and running Python scripts.
- **Extensible Functions:** Modular function system (see the `functions/` directory) for file operations and code execution.
- **Calculator Example:** Includes a sample `calculator/` project for demonstration and testing.
- **Verbose Mode:** Optional verbose output for debugging and transparency.

### Key Directories

- **`functions/`**: Contains modules for file operations and code execution:
  - `get_files_info.py`
  - `get_file_content.py`
  - `write_file.py`
  - `run_python_file.py`
  - `search_in_file.py`
- **`calculator/`**: Example Python project with its own `main.py` and `tests.py`.

## Example working Calculator Bug Fix (Operator Precedence)

The **calculator app** was initially producing incorrect results due to a bug in the operator precedence handling. Specifically, expressions like `"3 + 5 * 2"` were evaluated as `16` instead of the correct result `13`. The issue was caused by the **`+` operator** being evaluated before the **`*` operator**.

### Example Usage

Here’s how the calculator now works:

1. **Basic Calculation (3 + 5)**

   ```bash
   (venv) levyashvin@Yashvin:~/bootdev/ai-agent$ python calculator/main.py "3 + 5"
   ```

   Output:

   ```
   ┌─────────┐
   │  3 + 5  │
   │         │
   │  =      │
   │         │
   │  8      │
   └─────────┘
   ```

2. **Incorrect Calculation (Before Fix - 3 + 5 \* 2)**

   ```bash
   (venv) levyashvin@Yashvin:~/bootdev/ai-agent$ python calculator/main.py "3 + 5 * 2"
   ```

   Output (Incorrect):

   ```
   ┌─────────────┐
   │  3 + 5 * 2  │
   │             │
   │  =          │
   │             │
   │  16         │
   └─────────────┘
   ```

3. **Asking Gemini to fix the issue**

   ```bash
   (venv) levyashvin@Yashvin:~/bootdev/ai-agent$ python main.py "can you fix the bug in the calculator it is giving 3 + 5 * 2 = 16 when it should be 13"
   ```

   Output:

   ```
   - Calling function: get_files_info
   - Calling function: get_file_content
   - Calling function: get_file_content
   - Calling function: write_file
   - Calling function: run_python_file
   <class 'subprocess.CompletedProcess'>
   CompletedProcess(args=['python', '/home/levyashvin/bootdev/ai-agent/calculator/tests.py'], returncode=0, stdout='', stderr='.........\n----------------------------------------------------------------------\nRan 9 tests in 0.001s\n\nOK\n')
   Great! The tests passed, which means the issue with operator precedence has been resolved, and the calculator should now correctly evaluate expressions like "3 + 5 * 2".
   ```

4. **Correct Calculation After the Fix**

   Now, when running the same expression:

   ```bash
   (venv) levyashvin@Yashvin:~/bootdev/ai-agent$ python calculator/main.py "3 + 5 * 2"
   ```

   Output (Correct):

   ```
   ┌─────────────┐
   │  3 + 5 * 2  │
   │             │
   │  =          │
   │             │
   │  13         │
   └─────────────┘
   ```

### Summary:

* The bug in the **operator precedence** was fixed by adjusting the calculation logic in the calculator app.
* The **multiplication operator (`*`)** is now correctly evaluated before addition (`+`), resulting in the correct output for expressions like `3 + 5 * 2`.
* Tests were run and passed successfully to verify that the bug was fixed.


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
