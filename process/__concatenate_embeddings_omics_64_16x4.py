import pandas as pd
import os

# List of cancer types
cancer_types = ['BLCA', 'BRCA', 'CESC', 'COAD', 'ESCA', 'HNSC', 'KIRC', 'KIRP', 'LIHC', 
                'LUAD', 'LUSC', 'PRAD', 'READ', 'STAD', 'THCA', 'UCEC'] 

# Base paths for embedding files
base_paths = [
    "data/multiomics/{}/{}_omics_ppi_embeddings_16x4.csv",
    "data/multiomics_meth/CPDB_ppi_embeddings_64.csv"
]

# Output directory
output_dir = "data/multiomics"

for cancer in cancer_types:
    print(f"Processing {cancer}...")

    # Construct file paths dynamically
    file_paths = [path.format(cancer, cancer) for path in base_paths]

    # Check if the first file exists
    if not os.path.exists(file_paths[0]):
        print(f"⚠️ Skipping {cancer}, missing file: {file_paths[0]}")
        continue

    # Load the first file
    combined_embeddings = pd.read_csv(file_paths[0])

    # Ensure 'stId' is the first column
    if "stId" not in combined_embeddings.columns:
        raise ValueError(f"Missing 'stId' column in file: {file_paths[0]}")

    # Collect feature columns
    feature_columns = [col for col in combined_embeddings.columns if col != "stId"]

    # Ensure first file has exactly 64 feature columns
    if len(feature_columns) != 64:
        raise ValueError(f"File {file_paths[0]} has {len(feature_columns)} features, expected 64.")

    # Process additional files
    for file_path in file_paths[1:]:
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        df = pd.read_csv(file_path)

        # Ensure 'stId' is present
        if "stId" not in df.columns:
            raise ValueError(f"Missing 'stId' column in file: {file_path}")

        # Ensure correct feature count
        feature_cols = [col for col in df.columns if col != "stId"]
        if len(feature_cols) != 64:
            raise ValueError(f"File {file_path} has {len(feature_cols)} features, expected 64.")

        # Concatenate feature columns only (keeping 'stId')
        combined_embeddings = pd.concat([combined_embeddings, df.iloc[:, 1:]], axis=1)

    # Ensure final shape is (N genes, 129 columns: stId + 128 features)
    if combined_embeddings.shape[1] != 129:
        raise ValueError(f"Final DataFrame for {cancer} has {combined_embeddings.shape[1]-1} features, expected 128.")

    # Rename columns: "stId", then 0-127
    new_column_names = ["stId"] + list(range(0, 128))
    combined_embeddings.columns = new_column_names

    # Save the combined embeddings
    output_file = f"{output_dir}/{cancer}/{cancer}_omics_ppi_embeddings_128.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    combined_embeddings.to_csv(output_file, index=False)

    print(f"✅ {cancer} embeddings saved to: {output_file}")
