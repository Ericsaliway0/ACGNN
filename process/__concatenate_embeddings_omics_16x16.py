import pandas as pd

# Paths to the input files
file_paths = [
    "data/multiomics_meth/UCEC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/THCA_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/STAD_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/READ_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/PRAD_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/LUSC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/LUAD_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/LIHC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/KIRP_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/KIRC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/HNSC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/ESCA_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/COAD_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/CESC_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/BRCA_embeddings_lr0.001_dim16_lay2_epo100_final.csv",
    "data/multiomics_meth/BLCA_embeddings_lr0.001_dim16_lay2_epo100_final.csv"
]

# Load the first file
combined_embeddings = pd.read_csv(file_paths[0])

# Ensure 'stId' is the first column
if "stId" not in combined_embeddings.columns:
    raise ValueError(f"Missing 'stId' column in file: {file_paths[0]}")

# Collect feature columns
feature_columns = [col for col in combined_embeddings.columns if col != "stId"]

# Ensure first file has exactly 16 feature columns
if len(feature_columns) != 16:
    raise ValueError(f"File {file_paths[0]} has {len(feature_columns)} features, expected 16.")

# Process the rest of the files
for file_path in file_paths[1:]:
    df = pd.read_csv(file_path)

    # Ensure 'stId' is the first column
    if "stId" not in df.columns:
        raise ValueError(f"Missing 'stId' column in file: {file_path}")

    # Ensure each file has 16 feature columns
    feature_cols = [col for col in df.columns if col != "stId"]
    if len(feature_cols) != 16:
        raise ValueError(f"File {file_path} has {len(feature_cols)} features, expected 16.")

    # Concatenate feature columns only, maintaining 'stId'
    combined_embeddings = pd.concat([combined_embeddings, df.iloc[:, 1:]], axis=1)

# Ensure final shape is (N genes, 257 columns: stId + 256 features)
if combined_embeddings.shape[1] != 257:
    raise ValueError(f"Final DataFrame has {combined_embeddings.shape[1]-1} features, expected 256.")

# Rename columns: "stId", then 0-255
new_column_names = ["stId"] + list(range(0, 256))
combined_embeddings.columns = new_column_names

# Save the concatenated embeddings
output_file = "data/multiomics_meth/omics_ppi_embeddings_16x16.csv"
combined_embeddings.to_csv(output_file, index=False)

print(f"✅ Combined embeddings saved to: {output_file}")
