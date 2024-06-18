from approvaltests.approvals import verify

from day_counts.core import (
    acc_from_avro,
    apply_cutpoint,
    counts_from_csv,
    counts_from_df,
    counts_to_csv,
    daily,
    magnitude,
)


def test_counts_60():
    raw_data = acc_from_avro("tests/small.avro", "US/Central")
    counts_1s = counts_from_df(raw_data, 60)
    counts_to_csv(counts_1s, "/tmp/1s_counts.csv.gz")
    counts_60 = counts_from_csv("/tmp/1s_counts.csv.gz", 60)
    magnitude_counts = magnitude(counts_60)
    intensity = apply_cutpoint(magnitude_counts, 3000)
    days = daily(intensity)
    verify(days)


def test_counts_after_sum():
    raw_data = acc_from_avro("tests/small.avro", "US/Central")
    counts_1s = counts_from_df(raw_data, 1)
    counts_to_csv(counts_1s, "/tmp/1s_counts.csv.gz")
    counts_60 = counts_from_csv("/tmp/1s_counts.csv.gz", 60)
    original_counts_60 = counts_from_df(raw_data, 60)
    assert (counts_60 == original_counts_60).all().all()
