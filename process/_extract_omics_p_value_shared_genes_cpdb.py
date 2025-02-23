import pandas as pd
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests
from tqdm import tqdm

# File paths
input_file = "data/CPDB_ppi_0.99.csv"
results_output_file = "data/protein_interaction_p_value_CPDB_ppi_0.99.csv"

# Load the CSV file
data = pd.read_csv(input_file, header=0)

# Get unique genes
unique_genes = pd.unique(data[['partner1', 'partner2']].values.ravel())
N = len(unique_genes)

# Function to compute p-value using Fisher's Exact Test with validation
def compute_p_value_fisher_exact(N, K, M, n):
    contingency_table = [[n, max(0, K - n)], [max(0, M - n), max(0, N - K - M + n)]]
    try:
        _, p_value = fisher_exact(contingency_table, alternative='two-sided')
    except ValueError as e:
        print(f"Error computing Fisher's Exact Test for table {contingency_table}: {e}")
        p_value = 1.0
    return p_value

# Count the number of unique interaction partners for each gene
gene_interaction_group = data.groupby('partner1')['partner2'].nunique().reset_index()
gene_interaction_group.columns = ['gene', 'num_interactions']
gene_interaction_dict = gene_interaction_group.set_index('gene').to_dict()['num_interactions']

# Initialize lists to store results and p-values
results = []
p_values = []

# Get a unique list of genes
genes = sorted(data['partner1'].unique())

# Initialize progress bar for all combinations
total_combinations = len(genes) * (len(genes) - 1) // 2
with tqdm(total=total_combinations) as pbar:
    for i, genei in enumerate(genes):
        for j, genej in enumerate(genes):
            if i < j:
                # Get interaction counts
                K = gene_interaction_dict.get(genei, 0)
                M = gene_interaction_dict.get(genej, 0)

                # Find shared interaction partners
                partners_i = set(data[data['partner1'] == genei]['partner2'])
                partners_j = set(data[data['partner1'] == genej]['partner2'])
                shared_partners = partners_i & partners_j
                n = len(shared_partners)

                # Calculate p-value if shared partners exist
                if n > 0:
                    p_value = compute_p_value_fisher_exact(N, K, M, n)
                else:
                    p_value = 1.0

                p_values.append(p_value)

                # Append results
                results.append({
                    'partner1': genei,
                    'partner2': genej,
                    'shared_partners': ', '.join(map(str, shared_partners)),
                    'shared_partners_count': n,
                    'p-value': p_value,
                })

                pbar.update(1)

# Apply FDR correction for multiple testing
_, adjusted_p_values, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')

# Add adjusted p-values and significance level
for i, result in enumerate(results):
    result['adjusted_p-value'] = adjusted_p_values[i]
    result['significance'] = 'significant' if adjusted_p_values[i] < 0.05 else 'non-significant'

# Convert results to a DataFrame and save to CSV
results_df = pd.DataFrame(results)
results_df.to_csv(results_output_file, index=False)

print(f"Results saved to {results_output_file}")
print(results_df.head())
