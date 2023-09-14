#!/usr/bin/env python3

"""
Script to filter cluster_info.tsv.gz keeping only Cluster, best.PhROG.profile, best.PhROG.Annotation, and PhROG.Category columns 

filter_clusters_tsv.py -i cluster_info.tsv.gz -o envhog_clusters_filtered.tsv

"""

import pandas as pd
import numpy as np
import gzip
import argparse
import sys
from argparse import RawTextHelpFormatter



def get_input():
    """
    :return: args
    """
    parser = argparse.ArgumentParser(
        description="filter_clusters_tsv.py.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input_file",
        action="store",
        help="Input tsv.gz file.",
        required=True
    )

    parser.add_argument(
        "-o",
        "--output_file",
        action="store",
        default="",
        help="Output tsv.",
        required=True
    )


    args = parser.parse_args()

    return args


def main():
    args = get_input()

    # Open the gzipped input file and read it using pandas
    with gzip.open(args.input_file, 'rt') as file:
        df = pd.read_csv(file, sep='\t')

    # Select the desired columns
    selected_columns = ['Cluster', 'best.PhROG.profile', 'best.PhROG.Annotation', 'PhROG.Category']
    df_selected = df[selected_columns]

    # Rename the columns
    df_selected = df_selected.rename(columns={
        'Cluster': 'envhog',
        'best.PhROG.profile': 'phrog',
        'best.PhROG.Annotation': 'annot',
        'PhROG.Category': 'category'
    })

    # replace 'phrog_33' with 33
    df_selected['phrog'] = df_selected['phrog'].str.replace('phrog_', '', 1)

    df_selected.fillna('No_PHROG_for_ENVHOG', inplace=True)

    # Save the selected columns to a new TSV file
    df_selected.to_csv(args.output_file, sep='\t', index=False)

    print(f'saved to {args.output_file}')

if __name__ == "__main__":
    main()
