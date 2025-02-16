import os
import tempfile
import subprocess
import shutil
from gitignore_parser import parse_gitignore
from src.project_parser import get_project_structure, get_source_files


def generate_prompt(source):
    """
    Generate a markdown prompt that describes the project structure and the source files.
    The prompt includes:
      - An introductory explanation to help an LLM understand the context.
      - A Markdown-formatted project structure tree.
      - Content from each source file (displayed with its file name).
    """
    # Determine whether source is a GitHub URL or a local path.
    if source.startswith("http://") or source.startswith("https://") or source.startswith("git@github.com"):
        temp_dir = tempfile.mkdtemp(prefix='repo_')
        try:
            subprocess.run(
                ["git", "clone", source, temp_dir],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            project_path = temp_dir
        except subprocess.CalledProcessError as e:
            shutil.rmtree(temp_dir)
            return f"Error cloning repository: {e}"
    else:
        if not os.path.exists(source) or not os.path.isdir(source):
            return "Error: Provided source path does not exist or is not a directory."
        project_path = source

    # Parse the .gitignore file if it exists
    gitignore_path = os.path.join(project_path, ".gitignore")
    if os.path.exists(gitignore_path):
        matches = parse_gitignore(gitignore_path)
    else:
        matches = lambda path: False  # If no .gitignore, nothing is ignored

    prompt_lines = []
    # Initial explanation to help an LLM understand the project
    prompt_lines.append("## Project Source Code Prompt\n")
    prompt_lines.append(
        "Below is the source code of the considered project. The prompt begins with an organized view of the project's file structure, showing how the code is organized across directories and files. "
        "Following this overview, the complete source code for each file is provided, allowing for an in-depth understanding of the project's implementation.\n"
    )
    
    # Include project structure
    prompt_lines.append("### Project Structure\n")
    structure = get_project_structure(project_path)
    prompt_lines.append("``````\n" + structure + "\n``````\n")
    
    # Include source code from files, skipping ignored files
    prompt_lines.append("### Source Code Files\n")
    source_files = get_source_files(project_path)
    for file_path in source_files:
        if matches(file_path):  # Skip files ignored by .gitignore rules
            continue

        relative_path = os.path.relpath(file_path, project_path)
        prompt_lines.append(f"#### {relative_path}\n")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            code = f"Error reading file: {e}"
        
        prompt_lines.append("```")
        prompt_lines.append(code)
        prompt_lines.append("```")
    
    prompt_result = "\n".join(prompt_lines)
    
    # Cleanup temporary directory if applicable.
    if source.startswith("http://") or source.startswith("https://"):
        shutil.rmtree(project_path)
    
    return prompt_result
