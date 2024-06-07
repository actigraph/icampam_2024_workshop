import pandas as pd
import pandavro as pdx
from agcounts.extract import get_counts


def acc_from_avro(avro_file: str, timezone: str) -> pd.DataFrame:
    raw_acc = pdx.read_avro(avro_file)
    frequency = 1 / raw_acc.SampleOrder.max()
    raw_acc.Timestamp = raw_acc.Timestamp + raw_acc.SampleOrder * frequency
    raw_acc.Timestamp = pd.to_datetime(raw_acc.Timestamp, unit="s")
    raw_acc.set_index("Timestamp", inplace=True)
    raw_acc.tz_localize(timezone)
    return raw_acc


def counts_from_df(raw_acc: pd.DataFrame, epoch: int) -> pd.DataFrame:
    counts = get_counts(raw_acc[["X", "Y", "Z"]].values, freq=32, epoch=epoch)
    indexes = (
        raw_acc.index.to_series()
        .groupby(pd.Grouper(freq=f"{epoch}s", origin="start_day"))
        .first()
    )
    counts = pd.DataFrame(counts, columns=["X", "Y", "Z"], index=indexes[: len(counts)])
    return counts


def counts_to_csv(counts: pd.DataFrame, filename: str):
    counts.to_csv(filename)


def counts_from_csv(filename: str, epoch: int) -> pd.DataFrame:
    counts_1s = pd.read_csv(filename, parse_dates=[0], index_col="Timestamp")
    counts = counts_1s.groupby(pd.Grouper(freq=f"{epoch}s", origin="start_day")).sum()
    return counts


def magnitude(counts: pd.DataFrame) -> pd.Series:
    return (counts**2).sum(axis=1) ** 0.5


def apply_cutpoint(magnitude_counts: pd.Series, cutpoint: int) -> pd.Series:
    return magnitude_counts >= cutpoint


def daily(data: pd.Series) -> pd.Series:
    return data.groupby(pd.Grouper(freq="1d", origin="start_day")).sum()


if __name__ == "__main__":
    raw_data = acc_from_avro(
        "Accelerometer_ADXL_4265a3b3-16ab-4bcd-841c-04c44dea3296.avro", "US/Central"
    )
    epochs = counts_from_df(raw_data, 1)
    counts_to_csv(epochs, "1s_counts.csv.gz")
    counts_60 = counts_from_csv("1s_counts.csv.gz", 60)
    magnitude_counts = magnitude(counts_60)
    intensity = apply_cutpoint(magnitude_counts, 3000)
    days = daily(intensity)
