import os
import pandas as pd

DATA_FOLDER = "data"
OUTPUT_FILE = "formatted_output.csv"


def clean_price(price_value):
    """Convert prices like '$3.00' into 3.00."""
    return float(str(price_value).replace("$", "").strip())


def process_data():
    all_files = [
        os.path.join(DATA_FOLDER, file)
        for file in os.listdir(DATA_FOLDER)
        if file.endswith(".csv")
    ]

    processed_frames = []

    for file_path in all_files:
        df = pd.read_csv(file_path)

        # Keep only Pink Morsels
        df = df[df["product"] == "pink morsel"].copy()

        # Convert price to number and calculate sales
        df["price"] = df["price"].apply(clean_price)
        df["sales"] = df["quantity"] * df["price"]

        # Keep only required output columns
        df = df[["sales", "date", "region"]]

        # Rename columns to match required format
        df = df.rename(
            columns={
                "sales": "Sales",
                "date": "Date",
                "region": "Region"
            }
        )

        processed_frames.append(df)

    output_df = pd.concat(processed_frames, ignore_index=True)
    output_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Created {OUTPUT_FILE} with {len(output_df)} rows.")


if __name__ == "__main__":
    process_data()