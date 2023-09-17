import os
from external_tools import ExternalTool
from loguru import logger



def run_hhindex_hhblits(out_dir, gene_predictor,db_dir, threads, evalue, logdir):
    """
    Gets CDS using pyrodigal_gv
    :param filepath_in: input filepath
    :param out_dir: output directory
    :param threads: int
    :return:
    """
    
    # define the amino acid FASTA
    amino_acid_fasta_name = gene_predictor + "_aas_tmp.fasta"
    amino_acid_fasta_file = os.path.join(out_dir, amino_acid_fasta_name)


    # define target db
    target_db_dir = os.path.join(out_dir, "hhsuite_target_dir")
    tsv_prefix = os.path.join(target_db_dir, 'hhsuite_tsv_file.ff') 

    logger.info("Making target hhsuite db")
    # make dir for target db
    if os.path.isdir(target_db_dir) == False:
         os.mkdir(target_db_dir)




     # indexes the file 
     #can't pass curly brackets to subprocess so need to run using os

    combined_index_data = ''.join((tsv_prefix, 'data'))
    combined_index_index = ''.join((tsv_prefix, 'index'))


    ffindex_from_fasta = ExternalTool(
        tool="ffindex_from_fasta",
        input="",
        output="",
        params=f" -s {combined_index_data} {combined_index_index} {amino_acid_fasta_file} ",
        logdir=logdir,
        outfile="",
    )

    try:
        ExternalTool.run_tool(ffindex_from_fasta)
    except:
        logger.error("Error with ffindex_from_fasta")
        return 0

    ### hhblits

    tsv_file = os.path.join(target_db_dir, 'hhsuite_tsv_file')
    db = os.path.join(db_dir, "EnVhog")
    results_targets = os.path.join(target_db_dir, "results_your_seq_VS_EnVhog")
    results_tsv = os.path.join(target_db_dir, "results_tsv_file")

    logger.info("Running hhblits")

    hhblits = ExternalTool(
        tool="hhblits_omp",
        input="",
        output="",
        params=f" -i  {tsv_file} -d {db} -cpu {threads} -M first -n 1 -o {results_targets} -blasttab {results_tsv} -e {evalue} ",
        logdir=logdir,
        outfile="",
    )

    try:
        ExternalTool.run_tool(hhblits)
    except:
        logger.error("Error with hhblits")
        return 0


