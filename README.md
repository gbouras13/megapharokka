# megapharokka
A fork of Pharokka to handle enVhogs

# Creation of enVhog hmm profile for use with pyhmmer

See `scripts/notes.sh`

1. Download and untar the tarball
2. Extract the a3m files from hhsuite formatted files
3. Convert s3m to FASTA MSA
4. Rename MSA to match metadata and remove consensus sequence
5. Create HMMs with pyHMMER `create_custom_hmm.py` from Pharokka v1.4


# Installing megapharokka

1. Clone 

```
git clone https://github.com/gbouras13/megapharokka
cd megapharokka
```

2. Create conda env with external dependencies

```
mamba env  create -f environment.yml 
conda activate pharokka_env
```

3. Install with `pip`

```
pip install .
```

4. Install `pyrodigal` v3 and `pyrodigal-gv` pre-release

* Martin Larralde has not yet made production releases to be compatible with `pyrodigal-gv`

```
pip install -U --pre pyrodigal
pip install -U --pre pyrodigal-gv
```

5. Run megapharokka

```
megapharokka.py
```