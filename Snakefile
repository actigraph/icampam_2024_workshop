(inputs,) = glob_wildcards("input/{input_file}.avro")


rule all:
    input:
        expand("daily/{input_file}.csv", input_file=inputs),


rule daily:
    input:
        "counts_1s/{input_file}.csv.gz",
    output:
        "daily/{input_file}.csv",
    conda:
        "environment.yml"
    script:
        "scripts/daily.py"
        


rule counts_1:
    input:
        "input/{input_file}.avro",
    output:
        "counts_1s/{input_file}.csv.gz",
    conda:
        "environment.yml"
    script:
        "scripts/counts.py"
