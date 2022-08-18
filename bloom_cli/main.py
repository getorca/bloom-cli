import typer
from typing import Optional
import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich import print
from rich.prompt import Prompt
from enum import Enum


load_dotenv()
app = typer.Typer()

class Decoding(str, Enum):
    sampling = 'sampling'
    greedy = 'greedy'


def log_bloom(prompt, generated_text):
    """

    :return:
    """
    filename = 'bloom_log.jsonl'
    data = {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'prompt': prompt,
        'generated_text': generated_text
    }
    if os.path.exists(filename):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new
    with open('bloom_log.jsonl', append_write) as f:
        f.write(f'{json.dumps(data)} \n')

def query_bloom(payload, api_token, decoding):
    """
    Querries bloom by the huggingface inference api.
    :param decoding:
    :param do_sample:
    :param api_token:
    :param payload:
    :return:
    """
    payload['do_sample'] = False if decoding.lower() == 'greedy' else True
    api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"
    headers = {"Authorization": f"Bearer {api_token}"}
    response = requests.request("POST", api_url, headers=headers, json=payload)
    return response.json()

@app.command()
def main(
        prompt: Optional[str] = typer.Option(None, help='A single input to passed to Bloom for completion'),
        api_token: str = typer.Option(None, envvar="API_TOKEN", help='An API token for hugging face inference. Create a token for free at https://huggingface.co/settings/tokens'),
        regressive_mode: bool = typer.Option(True, help='Set to false if you don\'t want to continue'),
        decoding: Optional[Decoding] = typer.Option(Decoding.sampling, case_sensitive=False, help='Whether to use `sampling` or `greedy` decoding. Use `sampling` for more creative responses, and `greedy` for more accurate responses.')
):
    """

    :param decoding:
    :param regressive_mode:
    :param api_token:
    :param prompt:
    :return:
    """

    if not api_token:
        print("[bold red]An API_TOKEN is required.[/bold red] Enter set one in the .env file or pass it with --api_token. An API_TOKEN for hugging face inference can be created at https://huggingface.co/settings/tokens")
        raise typer.Exit()

    if not prompt:
        prompt = Prompt.ask('[blue]Enter prompt for completion[/blue]')


    if prompt.lower() in ['exit', 'exit()', 'quit', 'quit()', 'close']:
        print('[yellow]Closing the Bloom Cli. Good bye.[/yellow]')
        raise typer.Exit()

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        TimeElapsedColumn()
        # transient=True
    ) as progress:
        progress.add_task(description="Processing...", total=None)
        response = query_bloom({"inputs": prompt}, api_token=api_token, decoding=decoding)
    print('[bold green]Done \u2714 [/bold green]')
    if 'error' in response:
        log_bloom(prompt=prompt, generated_text=f"ERROR: {response['error']}")
        print(f"[bold red]Error:[/bold red] [red]{response['error']}[/red]")
    else:
        generated_text = response[0]['generated_text']
        log_bloom(prompt=prompt, generated_text=generated_text)
        print('[yellow]Bloom generated text:[/yellow]')
        print(generated_text)

    if regressive_mode:
        main(prompt=None, api_token=api_token, regressive_mode=regressive_mode, decoding=decoding)
    else:
        raise typer.Exit()


if __name__ == '__main__':
    print('[yellow]Welcome to the bloom-cli.[/yellow]')
    app()