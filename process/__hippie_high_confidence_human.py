import pandas as pd

# Define input and output file paths
input_file = "gat/data/hippie_current.txt"
output_file = "gat/data/hippie_high_confidence_human.csv"

# Read the tab-delimited file
df = pd.read_csv(input_file, sep="\t", header=None, low_memory=False)

# Assign column names based on expected format
df.columns = ["Protein_A", "ID_A", "Protein_B", "ID_B", "Score", "Details"]

# Convert Score to numeric (ensure proper filtering)
df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

# Filter for Score >= 0.99
df_filtered = df[df["Score"] >= 0.8]

# Remove "_HUMAN" suffix from protein names
df_filtered["Protein_A"] = df_filtered["Protein_A"].str.replace("_HUMAN", "", regex=False)
df_filtered["Protein_B"] = df_filtered["Protein_B"].str.replace("_HUMAN", "", regex=False)

# Select only Protein_A, Protein_B, and Score
df_selected = df_filtered[["Protein_A", "Protein_B", "Score"]]

# Save to CSV
df_selected.to_csv(output_file, index=False)

print(f"Filtered data saved to: {output_file}")
