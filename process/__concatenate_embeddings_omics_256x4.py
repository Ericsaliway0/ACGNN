import pandas as pd

# Paths to the input files
file_paths = [
    "data/multiomics_meth/omics_ppi_embeddings_16x16.csv",
    "data/multiomics_ge/omics_ppi_embeddings_16x16.csv",
    "data/multiomics_cna/omics_ppi_embeddings_16x16.csv",
    "data/multiomics_mf/omics_ppi_embeddings_16x16.csv"
]

# Load the first file
combined_embeddings = pd.read_csv(file_paths[0])

# Ensure 'stId' is the first column
if "stId" not in combined_embeddings.columns:
    raise ValueError(f"Missing 'stId' column in file: {file_paths[0]}")

# Collect feature columns
feature_columns = [col for col in combined_embeddings.columns if col != "stId"]

# Ensure first file has exactly 256 feature columns
if len(feature_columns) != 256:
    raise ValueError(f"File {file_paths[0]} has {len(feature_columns)} features, expected 256.")

# Process the rest of the files
for file_path in file_paths[1:]:
    df = pd.read_csv(file_path)

    # Ensure 'stId' is the first column
    if "stId" not in df.columns:
        raise ValueError(f"Missing 'stId' column in file: {file_path}")

    # Ensure each file has 256 feature columns
    feature_cols = [col for col in df.columns if col != "stId"]
    if len(feature_cols) != 256:
        raise ValueError(f"File {file_path} has {len(feature_cols)} features, expected 256.")

    # Concatenate feature columns only, maintaining 'stId'
    combined_embeddings = pd.concat([combined_embeddings, df.iloc[:, 1:]], axis=1)

# Ensure final shape is (N genes, 1025 columns: stId + 1024 features)
if combined_embeddings.shape[1] != 1025:
    raise ValueError(f"Final DataFrame has {combined_embeddings.shape[1]-1} features, expected 1024.")

# Rename columns: "stId", then 0-1023
new_column_names = ["stId"] + list(range(0, 1024))
combined_embeddings.columns = new_column_names

# Save the concatenated embeddings
output_file = "data/omics_ppi_embeddings_256x4.csv"
combined_embeddings.to_csv(output_file, index=False)

print(f"✅ Combined embeddings saved to: {output_file}")
