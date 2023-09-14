# megapharokka
A fork of Pharokka to handle enVhogs

# Creation of enVhog hmm profile for use with pyhmmer

See `scripts/notes.sh`


1. Download and untar the tarball
2. Extract the a3m files from hhsuite formatted files
3. Convert s3m to FASTA MSA
4. Rename MSA to match metadata and remove consensus sequence
5. Create HMMs with pyHMMER `create_custom_hmm.py` from Pharokka v1.4



