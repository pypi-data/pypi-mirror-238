# Fscan

Fscan pipeline for characterizing persistent narrowband spectral artifacts in gravitational wave detector data

## Installation

To use the Fscan workflow, the best practice is to use either the
installed version (in the pulsar user account at LHO and LLO) or to
clone the repository and use the scripts from a local version. To
install Fscan, please follow these instructions

1. Clone the Fscan repository

2. Create / activate a conda environment (e.g. `conda create -n
   fscan-py3.10 -c conda-forge python=3.10`)

3. Activate the `fscan-py3.10` environment and install using `pip
   install fscan/`. This enables the environment to gain access to
   Fscan command line scripts

## Example for running Fscan

Run the `FscanDriver <args>` exectuable with appropriate arguments (see `FscanDriver -h` for additional details). For example at CIT:

```bash
[...@ldas-grid public_html]$ /home/evan.goetz/lscrepos/fscan-eg/scripts/FscanDriver -C 1 -O 1 -A ligo.dev.o4.detchar.linefind.fscan -U evan.goetz --full-band-avg=1 --analysisStart=20200229 --analysisDuration=1day --averageDuration=1day -y /home/evan.goetz/lscrepos/fscan-eg/configuration/example_ch_info.yml -f . -s /home/evan.goetz/opt/lscsoft/bin/ -a /home/evan.goetz/opt/lscsoft/bin/ -S /home/evan.goetz/opt/lscsoft/bin/
```

### Another example (using a configuration file)

Running from the Fscan source directory,

```bash
FscanDriver --config configuration/example.config
```

Be sure to edit the arguments in `example.config` to reflect the locations of your lalsuite and fscan installations.
