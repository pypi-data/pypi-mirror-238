# Nearly Human Cortex SDK
<p align="center">
    <img src="https://www.nearlyhuman.ai/wp-content/uploads/2022/04/virtual-copy.svg" width="200"/>
</p>

A simple SDK that abstracts the Cortex API.  The application should reflect all of the Cortex routes, and provide a way
to interact with models within an approved client.

## Prerequisites
- Mamba
- Create a github token with repo permissions and set the `GH_TOKEN` environment variable

## Build
```bash
mamba env create -f ./conda.yml

# Build version of Nearly Human Cortex CLI for release
python -m build
```

## Installing the SDK
```bash
mamba create -n cortex_sdk python=3.10 pip -c conda-forge
mamba activate cortex_sdk
pip install cortex-sdk
```

## Running the SDK
```bash
mamba activate cortex_sdk
```
