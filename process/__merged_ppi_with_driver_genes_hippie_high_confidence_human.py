import pandas as pd

# Load driver and nondriver gene lists
d_lst = pd.read_table('./data/796_drivers.txt', sep='\t', header=None).iloc[:, 0].tolist()
nd_lst = pd.read_table('./data/2187_nondrivers.txt', sep='\t', header=None).iloc[:, 0].tolist()

# Read PathNet file (fix delimiter issue)
ppi_file = "data/hippie_high_confidence_human.csv"
ppi_df = pd.read_csv(ppi_file, sep=",", skiprows=1, names=["protein1", "protein2", "confidence"])

# Check if file loaded correctly
print(ppi_df.head())  # Debugging: Verify correct column structure

# Assign 'stId' and 'name' columns (redundant, can remove if unnecessary)
ppi_df["stId"] = ppi_df["protein1"]
ppi_df["name"] = ppi_df["protein1"]

# Assign gene_type based on labels
def determine_gene_type(row):
    if row['protein1'] in d_lst:
        return 1  # Driver genes
    elif row['protein1'] in nd_lst:
        return 0  # Nondriver genes
    elif row['protein2'] in d_lst:
        return 2  # Genes associated with driver genes
    else:
        return 3  # Rest of the genes

ppi_df["gene_type"] = ppi_df.apply(determine_gene_type, axis=1)

# Determine if protein1 connects to a driver gene
def check_connected_driver_gene(row):
    if row["protein1"] not in d_lst and row["protein2"] in d_lst:
        row["gene_type"] = 2
        return row["protein2"]
    return None

ppi_df["connected_driver_gene"] = ppi_df.apply(check_connected_driver_gene, axis=1)

# Reorder columns
ppi_df = ppi_df[["protein1", "protein2", "connected_driver_gene", "gene_type", "confidence"]]

# Save the processed data
output_file = "data/hippie_high_confidence_human_with_gene_type_and_connected_driver_gene.csv"
ppi_df.to_csv(output_file, index=False)

print(f"✅ Processed data saved to {output_file}")
