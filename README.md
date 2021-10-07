# `tap-jotform`

Singer Tap for Jotform.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `sync`
* `catalog`
* `state`
* `discover`

## Settings

| Setting   | Required | Default | Description |
|:----------|:--------:|:-------:|:------------|
| `api_key` | True     | None    | Authentication key. See https://api.jotform.com/docs/#authentication |
| `api_url` | False    | https://api.jotform.com | API Base URL |
| `user_agent` | False    | tap-jotform/0.0.1 | User-Agent header |

A full list of supported settings and capabilities is available by running: `tap-jotform --about`

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
