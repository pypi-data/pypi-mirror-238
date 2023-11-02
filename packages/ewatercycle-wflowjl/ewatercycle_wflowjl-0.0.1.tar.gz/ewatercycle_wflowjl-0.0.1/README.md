# eWaterCycle plugin for the Wflow.jl hydrological model

Wflow.jl plugin for [eWatercycle](https://ewatercycle.readthedocs.io/).

The Wflow.jl documentation is available at https://deltares.github.io/Wflow.jl/dev/ .

## Installation

eWaterCycle must be installed in a [mamba](https://conda-forge.org/miniforge/) environment. The environment can be created with

```console
wget https://raw.githubusercontent.com/eWaterCycle/ewatercycle/main/environment.yml
mamba env create --name ewatercycle-wflowjl --file environment.yml
conda activate ewatercycle-wflowjl
```

Install this package alongside your eWaterCycle installation

```console
pip install ewatercycle-wflowjl
```

Then Wflow becomes available as one of the eWaterCycle models

```python
from ewatercycle.models import WflowJl
```

Note that unlike other plugins, the WflowJl eWaterCycle model does not run in a container.

This is due to limitations of the Julia language.

## Usage

Usage of Wflow.jl forcing generation and model execution is shown in 
[docs/generate_era5_forcing.ipynb](https://github.com/eWaterCycle/ewatercycle-wflowjl/tree/main/docs/generate_era5_forcing.ipynb) and [docs/wflowjl_local.ipynb](https://github.com/eWaterCycle/ewatercycle-wflow/tree/main/docs/wflowjl_local.ipynb) respectively.

## License

`ewatercycle-wflowjl` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.
