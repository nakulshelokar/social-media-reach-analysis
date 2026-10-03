import pandas as pd
import numpy as np
import re


def clean_column_names(df):
    df.columns = [
        re.sub(r"_+", "_",
               re.sub(r"[^a-zA-Z0-9]+", "_", str(col).strip().lower())
        ).strip("_")
        for col in df.columns
    ]
    return df


def clean_data(input_file, output_file):

    df = pd.read_csv(input_file)

    print("Original shape:", df.shape)

    # Clean column names
    df = clean_column_names(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove extra spaces from text
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype("string").str.strip()

    # Handle numeric columns
    for col in df.select_dtypes(include="number").columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        df[col] = df[col].fillna(df[col].median())

    # Handle categorical missing values
    for col in df.select_dtypes(include=["object", "string"]).columns:
        if df[col].isna().any():
            mode = df[col].mode()

            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])

    # Convert date columns
    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Save cleaned data
    df.to_csv(output_file, index=False)

    print("Cleaned shape:", df.shape)
    print("Data cleaning completed successfully!")
    print("Saved to:", output_file)


if __name__ == "__main__":

    clean_data(
        "data/raw_data.csv",
        "data/cleaned_data.csv"
    )
