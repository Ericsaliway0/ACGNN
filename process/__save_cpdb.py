import pandas as pd

# Load the edgelist file with a header
file_path = "data/CPDB_uni_edgelist.tsv"
df = pd.read_csv(file_path, sep="\t")  # Auto-detect header

# Ensure necessary columns exist
required_columns = {"partner1", "partner2", "confidence"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing required columns. Expected: {required_columns}")

# Function to remove "_HUMAN" from protein names
def clean_protein_name(name):
    return name.replace("_HUMAN", "")

# Apply cleaning to the protein name columns
df["partner1"] = df["partner1"].astype(str).apply(clean_protein_name)
df["partner2"] = df["partner2"].astype(str).apply(clean_protein_name)

# Convert confidence to numeric and filter entries with confidence >= 0.99
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")
df_filtered = df[df["confidence"] >= 0.99]

# Save the cleaned & filtered data
output_file = "data/multiomics/CPDB_ppi_0.99.csv"
df_filtered.to_csv(output_file, sep=",", index=False)

print(f"✅ Saved cleaned & filtered edgelist to {output_file}")
