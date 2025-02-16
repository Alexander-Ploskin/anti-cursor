import click
from src.prompt_generator import generate_prompt
from enum import Enum
import pyperclip


class PromptTargetEnum(str, Enum):
    SAVE_TO_FILE = 'file'
    OUTPUT_TO_TERMINAL = 'terminal'
    COPY_TO_CLIPBOARD = 'clipboard'


@click.command()
@click.argument('source')
@click.option(
    '--target', '-t',
    type=click.Choice([PromptTargetEnum.SAVE_TO_FILE, PromptTargetEnum.OUTPUT_TO_TERMINAL, PromptTargetEnum.COPY_TO_CLIPBOARD], case_sensitive=False),
    default=PromptTargetEnum.COPY_TO_CLIPBOARD,
    help="Specify where to save the generated prompt: 'file', 'terminal', or 'clipboard'."
)
def main(source: str, target: str):
    """
    Generate a prompt from project source code.

    SOURCE can be either a local directory path or a GitHub repository URL.
    """
    prompt_text = generate_prompt(source)

    if target == PromptTargetEnum.SAVE_TO_FILE:
        # Save the prompt to a file named 'prompt.md'
        with open('prompt.md', 'w', encoding='utf-8') as f:
            f.write(prompt_text)
        click.echo("Prompt saved to 'prompt.md'.")

    elif target == PromptTargetEnum.OUTPUT_TO_TERMINAL:
        # Output the prompt to the terminal
        click.echo(prompt_text)

    elif target == PromptTargetEnum.COPY_TO_CLIPBOARD:
        # Copy the prompt to the clipboard
        pyperclip.copy(prompt_text)
        click.echo("Prompt copied to clipboard.")


if __name__ == '__main__':
    main()
