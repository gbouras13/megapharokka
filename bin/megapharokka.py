#!/usr/bin/env python3

import os
import shutil
import sys
import time
from pathlib import Path
from databases import check_db_installation
from hmm import run_pyhmmer_envhogs
from input_commands import (check_dependencies, get_input, instantiate_dirs,
                            instantiate_split_output,
                            validate_fasta, validate_gene_predictor,
                            validate_meta, 
                            validate_threads)
from loguru import logger
from post_processing import Pharok, remove_post_processing_files
from processes import (concat_phanotate_meta, concat_trnascan_meta,
                       convert_gff_to_gbk, run_aragorn,
                       run_dnaapler, run_mash_dist, run_mash_sketch,
                       run_minced, run_mmseqs, run_phanotate,
                       run_phanotate_fasta_meta, run_phanotate_txt_meta,
                       run_pyrodigal, run_pyrodigal_gv, run_trna_scan,
                       run_trnascan_meta, split_input_fasta, translate_fastas)
from util import count_contigs, get_version
from run_hhsuite import run_hhindex_hhblits


def main():
    # get the args
    args = get_input()

    logger.add(lambda _: sys.exit(1), level="ERROR")

    if args.citation == True:
        logger.info("If you use Pharokka in your research, please cite:")
        logger.info(
            "George Bouras, Roshan Nepal, Ghais Houtak, Alkis James Psaltis, Peter-John Wormald, Sarah Vreugde."
        )
        logger.info("Pharokka: a fast scalable bacteriophage annotation tool.")
        logger.info("Bioinformatics, Volume 39, Issue 1, January 2023, btac776.")
        logger.info("https://doi.org/10.1093/bioinformatics/btac776.")
        logger.info(
            "You should also cite the full list of tools Pharokka uses, which can be found at https://github.com/gbouras13/pharokka#citation."
        )
        sys.exit()

    # set the prefix
    if args.prefix == "Default":
        prefix = "pharokka"
    else:
        prefix = args.prefix

    # set the locustag flag for locustag generation
    if args.locustag == "Default":
        locustag = "Random"
    else:
        locustag = args.locustag

    # set the gene_predictor
    gene_predictor = args.gene_predictor

    # instantiate outdir
    out_dir = instantiate_dirs(args.outdir, args.meta, args.force)

    # set log dir
    logdir = Path(f"{out_dir}/logs")

    # set the db dir
    if args.database == "Default":
        db_dir = os.path.join(os.path.realpath(__file__), "../", "databases/")
    else:
        db_dir = args.database

    # get start time
    start_time = time.time()
    # initial logging stuff
    log_file = os.path.join(args.outdir, f"pharokka_{start_time}.log")
    # adds log file
    logger.add(log_file)

    # preamble
    logger.info(f"Starting Megapharokka v{get_version()}")
    logger.info("Command executed: {}", args)
    logger.info("Repository homepage is https://github.com/gbouras13/megapharokka")
    logger.info("Written by George Bouras: george.bouras@adelaide.edu.au")

    logger.info(f"Checking database installation in {db_dir}.")
    database_installed = check_db_installation(db_dir)
    if database_installed == True:
        logger.info("All databases have been successfully checked.")
    else:
        logger.error(
            "The database directory was unsuccessfully checked. Please install the databases."
        )


    # dependencies
    logger.info("Checking dependencies.")
    # output versions
    (
        phanotate_version,
        pyrodigal_version,
        pyrodigal_gv_version,
        trna_version,
        aragorn_version,
        minced_version,
    ) = check_dependencies()

    # instantiation/checking fasta and gene_predictor
    validate_fasta(args.infile)
    input_fasta = args.infile

    # other validations
    validate_gene_predictor(gene_predictor, False) # genbank false
    validate_threads(args.threads)

    ###################
    # define input
    ###################

    # reorient with dnaapler if chosen
    if args.dnaapler is True:
        logger.info(
            "You have chosen to reorient your contigs by specifying --dnaapler. Checking the input."
        )


        # count contigs
        contig_count = count_contigs(input_fasta)

        # runs dnaapler
        dnaapler_success = run_dnaapler(
            input_fasta, contig_count, out_dir, args.threads, logdir
        )

        if dnaapler_success == True:
            if contig_count == 1:
                input_fasta = os.path.join(
                    out_dir, "dnaapler/dnaapler_reoriented.fasta"
                )
            elif contig_count > 1:  # dnaapler all
                input_fasta = os.path.join(
                    out_dir, "dnaapler/dnaapler_all_reoriented.fasta"
                )
            destination_file = os.path.join(
                out_dir, f"{prefix}_dnaapler_reoriented.fasta"
            )
            # copy FASTA to output
            shutil.copy(input_fasta, destination_file)


    ########
    # mmseqs2 and hmm decisions
    ########


    # by default run both not in meta mode
    hmm_flag = True

    # validates meta mode
    validate_meta(input_fasta, args.meta, args.split, False) # genbank is False

    # meta mode split input for trnascan and maybe phanotate
    if args.meta == True:
        num_fastas = split_input_fasta(input_fasta, out_dir)
        # will generate split output gffs if split flag is true
        instantiate_split_output(out_dir, args.split)

    # CDS predicton
    # phanotate
    if gene_predictor == "phanotate":
        logger.info("Running Phanotate.")
        if args.meta == True:
            logger.info("Applying meta mode.")
            run_phanotate_fasta_meta(input_fasta, out_dir, args.threads, num_fastas)
            run_phanotate_txt_meta(input_fasta, out_dir, args.threads, num_fastas)
            concat_phanotate_meta(out_dir, num_fastas)
        else:
            run_phanotate(input_fasta, out_dir, logdir)
    elif gene_predictor == "prodigal":
        logger.info("Implementing Prodigal using Pyrodigal.")
        run_pyrodigal(input_fasta, out_dir, args.meta, args.coding_table, int(args.threads))
    elif gene_predictor == "genbank":
        logger.info("Extracting CDS information from your genbank file.")
    elif gene_predictor == "prodigal-gv":
        logger.info("Implementing Prodigal-gv using Pyrodigal-gv.")
        run_pyrodigal_gv(input_fasta, out_dir, int(args.threads))

    # translate fastas (parse genbank)
    translate_fastas(out_dir, gene_predictor, args.coding_table, args.infile)

    # run trna-scan meta mode if required
    if args.meta == True:
        logger.info("Starting tRNA-scanSE. Applying meta mode.")
        run_trnascan_meta(input_fasta, out_dir, args.threads, num_fastas)
        concat_trnascan_meta(out_dir, num_fastas)
    else:
        logger.info("Starting tRNA-scanSE.")
        run_trna_scan(input_fasta, args.threads, out_dir, logdir)
    # run minced and aragorn
    run_minced(input_fasta, out_dir, prefix, logdir)
    run_aragorn(input_fasta, out_dir, prefix, logdir)

    # running mmseqs2 on the 2 CARD and VFDB
    # run_mmseqs(
    #     db_dir,
    #     out_dir,
    #     args.threads,
    #     logdir,
    #     gene_predictor,
    #     args.evalue,
    #     db_name="CARD",
    # )
    # run_mmseqs(
    #     db_dir,
    #     out_dir,
    #     args.threads,
    #     logdir,
    #     gene_predictor,
    #     args.evalue,
    #     db_name="VFDB",
    # )

    # runs pyhmmer on enVhogsROGs
    # logger.info("Running PyHMMER on EnVhogs.")
    # best_results_pyhmmer = run_pyhmmer_envhogs(
    #     db_dir, out_dir, args.threads, gene_predictor, args.evalue
    # )
    logger.info("Running hhsuite on EnVhogs.")

    run_hhindex_hhblits(out_dir, gene_predictor, db_dir, args.threads, logdir)


    #################################################
    # post processing
    #################################################

    logger.info("Post Processing Output.")

    # instanatiate the class with some of the params
    pharok = Pharok()
    pharok.out_dir = out_dir
    pharok.db_dir = db_dir
    pharok.gene_predictor = gene_predictor
    pharok.prefix = prefix
    pharok.locustag = locustag
    pharok.input_fasta = input_fasta
    pharok.meta_mode = args.meta
    pharok.coding_table = args.coding_table
    pharok.phanotate_version = phanotate_version
    pharok.pyrodigal_version = pyrodigal_version
    pharok.pyrodigal_gv_version = pyrodigal_gv_version
    pharok.trna_version = trna_version
    pharok.aragorn_version = aragorn_version
    pharok.minced_version = minced_version
    pharok.pyhmmer_results_dict = best_results_pyhmmer

    #####################################
    # post processing
    #####################################

    # gets df of length and gc for each contig
    pharok.get_contig_name_lengths()

    # post process results
    # includes vfdb and card
    # adds the merged df, vfdb and card top hits dfs to the class objec
    # no need to specify params as they are in the class :)
    pharok.process_results()

    # parse the aragorn output
    # get flag whether there is a tmrna from aragor
    pharok.parse_aragorn()

    # create gff and save locustag to class for table
    pharok.create_gff()

    # create table
    pharok.create_tbl()

    # output single gffs in meta mode
    if args.split == True and args.meta == True:
        # create gffs for each contig
        pharok.create_gff_singles()
        # converts each gff to gbk
        pharok.convert_singles_gff_to_gbk()
        # splits the input fasta into single fastas
        pharok.split_fasta_singles()

    # create and write vfdb and card tophits
    # needs to be before .create_txt or else won't count properly
    # will only write to file if mmseqs2 has been run (in function)

    pharok.write_tophits_vfdb_card()

    # write the summary tsv outputs and functions
    pharok.create_txt()

    # convert to genbank
    logger.info("Converting gff to genbank.")
    # not part of the class so from processes.py
    convert_gff_to_gbk(input_fasta, out_dir, out_dir, prefix, pharok.prot_seq_df)

    # update fasta headers and final output tsv
    pharok.update_fasta_headers()
    pharok.update_final_output()

    # extract terL
    pharok.extract_terl()

    # run mash
    logger.info("Finding the closest match for each contig in INPHARED using mash.")
    # in process.py
    run_mash_sketch(input_fasta, out_dir, logdir)
    run_mash_dist(out_dir, db_dir, logdir)
    # part of the class
    pharok.inphared_top_hits()

    # delete tmp files
    # remove_post_processing_files(out_dir, gene_predictor, args.meta)

    # Determine elapsed time
    elapsed_time = time.time() - start_time
    elapsed_time = round(elapsed_time, 2)

    # Show elapsed time for the process
    logger.info("Megapharokka has finished.")
    logger.info(f"Elapsed time: {elapsed_time} seconds")

    logger.info("If you use Pharokka in your research, please cite:")
    logger.info(
        "George Bouras, Roshan Nepal, Ghais Houtak, Alkis James Psaltis, Peter-John Wormald, Sarah Vreugde."
    )
    logger.info("Pharokka: a fast scalable bacteriophage annotation tool.")
    logger.info("Bioinformatics, Volume 39, Issue 1, January 2023, btac776.")
    logger.info("https://doi.org/10.1093/bioinformatics/btac776.")
    logger.info(
        "You should also cite the full list of tools Pharokka uses, which can be found at https://github.com/gbouras13/pharokka#citation."
    )


if __name__ == "__main__":
    main()
