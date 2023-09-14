# megapharokka
A fork of Pharokka to handle enVhogs

# Table of Contents

- [megapharokka](#megapharokka)
- [Table of Contents](#table-of-contents)
- [Creation of enVhog HMM profile Databases for use with pyhmmer](#creation-of-envhog-hmm-profile-databases-for-use-with-pyhmmer)
- [Installing megapharokka](#installing-megapharokka)
- [Running megapharokka](#running-megapharokka)
- [Database](#database)


# Creation of enVhog HMM profile Databases for use with pyhmmer

See `scripts/notes.sh`

1. Download and untar the tarball (ends up about 60GB).
2. Extract the a3m files from hhsuite formatted files
3. Convert s3m to FASTA MSA
4. Rename MSA to match metadata and remove consensus sequence
5. Create HMMs with pyHMMER `create_custom_hmm.py` from Pharokka v1.4
6. Create the filtered tsv with `filter_clusters_tsv.py`
7. 

# Installing megapharokka

1. Clone 

```
git clone https://github.com/gbouras13/megapharokka
cd megapharokka
```

2. Create conda env with external dependencies installed

```
mamba env  create -f environment.yml 
conda activate megapharokka_env
```

3. Install `megapharokka` and most python dependecies with `pip`

```
pip install .
```

4. Install `pyrodigal` v3 and `pyrodigal-gv` pre-releases

* Martin Larralde the creator and maintainer of these tools at EMBL Heidelberg has not yet made production releases. `pyrodigal` v3 is required to be compatible with `pyrodigal-gv` (essentially he made it in response to an issue in and for Pharokka).
* When he releases it I will update.

```
pip install -U --pre pyrodigal
pip install -U --pre pyrodigal-gv
```

# Running megapharokka

* `-m` meta mode
* `-s` creates split directories for your contig fastas, gffs and gbks
* You can also use `--dnaapler` to reorient contigs to begin with the large terminase subunit. Wouldn't recommend unless you know the contigs are complete.

```
threads=8
megapharokka.py -i input.fasta -o output_dir -t $threads  -d envhogs_db -g 'prodigal-gv' -m -s -f 
```

# Database

Database directory required the usual VFDB, CARD and INPHARED files from Pharokka v1.4.0.

It also requires `enVhogs.h3m` and `envhogs_annot_140923.tsv`.

It can also work on an enVhogs.h3m file that is a subset of all enVhogs.



```
usage: megapharokka.py [-h] [-i INFILE] [-o OUTDIR] [-d DATABASE] [-t THREADS] [-f] [-p PREFIX] [-l LOCUSTAG] [-g GENE_PREDICTOR] [-m] [-s]
                       [-c CODING_TABLE] [-e EVALUE] [--dnaapler] [-V] [--citation]

megapharokka: fast phage annotation program with enVhogs

options:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        Input genome file in fasta format.
  -o OUTDIR, --outdir OUTDIR
                        Directory to write the output to.
  -d DATABASE, --database DATABASE
                        Database directory. If the databases have been installed in the default directory, this is not required. Otherwise specify the path.
  -t THREADS, --threads THREADS
                        Number of threads. Defaults to 1.
  -f, --force           Overwrites the output directory.
  -p PREFIX, --prefix PREFIX
                        Prefix for output files. This is not required.
  -l LOCUSTAG, --locustag LOCUSTAG
                        User specified locus tag for the gff/gbk files. This is not required. A random locus tag will be generated instead.
  -g GENE_PREDICTOR, --gene_predictor GENE_PREDICTOR
                        User specified gene predictor. Use "-g phanotate" or "-g prodigal". 
                        Defaults to phanotate (not required unless prodigal is desired).
  -m, --meta            meta mode for metavirome input samples
  -s, --split           split mode for metavirome samples. -m must also be specified. 
                        Will output separate split FASTA, gff and genbank files for each input contig.
  -c CODING_TABLE, --coding_table CODING_TABLE
                        translation table for prodigal. Defaults to 11. Experimental only.
  -e EVALUE, --evalue EVALUE
                        E-value threshold for MMseqs2 database PHROGs, VFDB and CARD and PyHMMER PHROGs database search. Defaults to 1E-05.
  --dnaapler            Runs dnaapler to automatically re-orient all contigs to begin with terminase large subunit if found. 
                        Recommended over using '--terminase'.
  -V, --version         Print pharokka Version
  --citation            Print pharokka Citation
```