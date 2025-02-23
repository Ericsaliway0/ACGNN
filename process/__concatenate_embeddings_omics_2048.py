import pandas as pd

# Paths to the input files
file_paths = [
    "gat/data/multiomics_meth/ppi_embeddings_lr0.001_dim1024_lay2_epo10_final.csv",
    "gat/data/multiomics_meth/omics_ppi_embeddings_256x4.csv"
    ##"gat/data/pathnet_mutation_gene_embeddings_lr0.0001_dim64_lay2_epo100_final.csv",
    ##"gat/data/pathnet_expression_gene_embeddings_lr0.0001_dim64_lay2_epo100_final.csv"
]

# Load the embeddings from each file
embeddings = [pd.read_csv(file_path,) for file_path in file_paths]

# Merge the embeddings on the "stId" column without adding suffixes
combined_embeddings = embeddings[0]
for embed_df in embeddings[1:]:
    combined_embeddings = pd.merge(combined_embeddings, embed_df, on="stId")

# Rename the columns: "stId" as the first column, then numeric headers from 0 to 191
new_column_names = ["stId"] + list(range(0, combined_embeddings.shape[1] - 1))
combined_embeddings.columns = new_column_names

# Save the concatenated embeddings to a new CSV file
output_file = "gat/data/multiomics_meth/omics_ppi_embeddings_2048.csv"
combined_embeddings.to_csv(output_file, index=False)

print(f"Combined embeddings saved to: {output_file}")
