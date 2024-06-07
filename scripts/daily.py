from day_counts import core

if __name__ == "__main__":
    counts_60 = core.counts_from_csv(snakemake.input[0], 60)
    magnitude_counts = core.magnitude(counts_60)
    intensity = core.apply_cutpoint(magnitude_counts, 3000)
    days = core.daily(intensity)
    days.to_csv(snakemake.output[0])
