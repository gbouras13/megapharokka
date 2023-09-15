
import pandas as pd


def hhparse(hhresult_file):
        
    # Initialize lists to store data
    envhog_list = []
    gene_list = []
    probab_list = []
    evalue_list = []
    score_list = []
    aligned_cols_list = []
    identities_list = []
    similarity_list = []
    
    
    # Read the file line by line
    with open(hhresult_file, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith('>'):
                # Extract 'envhog' and 'gene' values from the line
                envhog = lines[i].strip().split('>')[1]
                gene = lines[i + 3].split()[1] if i + 3 < len(lines) else None  # Assuming gene value is 3 lines after '>'
            
                # Add 'envhog' and 'gene' to lists
                envhog_list.append(envhog)
                gene_list.append(gene)
    
                # Extract data from subsequent lines until the next '>'
                data = lines[i + 1].split()  # Split the line to extract the data
                probab = float(data[0].split('=')[1])
                evalue = float(data[1].split('=')[1])
                score = float(data[2].split('=')[1])
                aligned_cols = int(data[3].split('=')[1])
                identities = float(data[4].split('=')[1].rstrip('%'))
                similarity = float(data[5].split('=')[1])
            
                probab_list.append(probab)
                evalue_list.append(evalue)
                score_list.append(score)
                aligned_cols_list.append(aligned_cols)
                identities_list.append(identities)
                similarity_list.append(similarity)
    
                i += 1  # Move to the next line after the '>'
            else:
                i += 1
    
    # Create a DataFrame
    df = pd.DataFrame({
        'envhog': envhog_list,
        'gene': gene_list,
        'Probab': probab_list,
        'E-value': evalue_list,
        'Score': score_list,
        'Aligned_cols': aligned_cols_list,
        'Identities': identities_list,
        'Similarity': similarity_list
    })
    
    # Save the DataFrame to a CSV file
    #df.to_csv('output.csv', index=False)

    print(df)

    return df




# # -*- coding: utf-8 -*-

# """
# This script takes the .hhr files output by HHSuite and
# turns the quite verbose file in to a fully tabulated
# version with all the fields separated one, one line per
# file. Thus, the file can be viewed simply in Excel etc.

# It requires the non-standard pandas module.
# """

# # This program is free software: you can redistribute it and/or
# # modify it under the terms of the GNU General Public License as
# # published by the Free Software Foundation, either version 3 of
# # the License, or (at your option) any later version.

# # This program is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# # GNU General Public License for more details.

# # The license for HHSuite remains with the authors. Please consult
# # their licensce agreements before using this software, and ensure
# # they are cited for any use. Run the script with -b to print rel-
# # evant references.


# import os
# import sys
# import requests
# import argparse
# from io import StringIO
# import pandas as pd

# __author__ = "Joe R. J. Healey"
# __version__ = "1.1.0"
# __title__ = "tabulateHHpred"
# __license__ = "GPLv3"
# __author_email__ = "jrj.healey@gmail.com"

# template = u"""
# ---|------|------------------------|----|-------|-------|------|-----|----|---------|--------------|
#  No Hit    Short Desc               Prob E-value P-value  Score    SS Cols Query HMM  Template HMM
# """


# def hhparse(hhresult_file, verbose):
#     """Convert HHpred's text-based output table in to a pandas dataframe"""
#     pattern = StringIO(template).readlines()[1]
#     colBreaks = [i for i, ch in enumerate(pattern) if ch == "|"]
#     widths = [j - i for i, j in zip(([0] + colBreaks)[:-1], colBreaks)]
#     hhtable = pd.read_fwf(hhresult_file, skiprows=8, nrows=10, header=0, widths=widths)
#     if verbose is True:
#         print(hhtable)

#     top_hit = str(hhtable.loc[0, "Hit"])[0:4]
#     top_hit_full = hhtable.loc[0, "Hit"]
#     top_prob = hhtable.loc[0, "Prob"]
#     top_eval = hhtable.loc[0, "E-value"]
#     top_pval = hhtable.loc[0, "P-value"]
#     top_score = hhtable.loc[0, "Score"]

#     if verbose is True:
#         print("Your best hit: (PDB ID | Probability | E-Value | P-Value | Score)")
#         print("\t".join([top_hit, top_prob, top_eval, top_pval, top_score]))

#     return top_hit, top_hit_full, top_prob, top_eval, top_pval, top_score


# def getFullDesc(hhresult_file, top_hit_full, verbose):
#     with open(hhresult_file, "r") as hrh:
#         for line in hrh:
#             if line.startswith(">" + top_hit_full):
#                 full_desc = line.rstrip("\n")

#     if verbose is True:
#         print(full_desc)

#     return full_desc


# def getDOI(top_hit):
#     """Query the PDB REST API to get an associated DOI/Publication"""
#     # TODO: This function no longer appears to work. The URL may have changed format...
#     #      to be fixed in future.

#     try:
#         query = requests.get(
#             "https://www.ebi.ac.uk/pdbe/api/pdb/entry/publications/" + str(top_hit)
#         )
#         qjson = query.json()
#         doi = qjson[top_hit][0]["doi"]

#         if not doi:
#             doi = "No DOI found."

#     except KeyError:
#         doi = "Key error. ID likely deprecated."

#     return doi


# def displayRefs():
#     """Display relevant references"""
#     print(
#         """
#     - The following publications pertain to HHSuite:
# 	- Alva V., Nam SZ., Söding J., Lupas AN. (2016)
# 	  The MPI bioinformatics Toolkit as an integrative platform for advanced protein sequence and structure analysis.
# 	  Nucleic Acids Res. pii: gkw348. PMID: 27131380

# 	- Remmert M., Biegert A., Hauser A., Söding J. (2011) HHblits: Lightning-fast iterative protein sequence searching by HMM-HMM alignment.
# 	  Nat Methods. 9(2):173-5. doi: 10.1038/nmeth.1818. PMID: 22198341

# 	- Söding J., Biegert A., Lupas AN. (2005) The HHpred interactive server for protein homology detection and structure prediction.
# 	  Nucleic Acids Res 33 (Web Server issue), W244-W248. PMID: 15980461

# 	- Söding J. (2005) Protein homology detection by HMM-HMM comparison.
# 	  Bioinformatics 21: 951-960. PMID: 15531603

# 	- Hildebrand A., Remmert A., Biegert A., Söding J. (2009) Fast and accurate automatic structure prediction with HHpred.
# 	  Proteins 77(Suppl 9):128-32. doi: 10.1002/prot.22499. PMID: 19626712

# 	- Meier A., Söding J. (2015) Automatic Prediction of Protein 3D Structures by Probabilistic Multi-template Homology Modeling.
# 	  PLoS Comput Biol. 11(10):e1004343. doi: 10.1371/journal.pcbi.1004343. PMID: 26496371
# 	"""
#     )
#     sys.exit(1)


# def get_args():
#     """Parse commandline arguments"""

#     try:
#         parser = argparse.ArgumentParser(
#             description="This script converts HHpreds verbose output in to a full table for subsequent analysis."
#         )
#         parser.add_argument(
#             "-i", "--infile", action="store", help="The HHpred output file to parse."
#         )
#         parser.add_argument(
#             "-v",
#             "--verbose",
#             action="store_true",
#             help="Print additional messages to screen. Default behaviour is false, only the result would be printed to screen for piping etc.",
#         )
#         parser.add_argument(
#             "-o",
#             "--outfile",
#             action="store",
#             default="None",
#             help="Output file name to store results in. If none provided, the default will be infile.tsv.",
#         )
#         parser.add_argument(
#             "-b",
#             "--bibliography",
#             action="store_true",
#             help="Display references (cannot be used with any other argument).",
#         )
#         parser.add_argument(
#             "-d",
#             "--doi",
#             action="store_true",
#             help="Try to retrieve relevant publications from PDB RESTful API. Warning, this will significantly slow down the processing of results.",
#         )

#         if len(sys.argv) == 1:
#             parser.print_help(sys.stderr)
#             sys.exit(1)

#     except:
#         print(
#             "An exception occured with argument parsing. Check your provided options."
#         )

#     return parser.parse_args()


# def main():
#     """Make function calls and handle arguments for tabulateHHpred.py"""
#     args = get_args()

#     if args.bibliography is True:
#         displayRefs()

#     verbose = args.verbose
#     hhresult_file = args.infile

#     indir = os.path.dirname(os.path.abspath(hhresult_file))

#     split = os.path.splitext(args.infile)
#     basename = os.path.basename(split[0])

#     if args.outfile is "None":
#         outfile = indir + "/" + basename + ".tsv"
#     else:
#         outfile = args.outfile

#     # Main code begins:

#     top_hit, top_hit_full, top_prob, top_eval, top_pval, top_score = hhparse(
#         hhresult_file, verbose
#     )
#     full_desc = getFullDesc(hhresult_file, top_hit_full, verbose)

#     row = (
#         "\t".join(
#             [
#                 basename,
#                 top_hit,
#                 top_hit_full,
#                 str(top_prob),
#                 str(top_eval),
#                 str(top_pval),
#                 str(top_score),
#                 full_desc,
#             ]
#         )
#         + "\n"
#     )

#     if args.doi is True:
#         doi = getDOI(top_hit)
#         row = row.rstrip("\n") + "\t" + doi + "\n"

#     with open(outfile, "w") as ofh:
#         ofh.write(row)
#         print(row)


# if __name__ == "__main__":
#     main()