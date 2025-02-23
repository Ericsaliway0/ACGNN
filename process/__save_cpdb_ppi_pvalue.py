import pandas as pd
import os

# Define file paths
multiomics_file = "data/multiomics/multiomics_cna.csv"
ppi_file = "data/multiomics/CPDB_ppi_0.99.csv"
output_dir = "data/multiomics_cna"  # Output folder

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load multi-omics CNA data
df_omics = pd.read_csv(multiomics_file, sep="\t")  # Ensure correct delimiter

# Load PPI data (filtered for confidence >= 0.99)
df_ppi = pd.read_csv(ppi_file, sep=",")  # Ensure correct delimiter

# Ensure required columns exist
if "Gene" not in df_omics.columns or not {"partner1", "partner2", "confidence"}.issubset(df_ppi.columns):
    raise ValueError("One or more required columns are missing.")

# Set Gene as index for easier merging
df_omics.set_index("Gene", inplace=True)

# Get list of cancer types (columns from omics file)
cancer_types = df_omics.columns.tolist()

# Iterate through each cancer type and save separate files
for cancer in cancer_types:
    # Merge omics data with PPI data where Gene matches partner1
    df_merged = df_ppi.merge(df_omics[[cancer]], left_on="partner1", right_index=True, how="inner")

    # Rename the selected cancer type column for clarity
    df_merged.rename(columns={cancer: "cancer_value"}, inplace=True)

    # Define output filename
    output_file = os.path.join(output_dir, f"CPDB_PPI_{cancer}.csv")

    # Save the filtered data
    df_merged[["partner1", "partner2", "cancer_value", "confidence"]].to_csv(output_file, sep=",", index=False)

    print(f"✅ Saved {output_file}")
