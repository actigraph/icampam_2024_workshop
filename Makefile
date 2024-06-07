.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PHONY: container format test

container:
	docker build --tag counts .

format:
	isort scripts test day_counts
	black scripts test day_counts

test:
	pytest

run:
	docker run -v .:/mnt counts:latest python scripts/counts.py /mnt/input/big.avro /mnt/test.csv