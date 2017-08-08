# PMTDS
# Precision Medicine Target-Drug Selection in Cancer

This algorithm uses biological pathways to identify the drug-targets in cancer based on patients genetic profile (Gene Expression (GE), Copy number variation (CNV) and Mutation (MUT).
Input: Cancer patient's GE, CNV and MUT
Background Knowledgebase: Biological Pathways and Drug-Target data
Output : Personalized selection of drug-targets for each patient based on his/her genetic profile.

# Installation

The algorithm is developed in Python 2.7. All the modules/packages required to run this algorithm can be installed using 'pip'. 
For example: In your command line type 
1. python -m pip install 'module name' (For Windows)
2. pip install 'module name' (For MAC)

After installing all the modules, you have to download the script to your project directory which has all the datasets mentioned above and run it. If the patient number is small, then the script can be run on ipython. If the dataset is huge it can be run on any HPC clusters accordingly.

# Input Dataset

The dataset is from small case study.
1. pathway_data: PI3K pathway (From PPI database)
2. patient_data: GE, CNV and MUT data for 3 Pancreatic Adenocarcinoma patients obtained from TCGA.
3. drug_data: Includes all FDA approved drugs from DrugBank database
