import pandas as pd

DATA_PATH = "astana_real_estate_dataset.csv"


def main():
    df = pd.read_csv(DATA_PATH)

    print("Shape:", df.shape)
    print("\nFirst rows:")
    print(df.head().to_string())
    print("\nInfo:")
    df.info()
    print("\nDescription:")
    print(df.describe(include="all").T.to_string())
    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False).to_string())
    print("\nDuplicates:", df.duplicated().sum())


if __name__ == "__main__":
    main()
