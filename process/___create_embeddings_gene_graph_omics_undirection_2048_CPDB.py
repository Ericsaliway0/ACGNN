import csv
import json
import os

# File paths
source_csv_path = 'data/multiomics_meth/omics_ppi_embeddings_2048.csv'
target_csv_path = 'data/multiomics_meth/omics_ppi_embeddings_2048.csv'
relation_csv_path = 'data/CPDB_ppi_0.99_with_gene_type_and_connected_driver_gene.csv'
output_json_path = 'data/multiomics_meth/omics_ppi_embeddings_2048.json'
csv_file_path = 'data/multiomics_meth/omics_ppi_embeddings_2048.csv'

# Interaction types and corresponding labels
interaction_labels = {
    "0": 0,  # Label 0
    "1": 1,  # Label 1
    "2": -1,  # Label 2
    "3": -1   # Label 3
}

# Ensure interaction stats CSV exists with a header
if not os.path.isfile(csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['num_nodes', 'num_edges']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

# Function to read embeddings from a CSV file
def read_embeddings(file_path):
    embeddings = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header
        for row in reader:
            name = row[0]
            embedding = list(map(float, row[1:]))
            print(embedding)
            embeddings[name] = embedding
    return embeddings

# Read source and target embeddings
source_embeddings = read_embeddings(source_csv_path)
target_embeddings = read_embeddings(target_csv_path)

# Read relationships and count nodes and edges
nodes = set()
edges = set()  # Use a set to track unique edges
relationships_to_include = []

with open(relation_csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        source_stId = row['partner1']
        target_stId = row['partner2']
        relation_type = row['gene_type']
        
        if relation_type in interaction_labels:
            nodes.add(source_stId)
            nodes.add(target_stId)

            edge = tuple(sorted([source_stId, target_stId]))  # Store edges in sorted order to make them undirected
            if edge not in edges:
                edges.add(edge)
                relationships_to_include.append((source_stId, target_stId, relation_type))
                relationships_to_include.append((target_stId, source_stId, relation_type))  # Add reversed edge

# Print node and edge counts
print(f"Number of nodes: {len(nodes)}")
print(f"Number of edges: {len(edges)}")

# Create the JSON structure
relationships = []
for source_stId, target_stId, relation_type in relationships_to_include:
    if source_stId in source_embeddings and target_stId in target_embeddings:
        source_label = interaction_labels[relation_type]  # Assign label based on type
        target_label = 1 if relation_type == "2" else 0 if relation_type == "0" else None

        relationship = {
            "source": {
                "properties": {
                    "name": source_stId,
                    "label": source_label,
                    "embedding": source_embeddings[source_stId]
                }
            },
            "relation": {
                "type": relation_type
            },
            "target": {
                "properties": {
                    "name": target_stId,
                    "label": target_label,
                    "embedding": target_embeddings[target_stId]
                }
            }
        }
        relationships.append(relationship)

# Save to JSON file
with open(output_json_path, 'w') as json_file:
    json.dump(relationships, json_file, indent=2)

print(f"JSON file saved to {output_json_path}")

# Save node and edge counts to CSV file
with open(csv_file_path, 'a', newline='') as csvfile:
    fieldnames = ['num_nodes', 'num_edges']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writerow({
        'num_nodes': len(nodes),
        'num_edges': len(edges)
    })

print(f"CSV file updated with node and edge counts.")
