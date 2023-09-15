"""
to tar DBs
export GZIP=-9
tar cvzf pharokka_v1.4.0_databases.tar.gz pharokka_v1.4.0_databases

to create the mmseqs2 databases (CARD)
with the latest download v 3.2.7 on August 21
mmseqs createdb protein_fasta_protein_homolog_model.fasta CARD

# also need aro.tsv for this one

# for VFDB, only need the FASTA

# VFDB update as of August 18 2023 (not versioned)
# clustered 

mmseqs easy-cluster VFDB_setB_pro_form.fas VFDBclusterRes tmp --min-seq-id 0.5 -c 0.8 --cov-mode 1
mmseqs createdb VFDBclusterRes_rep_seq.fasta vfdb

"""

#!/usr/bin/env python3
import hashlib
import os
import shutil
import tarfile
from pathlib import Path

import requests
from alive_progress import alive_bar
from loguru import logger
from post_processing import remove_directory

# to hold information about the different DBs


#ENVHOG_NAMES = ["enVhogs.h3m", "envhogs_annot_140923.tsv"]
ENVHOG_NAMES = ["EnVhog_hhm.ffdata", "EnVhog_hhm.ffindex",
                "EnVhog_a3m.ffdata", "EnVhog_a3m.ffindex",
                "EnVhog_cs219.ffdata", "EnVhog_cs219.ffindex"]


VFDB_DB_NAMES = [
    "vfdb",
    "vfdb.dbtype",
    "vfdb.index",
    "vfdb.lookup",
    "vfdb.source",
    "vfdb_h",
    "vfdb_h.dbtype",
    "vfdb_h.index",
    "VFDBclusterRes_cluster.tsv",
    "VFDBclusterRes_rep_seq.fasta",
]

CARD_DB_NAMES = [
    "CARD",
    "CARD.dbtype",
    "CARD.index",
    "CARD.lookup",
    "CARD.source",
    "CARD_h",
    "CARD_h.dbtype",
    "CARD_h.index",
]

INPHARED_NAMES = [
    "1Aug2023_genomes.fa.msh",
    "1Aug2023_data.tsv"
]


def instantiate_install(db_dir):
    instantiate_dir(db_dir)
    # check the database is installed
    logger.info(f"Checking Megapharokka database installation in {db_dir}.")
    downloaded_flag = check_db_installation(db_dir)




def instantiate_dir(db_dir):
    if os.path.isdir(db_dir) == False:
        os.mkdir(db_dir)


def check_db_installation(db_dir):
    downloaded_flag = True
    # ENVHOG files
    for file_name in ENVHOG_NAMES:
        path = os.path.join(db_dir, file_name)
        if os.path.isfile(path) == False:
            logger.info(f"ENVHOGs Database file {path} is missing.")
            downloaded_flag = False
            break
    # VFDB
    for file_name in VFDB_DB_NAMES:
        path = os.path.join(db_dir, file_name)
        if os.path.isfile(path) == False:
            logger.info(f"VFDB Database file {path} is missing.")
            downloaded_flag = False
            break
    # CARD
    for file_name in CARD_DB_NAMES:
        path = os.path.join(db_dir, file_name)
        if os.path.isfile(path) == False:
            logger.info(f"CARD Databases file {path} is missing.")
            downloaded_flag = False
            break
    # annot.tsv
    path = os.path.join(db_dir, "phrog_annot_v4.tsv")
    if os.path.isfile(path) == False:
        logger.info("PHROGs Annotation File is missing.")
        downloaded_flag = False

    # mash files
    for file_name in INPHARED_NAMES:
        path = os.path.join(db_dir, file_name)
        if os.path.isfile(path) == False:
            logger.info("INPHARED File is missing.")
            downloaded_flag = False

    return downloaded_flag
