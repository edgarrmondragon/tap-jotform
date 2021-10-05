# tap-jotform

`tap-jotform` is a Singer tap for Jotform.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

```bash
pipx install git+https://github.com/edgarrmondragon/tap-jotform.git
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-jotform --about
```

| Setting | Required | Default | Description |
|:-:|:-:|:-:|:-:|
| `api_key` | Yes || Authentication key. See https://api.jotform.com/docs/#authentication |
| `api_url` | No | `https://api.jotform.com` | API Base URL |
| `user_agent` | No | `tap-jotform/x.y.z` | User-Agent header |

### Source Authentication and Authorization

To generate an API key, follow the instructions in https://api.jotform.com/docs/#gettingstarted.

## Usage

You can easily run `tap-jotform` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-jotform --version
tap-jotform --help
tap-jotform --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_jotform/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-jotform` CLI interface directly using `poetry run`:

```bash
poetry run tap-jotform --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-jotform
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-jotform --version
# OR run a test `elt` pipeline:
meltano elt tap-jotform target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
