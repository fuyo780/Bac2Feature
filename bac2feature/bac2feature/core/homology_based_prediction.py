### library ###
from os.path import join
import subprocess

import pandas as pd

import bac2feature.core.default as default

### main func ###
def predict_by_homology(
    input_fasta:str, out_trait:str, intermediate_dir:str,
    ref_blastdb=default.ref_blastdb,
    ref_trait=default.ref_trait, perc_identity=None, threads=1) -> None:
    """Predict microbial traits from fasta file by homology search."""
    blast_result_path = join(intermediate_dir, 'bla_result.outfmt6')
    # Homology search by BLAST
    call_blast(ref_blastdb=ref_blastdb,
               input_fasta=input_fasta,
               blast_result_path=blast_result_path,
               threads=threads
               )
    # Predict trait values from best hits of blast results
    blast_result_to_trait(blast_result_path=blast_result_path,
                          out_trait=out_trait,
                          ref_trait=ref_trait,
                          perc_identity=perc_identity
                          )
    return

### func ###
def call_blast(
    ref_blastdb:str, input_fasta:str, blast_result_path:str, threads:int) -> None:
    """Call BLASTn for homology search."""
    cmd = ['blastn',
           '-db', ref_blastdb,
           '-query', input_fasta,
           '-out', blast_result_path,
           '-num_threads', str(threads),
           '-outfmt', '6 qseqid sseqid pident length mismatch gapopen bitscore evalue'
           ]
    subprocess.run(cmd)
    return

def blast_result_to_trait(
    blast_result_path:str, out_trait:str, ref_trait:str, perc_identity:float) -> None:
    """Predict trait values from best hits of blast results."""
    # Load data
    blast_cols = ['sequence', 'species_tax_id', 'pident', 'length', 'mismatch', 'gapopen', 'bitscore', 'evalue']
    blast_result = pd.read_csv(blast_result_path, sep='\t', header=None, names=blast_cols, dtype=str)
    trait = pd.read_csv(ref_trait, sep='\t', dtype=str)

    # Filter the blast result based on the percent identity
    blast_result = preprocess_blast_result(blast_result, perc_identity)

    # Merge with trait data
    res_trait = pd.merge(blast_result, trait, how='left', on='species_tax_id')

    # Summarize the predicted traits for each sequences
    res_trait.set_index('sequence', drop=False, inplace=True)
    summarized_trait = summarize_traits(res_trait, trait.columns[1:])

    # Save
    summarized_trait.to_csv(out_trait, sep="\t", index=False)
    return

def preprocess_blast_result(blast_result: pd.DataFrame, perc_identity: float):
    """Preprocess the data according to the alignment length and percent identity."""
    # Convert columns to numeric
    blast_result[['pident', 'length']] = blast_result[['pident', 'length']].astype(float)

    # Filter by percentage identity, if provided
    if perc_identity is not None:
        blast_result = blast_result[blast_result['pident'] >= perc_identity]

    # Exclude very short sequences based on half the average length
    min_length = blast_result['length'].mean() * 0.5
    blast_result = blast_result[blast_result['length'] >= min_length]
    blast_result.reset_index()

    return blast_result

def summarize_traits(res_trait, trait_cols):
    """Summarize traits for each sequence based on non-null entries."""
    bests = [
        res_trait.loc[res_trait[col].notnull()].drop_duplicates(subset='sequence', keep='first')[[col, 'pident']].rename(columns={'pident': f'{col}_pident'})
        for col in trait_cols
    ]
    out_trait = pd.concat(bests, axis=1)
    out_trait = pd.concat([res_trait['sequence'].drop_duplicates(keep='first'), out_trait], axis=1)
    return out_trait
