from sys import argv

from day_counts.core import acc_from_avro, counts_from_df, counts_to_csv

if __name__ == "__main__":
    try:
        in_file = snakemake.input[0]
        out_file = snakemake.output[0]
    except NameError:
        in_file = argv[1]
        out_file = argv[2]
    raw_data = acc_from_avro(in_file, "us/central")
    epochs = counts_from_df(raw_data, 1)
    counts_to_csv(epochs, out_file)
