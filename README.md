# Anti-Cursor

**Anti-Cursor** is a Python CLI utility designed to generate Markdown prompts that provide a comprehensive overview of a project's source code. This tool is particularly useful for interacting with large language models (LLMs) — allowing them to reason about, analyze, and understand both the file structure and the complete source code implementation of a project.

The generated prompt includes:
- A detailed **file structure** that illustrates how the project's code is organized.
- The **source code** of each file, giving LLMs the context needed to reason about the project’s implementation and logic.

This utility is ideal for tasks such as:
- Debugging or reviewing code with the assistance of LLMs.
- Generating high-quality documentation based on the project's structure.
- Summarizing and understanding complex projects through automated reasoning.

---

## Features

- Accepts either a **local directory path** or a **GitHub repository URL** as input.  
  *Note:* If an HTTPS GitHub URL does not work as expected, you can also use the SSH URL format (e.g., `git@github.com:Alexander-Ploskin/anti-cursor.git`).
- Generates a highly organized Markdown prompt with:
  - A clear, LLM-friendly introduction outlining the project.
  - A detailed, tree-like representation of the project's file structure.
  - Code listings from individual source files (excluding any files or directories specified in `.gitignore`).
- Supports multiple output targets:
  - Save the prompt to a file (`prompt.md`).
  - Output the prompt directly in the terminal.
  - Copy the prompt into the system clipboard for immediate sharing.
- Clean architecture with a clear separation between CLI, core logic, and file parsing.
- Comes with comprehensive unit tests to ensure proper functionality.

---

## Installation

### From Source

1. **Clone the repository:**
   ```
   git clone https://github.com/Alexander-Ploskin/anti-cursor.git
   ```

2. **Install dependencies:**
   ```
   sudo apt-get install xclip  # Required for clipboard functionality on Linux
   pip install poetry
   poetry install
   ```

### From PyPI

Install the package directly from PyPI:
```
pip install anti-cursor
```

---

## Usage

Run the CLI tool using:
```
anti-cursor <source> [--target <target>]
```

Where `<source>` is either a local directory path or a GitHub repository URL, and `<target>` specifies where to display or save the generated prompt.

### Target Options
The `--target` option allows you to choose the output for the generated prompt:
- `file`: Save the prompt to a file named `prompt.md`.
- `terminal`: Output the prompt directly to the terminal.
- `clipboard`: Copy the prompt to your system clipboard (default).

*Note:* If you experience issues when using an HTTPS GitHub URL, try using the SSH URL format (for example: `git@github.com:Alexander-Ploskin/anti-cursor.git`).

---

### Examples

1. **Generate a prompt from a local directory and output it to the terminal:**
   ```
   anti-cursor . --target terminal
   ```

2. **Generate a prompt from a GitHub repository (using HTTPS) and copy it to the clipboard:**
   ```
   anti-cursor https://github.com/Alexander-Ploskin/anti-cursor --target clipboard
   ```

3. **Generate a prompt from a GitHub repository (using SSH) and copy it to the clipboard:**
   ```
   anti-cursor git@github.com:Alexander-Ploskin/anti-cursor.git --target clipboard
   ```

4. **Generate a prompt from a local directory and save it to `prompt.md`:**
   ```
   anti-cursor ./my_project --target file
   ```

### Example of Generated Prompt

Below is an example of what the generated Markdown prompt might look like (trimmed for brevity):

```
## Project Source Code Prompt

Below is the source code of the considered project. The prompt begins with an organized view of the project's file structure — showing how files and directories are arranged — followed by the complete source code for each file, allowing for an in-depth understanding of the project's implementation.

### Project Structure

./
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
└── src/
    ├── __init__.py
    ├── cli.py
    ├── project_parser.py
    └── prompt_generator.py

### Source Code Files

#### README.md
...

#### src/cli.py

import click from prompt_generator
...
```

This example demonstrates how **Anti-Cursor** organizes and presents both the project structure and its source code in a format that is optimized for LLMs to understand and reason about.

---

## Contributing

Contributions are welcome! If you have suggestions or find issues, please open an issue or submit a pull request on GitHub.

---

## License

This project is licensed under the Apache License 2.0. See [LICENSE](./LICENSE) for details.
