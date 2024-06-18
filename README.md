# Reproducible data analysis
This repository contains the presentation and source code for workshop 5 at the ICAMPAM 2024 conference.

## Source code
The various functions used are in the `day_counts` folder. This folder also contains the source code that will be installed if this module is installed using e.g. `pip`.

## Notebook
`workshop.ipynb` contains a short exercise for calculating ActiGraph counts on some sample data.

## Snakemake
The contained `Snakefile` will process `inputs/big.avro`.

> [!IMPORTANT]
> Make sure you have conda installed to allow `--use-conda` to work

## Docker
You can build the container using

```shell
docker build --tag test .
```