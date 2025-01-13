from typing import Tuple
import click
import requests
import subprocess
import json


def exec_sh_cmd(cmd: str) -> Tuple[str, str]:
    """Executes a bash command.

    Args:
      cmd: The command to exectute.

    Returns:
      Tuple[str, str]: A tuple, with the first value being the output and the second the error, if there is one.
    """

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        output = result.stdout.decode("utf-8").strip()
        err = result.stderr.decode("utf-8").strip()
        return output, err
    except subprocess.CalledProcessError as e:
        return None, str(e)


@click.group()
def cli():
    """A CLI for demonstrating multiple commands."""
    pass

@cli.command(name="collections")
@click.option("--collection", default=None, help="Collection name.")
def collections(collection):
    """List of collections."""
    
    cmd = "curl -u agnt:smth http://localhost:8000/api/v1/collections"

    output, err = exec_sh_cmd(cmd)

    jsn = json.loads(output)
    formatted_json = json.dumps(jsn, indent=4, sort_keys=True)
    click.echo(formatted_json)


@cli.command(name="qry")
@click.option("--question", default=None, help="Question to ask")
def collections(question):
    """Ask a question."""

    data = json.dumps({
        "qry": question,
        "file_system_path": "/Users/simon.stipcich/code/azdo/Platform-RaffleMania/"
    })

    cmd = f"""
        curl --location 'http://localhost:6001/qry' \
            --header 'Content-Type: application/json' \
            --data '{data}'
    """

    output, err = exec_sh_cmd(cmd)

    jsn = json.loads(output)["output"]
    formatted_json = json.dumps(jsn, indent=4, sort_keys=True)
    click.echo(formatted_json)


if __name__ == '__main__':
    cli()
