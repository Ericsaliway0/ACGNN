# Adaptive Chebyshev Graph Neural Network for Cancer Gene Prediction with Multi-Omics Integration

This repository contains the code for our paper, "Adaptive Chebyshev Graph Neural Network for Cancer Gene Prediction with Multi-Omics Integration," accepted for presentation at the IEEE International Conference on Bioinformatics & Biomedicine (BIBM) 2024, held from December 3-6, 2024, in Lisbon, Portugal.

![Alt text](images/__overview_framework.png)


## Data 
Download the data from the link below and put it the data/multiomics_meth/ before training:

-) https://drive.google.com/file/d/1l7mbTn2Nxsbc7LLLJzsT8y02scD23aWo/view?usp=sharing

## Setup

-) conda create -n gnn python=3.11 -y

-) conda activate gnn 

-) conda install pytorch::pytorch torchvision torchaudio -c pytorch

-) pip install pandas

-) pip install py2neo pandas matplotlib scikit-learn

-) pip install tqdm

-) conda install -c dglteam dgl

-) pip install seaborn

##
pip install -r requirements.txt

-) conda activate gnn 

-) conda install pytorch::pytorch torchvision torchaudio -c pytorch

-) pip install pandas

-) pip install py2neo pandas matplotlib scikit-learn

-) pip install tqdm

-) conda install -c dglteam dgl

-) pip install seaborn

## Get start
python main.py --model_type ACGNN --net_type CPDB --score_threshold 0.99 --learning_rate 0.001 --num_epochs 200
   

