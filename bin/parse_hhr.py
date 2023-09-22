"""
Function to parse the hhsuite output and returns the tophit hhsuite dataframe
"""
import os

import pandas as pd


def process_hhsuite_results(out_dir, ev):
    """
    wraps hhparse
    :param out_dir: output directory
    :param ev: evalue threshold
    :return: tophits_df tophit for every gene if it exists
    """

    target_db_dir = os.path.join(out_dir, "hhsuite_target_dir")
    hhresult_file = os.path.join(target_db_dir, "results_your_seq_VS_EnVhog.ffdata")

    tophits_df = hhparse(hhresult_file, ev)  # verbose
    return tophits_df


def hhparse(hhresult_file, ev):
    # Initialize lists to store data
    envhog_list = []
    gene_list = []
    probab_list = []
    evalue_list = []
    score_list = []
    aligned_cols_list = []
    identities_list = []
    similarity_list = []

    # Read the file line by line
    current_gene = "gene"
    with open(hhresult_file, "r") as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith(">"):
                # Extract 'envhog' and 'gene' values from the line
                envhog = lines[i].strip().split(">")[1]
                gene = (
                    lines[i + 3].split()[1] if i + 3 < len(lines) else None
                )  # Assuming gene value is 3 lines after '>'

                if gene != current_gene:  # to only keep tophits
                    # for the next step of the loop, make current_gene
                    current_gene = gene

                    # Add 'envhog' and 'gene' to lists
                    envhog_list.append(envhog)
                    gene_list.append(gene)

                    # Extract data from subsequent lines until the next '>'
                    data = lines[i + 1].split()  # Split the line to extract the data
                    probab = float(data[0].split("=")[1])
                    evalue = float(data[1].split("=")[1])
                    score = float(data[2].split("=")[1])
                    aligned_cols = int(data[3].split("=")[1])
                    identities = float(data[4].split("=")[1].rstrip("%"))
                    similarity = float(data[5].split("=")[1])

                    probab_list.append(probab)
                    evalue_list.append(evalue)
                    score_list.append(score)
                    aligned_cols_list.append(aligned_cols)
                    identities_list.append(identities)
                    similarity_list.append(similarity)

                i += 1  # Move to the next line after the '>'
            else:
                i += 1

    # Create a DataFrame
    tophits_df = pd.DataFrame(
        {
            "envhog": envhog_list,
            "gene_for_envhog_merge": gene_list,
            "hhsuite_Prob": probab_list,
            "hhsuite_evalue": evalue_list,
            "hhsuite_Score": score_list,
            "hhsuite_Aligned_cols": aligned_cols_list,
            "hhsuite_Identities": identities_list,
            "hhsuite_Similarity": similarity_list,
        }
    )

    # only keep evalue < evalue
    tophits_df = tophits_df[tophits_df["hhsuite_evalue"] < float(ev)]

    return tophits_df
