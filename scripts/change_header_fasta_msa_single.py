#!/usr/bin/env python3

"""
Script to append header to fasta msa based on a3m and remove consensus sequence

change_header_fasta_msas.py -a <a3ms msa file> -m <FASTA msa file> -o < output FASTA msa file> -c < outoput consensus file>

"""

import os
import shutil
import argparse
import os
import sys
from argparse import RawTextHelpFormatter
from loguru import logger
from Bio import SeqIO

def get_input():
    """gets input for create_custom_hmm.py
    :return: args
    """
    parser = argparse.ArgumentParser(
        description="create_custom_hmm.py: Creates HMMs from FASTA formatted MSAs with PyHMMER for use with Pharokka v1.4.0 and higher.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--a3file",
        action="store",
        help="Input a3m file.",
        required=True
    )

    parser.add_argument(
        "-o",
        "--outdir",
        action="store",
        default="",
        help="Output FASTA MSAs dir.",
        required=True
    )

    parser.add_argument(
        "-m",
        "--msafile",
        action="store",
        default="",
        help="Input  FASTA MSA file.",
        required=True
    )

    parser.add_argument(
        "-c",
        "--consdir",
        action="store",
        default="",
        help="Output directory to store consensus FASTA file.",
        required=True
    )


    parser.add_argument(
        "-f", "--force", help="Overwrites the output files.", action="store_true"
    )

    args = parser.parse_args()

    return args


def main():
    args = get_input()

    logger.add(lambda _: sys.exit(1), level="ERROR")

    a3m_file = args.a3file
    MSA_file = args.msafile
    cons_dir = args.consdir
    out_dir = args.outdir

    #### force


    # Check if the directory already exists and make the dir
    if not os.path.exists(out_dir):
        # Create the output directory
        os.mkdir(out_dir)

    logger.info(
        f"Creating MSAs in the file {out_dir} from MSAs in {MSA_file}."
    )


    # Check if the directory already exists and make the dir
    if not os.path.exists(cons_dir):
        # Create the output directory
        os.mkdir(cons_dir)

    logger.info(
        f"Creating consensus sequences in the directory {cons_dir} from a3ms in the directory {cons_dir}."
    )

    ###### get header
    # removes .fas
    a3m_name = os.path.basename(a3m_file)

    # read in the header from a3m
    with open(a3m_file, "r") as f:
        lines = f.read().splitlines() 
        # get name and trim off the #
        header = lines[0][1:]
    f.close()

    # checout output exists

    cons_fasta = f"{cons_dir}/{header}.fasta"
    out_fasta = f"{out_dir}/{header}.fasta"

    if args.force == True:
        if os.path.isdir(out_fasta) == True:
            logger.info(
                f"Removing output file {out_fasta} as -f or --force was specified."
            )
            shutil.rmtree(out_fasta)
        elif os.path.isfile(out_fasta) == True:
            logger.info(
                f"Removing output file {out_fasta} as -f or --force was specified."
            )
            os.remove(out_fasta)
        else:
            logger.info(
                f"--force was specified even though the output file {out_fasta} does not already exist. Continuing."
            )
    else:
        if os.path.isdir(out_fasta) == True or os.path.isfile(out_fasta) == True:
            logger.error(
                f"The output file {out_fasta} already exists and force was not specified. Please specify -f or --force to overwrite it."
            )


    if args.force == True:
        if os.path.isdir(cons_fasta) == True:
            logger.info(
                f"Removing output file {cons_fasta} as -f or --force was specified."
            )
            shutil.rmtree(cons_fasta)
        elif os.path.isfile(cons_fasta) == True:
            logger.info(
                f"Removing output file {cons_fasta} as -f or --force was specified."
            )
            os.remove(cons_fasta)
        else:
            logger.info(
                f"--force was specified even though the output file {cons_fasta} does not already exist. Continuing."
            )
    else:
        if os.path.isdir(cons_fasta) == True or os.path.isfile(cons_fasta) == True:
            logger.error(
                f"The output file {cons_fasta} already exists and force was not specified. Please specify -f or --force to overwrite it."
            )


    # final

    # get records
    fasta_records = []

    # Open and read the FASTA file and save records
    with open(MSA_file, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            fasta_records.append(record)

    # Write all records except the first one to the output FASTA file
    with open(out_fasta, "w") as output_handle:
        SeqIO.write(fasta_records[1:], output_handle, "fasta")

    # Write  the first one to the consensus FASTA file
    with open(cons_fasta, "w") as output_handle:
        SeqIO.write(fasta_records[0], output_handle, "fasta")


if __name__ == "__main__":
    main()
