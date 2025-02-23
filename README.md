## Adaptive Chebyshev Graph Neural Network for Cancer Gene Prediction with Multi-Omics Integration

This repository contains the code for our project,  
**"Adaptive Chebyshev Graph Neural Network for Cancer Gene Prediction with Multi-Omics Integration,"**  
submitted to the **13th International Conference on Intelligent Biology and Medicine (ICIBM 2025)**,  
which will take place **August 10-12, 2025, in Columbus, OH, USA**.  

You can learn more about the conference here:  
[ICIBM 2025](https://icibm2025.iaibm.org/)

![Alt text](images/__overview_framework.png)


## Data Source

The dataset is obtained from the following sources:

- **[STRING database](https://string-db.org/cgi/download?sessionId=b7WYyccF6G1p)**  
- **[HIPPIE: Human Integrated Protein-Protein Interaction rEference](https://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/download.php)**  
- **[ConsensusPathDB (CPDB)](http://cpdb.molgen.mpg.de/CPDB)**  

These databases provide curated and integrated protein-protein interaction (PPI) and pathway data for bioinformatics research.


## Setup and Get Started

To set up the environment, first, install the required dependencies by running `pip install -r requirements.txt`. Then, activate your Conda environment with `conda activate gnn` and install PyTorch using `conda install pytorch torchvision torchaudio -c pytorch`. Next, install the necessary Python packages with `pip install pandas py2neo pandas matplotlib scikit-learn tqdm seaborn`. Additionally, install DGL using `conda install -c dglteam dgl`. Before training, download the data from [HIPPIE Database](https://cbdm-01.zdv.uni-mainz.de/~mschaefer/hippie/download.php) and place it in the `data/multiomics_meth/` directory. Finally, to train the model, run the command: `python main.py --model_type ACGNN --net_type CPDB --score_threshold 0.99 --learning_rate 0.001 --num_epochs 200`.

