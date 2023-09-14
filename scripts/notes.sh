#### 

scripts_dir="megapharokka/scripts"

# 1. download the EnVhog.tar.gz

wget "envhog.u-ga.fr/envhog/EnVhog_HMMs/EnVhog.tar.gz"

# 2. untar the enVhogs
tar -xzf EnVhog.tar.gz

# 3. convert the hhsuite format to get a3m files

# install hhsuite
# mamba create -n hhsuite hhsuite
conda activate hhsuite

# get a3m files using ffindex_unpack
mkdir -p a3ms
ffindex_unpack envhog_hmm/EnVhog_a3m.ffdata  envhog_hmm/EnVhog_a3m.ffindex  a3ms/ .

# 4. reformat the a3ms to FASTA MSAs - taken from hhsuite
# Source directory containing the input files
input_dir="a3ms"

# Destination directory for the output files
output_dir="fasta_msas"
mkdir -p $output_dir

# Loop through all files in the input directory with a3m extension
# allows for multithreaded use

# Function to process a single file
process_file() {
    input_file="$1"
    base_name=$(basename "$input_file" .a3m)
    output_file="$output_dir/$base_name.fas"
    $scripts_dir/reformat.pl a3m fas "$input_file" "$output_file"
    
    echo "Processed: $input_file -> $output_file"
}

# Loop through all files in the input directory with a3m extension and process them concurrently
for input_file in "$input_dir"/*; do
    process_file "$input_file" &
done




# 5. rename the FASTA MSAs with the matching header as the metadata, and remove consensus sequence

# get deps from pharokka
#mamba create -n pharokka1.4.1 pharokka==1.4.1
conda activate pharokka1.4.1


# Source directory containing the input files
a3m_dir="a3ms"
msa_dir="fasta_msas"

fasta_msas_with_header_dir="fasta_msas_with_header"
consensus_fasta_dir="consensus_fastas"

# Function to process a single file
process_file() {
    msa_file="$1"
    base_name=$(basename "$msa_file" .fas)
    a3m_file="$a3m_dir/$base_name"

    python $scripts_dir/change_header_fasta_msa_single.py -a "$a3m_file" -m "$msa_file" -o $fasta_msas_with_header_dir -c $consensus_fasta_dir
    echo "Processed: $base_name "
}

# Loop through all files in the input directory with a3m extension and process them concurrently
for input_file in "$msa_dir"/*.fas; do
    process_file "$input_file" &
done

# find -type f -name '*' | wc -l

# 6. convert to hmms for pyhmmer
create_custom_hmm.py -i fasta_msas_with_header -o pyhmmer_hmms -p enVhogs

# resulting db file will be `pyhmmer_hmms/enVhogs.h3m`

# 7. Create envhogs_annot_140923.tsv from cluster_info.tsv.gz

$scripts_dir/filter_clusters_tsv.py -i cluster_info.tsv.gz -o envhogs_db/envhogs_annot_140923.tsv