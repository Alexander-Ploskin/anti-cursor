import os
from gitignore_parser import parse_gitignore


def get_project_structure(root_path):
    """
    Return a string representing the directory tree of the project,
    excluding files and directories that match the .gitignore rules.
    
    The root folder will be marked as '.', and the tree will be formatted like:
    
      ./
      └── src/
          └── prompt_generator/
               ├── __init__.py
               ├── cli.py
               ├── prompt_generator.py
               └── project_parser.py
    """
    # Convert to absolute path to ensure correct matching
    root_abs = os.path.abspath(root_path)
    # Prepare the .gitignore matcher (using relative paths for matching)
    gitignore_path = os.path.join(root_abs, ".gitignore")
    matcher = parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else lambda path: False

    def build_tree(current_path, prefix):
        """
        Recursively build the tree lines for the directory at current_path.
        """
        entries = []
        # List all entries in sorted order
        for entry in sorted(os.listdir(current_path)):
            abs_entry = os.path.join(current_path, entry)
            # Skip if the entry is gitignored
            if matcher(os.path.join(abs_entry, root_abs)):
                continue
            # Explicitly skip directories named ".git" (even if not gitignored)
            if os.path.isdir(abs_entry) and entry == ".git":
                continue
            entries.append((entry, os.path.isdir(abs_entry)))
        
        lines = []
        for i, (name, is_dir) in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            # Append a '/' to directory names
            line = prefix + connector + (name + "/" if is_dir else name)
            lines.append(line)
            # If this entry is a directory, process its children recursively
            if is_dir:
                new_prefix = prefix + ("    " if is_last else "│   ")
                child_path = os.path.join(current_path, name)
                lines.extend(build_tree(child_path, new_prefix))
        return lines

    # The root is always shown as "."
    tree_lines = ["./"]
    tree_lines.extend(build_tree(root_abs, ""))
    return "\n".join(tree_lines)


def get_source_files(root_path):
    """
    Return a list of file paths containing source code,
    excluding those that match .gitignore rules.
    """
    root_abs = os.path.abspath(root_path)
    gitignore_path = os.path.join(root_abs, ".gitignore")
    matcher = parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else lambda path: False

    source_files = []
    for dirpath, _, filenames in os.walk(root_abs):
        # Skip any directory that has a ".git" part in its path (not just if its basename is ".git")
        if ".git" in os.path.normpath(dirpath).split(os.sep):
            continue

        for fname in filenames:
            abs_file = os.path.join(dirpath, fname)
            if not matcher(abs_file):
                source_files.append(abs_file)
    return source_files
