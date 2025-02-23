import pandas as pd

# Load the data
file_path = "data/multiomics_features.csv"
df = pd.read_csv(file_path, index_col=0)

# Define omics categories
omics_types = ["MF", "METH", "GE", "CNA"]

# Ensure correct number of columns per omics type
for omics in omics_types:
    # Select columns starting with the omics type
    selected_columns = [col for col in df.columns if col.startswith(f"{omics}:")]
    
    # If there are more than 16 columns, select only the first 16
    if len(selected_columns) > 16:
        selected_columns = selected_columns[:16]  # Take only the first 16 columns
    elif len(selected_columns) < 16:
        print(f"Warning: {omics} has only {len(selected_columns)} columns instead of 16. Skipping...")
        continue  # Skip this omics type if it doesn't have 16 columns

    df_filtered = df[selected_columns]

    # Rename columns to remove "MF:", "METH:", etc.
    df_filtered.columns = [col.replace(f"{omics}:", "").strip() for col in selected_columns]

    # Define output file name
    output_file = f"data/multiomics/multiomics_{omics.lower()}.csv"

    # Save as a tab-separated file
    df_filtered.to_csv(output_file, sep="\t", index_label="Gene")
    print(f"✅ Saved {output_file} with exactly 16 columns.")
