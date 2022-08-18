# Bloom CLI

A simple CLI to play with the large Language model [BLOOM](https://huggingface.co/bigscience/bloom) through the hugging face inference API. Bloom is a text completion model and can be prompeted to completed text. Having been trained on 176 billion parameters, it is one of the most advanced models of it's type. 

![hippo](https://raw.githubusercontent.com/getorca/.gif)


This CLI makes it easy to experiment, but has no particular use case, other than making experimentation easier.

## Features
- a CLI that makes expirementing with bloom easy, continually try single prompts to see what bloom does.
- logs the prompts and generated texts to a json lines file for easy review.

**Note on limitations**

`Input is too long (128 tokens). We're disabling long prompts temporarily`

Hugging face has currently and temporarily disabled long input prompts for the hosted inference API. This make prompting bloom difficult.


## Installation

### Prerequisites
- python 3.8.10 (lower may work, but this is where it was developed and tested)
- poetry
- a free [hugging face account](https://huggingface.co/join) to use create an api token
- a [hugging face api token](https://huggingface.co/settings/tokens)

### From Repo
clone the repo `git clone ...`

change to the directory `cd bloom-cli`

create a python virtual environment  `python3 -m venv venv

activate the venv `source venv/bin/activate`

install with poetry `install poetry`

### From PyPi
...coming soon

## API Docs

**Usage**:

```console
$ bloom-cli [OPTIONS]
```

note we recommend creating a .env file with:
```.env
API_TOKEN: [your_token]
```
alternatively specify it with option --api_token shown below

**Exiting**:

type `exit` and any command prompt to close bloom-cli

**Options**:

* `--prompt TEXT`: A single input to passed to Bloom for completion
* `--api-token TEXT`: An API token for hugging face inference. Create a token for free at https://huggingface.co/settings/tokens  [env var: API_TOKEN]
* `--regressive-mode / --no-regressive-mode`: Set to false if you don't want to continue  [default: True]
* `--decoding [sampling|greedy]`: Whether to use `sampling` or `greedy` decoding. Use `sampling` for more creative responses, and `greedy` for more accurate responses.  [default: sampling]
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.


## ToDo:
 - support for line delimited text file for inputs
 - some unit tests
 - support specifying where the logging file will go