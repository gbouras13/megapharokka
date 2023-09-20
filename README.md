# megapharokka
A fork of Pharokka to handle enVhogs

# Table of Contents

- [megapharokka](#megapharokka)
- [Table of Contents](#table-of-contents)
- [Outline](#outline)
- [Benchmarking](#benchmarking)
- [Installing megapharokka](#installing-megapharokka)
- [Running megapharokka](#running-megapharokka)
- [Database](#database)

# Outline

* Megapharokka will Run MMSeqs2 (default of `--mmseqs2`), PyHMMER (`--pyhmmer`) or HHsuite (`--hhsuite`) against appropriately formatted ENVHOG databases.
* Documentation in [Database](#database).
* I would recommend only using `--mmseqs2`. `--hhsuite` takes too long for large datasets.
* Need to do some testing for optimal `--sensitivity`.
* Gene predictor defaults to `-g pyrodigal-gv`.
* Massive datasets recommended to be run with `--skip_mash`.

# Benchmarking

* All benchmarking was conducted on a Intel® Core™ i7-10700K CPU @ 3.80GHz on a machine running Ubuntu 20.04.6 LTS with `-t 8` threads.
* The 673 crAss-like contig dataset from Yutin et al was used as a test set. Yutin, N., Benler, S., Shmakov, S.A. et al. Analysis of metagenome-assembled viral genomes from the human gut reveals diverse putative CrAss-like phages with unique genomic features. Nat Commun 12, 1044 (2021) https://doi.org/10.1038/s41467-021-21350-w.
* `-g prodigal-gv` was used as gene predictor for all options.
* `megapharokka` = 2.2M ENVHOGs consensus sequences. 
* `pharokka` = 38880 PHROGs.
* By default, `pharokka` uses MMSeqs2 sensitivity of 8.5.
* `--hhsuite` on a small subset took >20 hours, so rule that out as a viable option for metagenomes.

Overall, it is clear that `megapharokka` with `--mmseqs2` oon ENVHOGs is more sensitive than regular `-pharokka` on PHROGs even with `--fast` (pyhmmer). 

| 673 crAss-like genomes from Yutin et al., 2021 | `megapharokka --mmseqs2 --sensitivity 4`| `megapharokka --mmseqs2 --sensitivity 3`  | `pharokka v1.5.0 mmseqs2`| `pharokka v1.5.0 --fast (pyhmmer)` |
|------------------------------------------------|------------------------------|----------------------------------|--------------------|-------------|
| Time (min)                                     | 25.21                       | 16.73                        | 17.43             | 61.73   |
| CDS                                            | 74980                       | 74980                        | 74980              | 74980   |
| Annotated Function CDS                         | 17724                         | 17540                         | 10131              | 16357   |
| Unknown Function CDS                           | 57256                       | 57440                        | 64849              | 58623   |

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

* Note: The inimitable Martin Larralde [@althonos](https://github.com/althonos), the creator and maintainer of these tools at EMBL Heidelberg just made production releases: `pyrodigal` v3 is required to be compatible with `pyrodigal-gv` v0.1.0

```
pip install .
```

# Running megapharokka

* Megapharokka will Run MMSeqs2 (default of `--mmseqs2`) or PyHMMER (`--pyhmmer`) or HHsuite (`--hhsuite`) against appropriately formatted ENVHOG databases.
* `--skip_extra_annotations` will skip tRNAscan-SE, MINced and Aragorn
* `--skip_mash` will skip Mash sketch against INPHARED.
* Run `-m` meta mode (now irrelevant as we are not splitting files but indicate anyway).
* `-s` creates split directories for your contig fastas, gffs and gbks.
* You can also use `--dnaapler` to reorient contigs to begin with the large terminase subunit. Wouldn't recommend unless you know the contigs are complete.

```
threads=8
# mmseqs2
megapharokka.py -i input.fasta -o output_dir -t $threads  -d envhogs_db -g 'prodigal-gv' --mmseqs2 -m -s -f  --skip_extra_annotations
# pyhmmer
megapharokka.py -i input.fasta -o output_dir -t $threads  -d envhogs_db -g 'prodigal-gv' --pyhmmer -m -s -f  --skip_extra_annotations
# hhsuite
megapharokka.py -i input.fasta -o output_dir -t $threads  -d envhogs_db -g 'prodigal-gv' --hhsuite -m -s -f  --skip_extra_annotations
```

# Database

Database directory requires the usual VFDB, CARD and INPHARED files from Pharokka v1.4.0.

You can install this with 

```
install_databases.py -d megapharokka_db
```

It requires ENVHOG database annotation and MMSeqs2 database:

* `envhogs_annot_140923.tsv` for annotation.
* `EnVhog_consensus` MMSeqs2 database with `--mmseqs2`

It optionally takens the ENVHOG database files:

* `enVhogs.h3m` with `--pyhmmer`
* `EnVhog_hmm.ffdata`, `EnVhog_hmm.ffindex`, `EnVhog_a3m.ffdata`, `EnVhog_a3m.ffindex`, `EnVhog_cs219.ffdata`, `EnVhog_cs219.ffindex`, hhsuite database with `--hhsuite`


```
usage: megapharokka.py [-h] [-i INFILE] [-o OUTDIR] [-d DATABASE] [-t THREADS] [-f] [-p PREFIX] [-l LOCUSTAG] [-g GENE_PREDICTOR] [-m] [-s] [-c CODING_TABLE] [-e EVALUE] [--dnaapler] [--hhsuite]
                       [--mmseqs2] [--pyhmmer] [--skip_extra_annotations] [-V] [--citation]

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
                        User specified gene predictor. Use "-g phanotate" or "-g prodigal" or "-g prodigal-gv". 
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
  --hhsuite             Runs hhsuite on EnVhogs.
  --mmseqs2             Runs MMSeqs2 on EnVhogs.
  --pyhmmer             Runs pyhmmer on EnVhogs.
  --skip_extra_annotations
                        Skips tRNAscan-se, MINced and Aragorn.
  -V, --version         Print pharokka Version
  --citation            Print pharokka Citation
```