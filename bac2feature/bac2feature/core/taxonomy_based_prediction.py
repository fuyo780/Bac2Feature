### library ###
import decimal
import json
from os.path import join
import subprocess

import pandas as pd

import bac2feature.core.default as default

### main func ###
def predict_by_taxonomy(
    input_fasta:str, out_trait:str, intermediate_dir: str, qiime_env:str,
    ref_nb_classifier=default.ref_nb_classifier,
    ref_trait_taxonomy=default.ref_trait_taxonomy, threads=1) -> None:
    """
    Predict microbial traits from fasta file by taxonomic assignment.
    """
    # Taxonomic assigment by q2-naive-bayes in QIIME2
    nb_result_path = join(intermediate_dir, 'taxonomy.tsv')
    call_qiime_taxonomic_assignment(input_fasta=input_fasta,
                                    out_taxonomy=nb_result_path,
                                    ref_nb_classifier=ref_nb_classifier,
                                    qiime_env=qiime_env,
                                    threads=threads)
    # Predict traits from taxonomy
    predict_by_emp_dist(taxonomy_path=nb_result_path,
                        out_trait=out_trait,
                        ref_trait_taxonomy=ref_trait_taxonomy)
    return

### func ###
def call_qiime_taxonomic_assignment(
    input_fasta: str, out_taxonomy: str,
    ref_nb_classifier: str, qiime_env:str, threads:int) -> None:
    script_path = join(default.b2f_core_dir, 'qiime_taxonomic_assignment.sh')
    cmd = ['conda',
           'run',
           '--name',
           qiime_env,
           script_path,
           '-i',
           input_fasta,
           '-o',
           out_taxonomy,
           '-c',
           ref_nb_classifier,
           '-t',
           str(threads)
           ]
    subprocess.run(cmd)
    return

def predict_by_emp_dist(
    taxonomy_path: str, out_trait: str, ref_trait_taxonomy: str) -> None:
    # Empirical trait distribution
    emp_file = open(ref_trait_taxonomy, 'r')
    emp_dist = json.load(emp_file)
    emp_file.close()

    # Preprocess naibe bayes result
    clades = ["superkingdom", "phylum", "class", "order", "family", "genus", "species"]
    prefix = ["k__", "p__", "c__", "o__", "f__", "g__", "s__"]
    naive_bayes_result = pd.read_csv(taxonomy_path, sep="\t")
    x = naive_bayes_result["Taxon"].str.split("; ", expand=True)
    x = x.set_axis(clades, axis="columns")
    x = x.fillna("")
    for c, p in zip(clades, prefix):
        x[c] = x[c].str.replace(p, "")
    naive_bayes_result = pd.concat([naive_bayes_result, x], axis=1)
    naive_bayes_result["tax_dict"] = naive_bayes_result[clades].apply(
                                         lambda df: df.to_dict(), axis=1
                                     )
    # Prediction
    nt = ['cell_diameter', 'cell_length', 'doubling_h', 'growth_tmp', 'optimum_tmp', 'optimum_ph', 'genome_size', 'gc_content', 'coding_genes', 'rRNA16S_genes', 'tRNA_genes']
    ct = ['gram_stain',
        'sporulation', 'motility', 'range_salinity', 'facultative_respiration',
        'anaerobic_respiration', 'aerobic_respiration', 'mesophilic_range_tmp',
        'thermophilic_range_tmp', 'psychrophilic_range_tmp',
        'bacillus_cell_shape', 'coccus_cell_shape', 'filament_cell_shape',
        'coccobacillus_cell_shape', 'vibrio_cell_shape', 'spiral_cell_shape']
    for t in nt:
        naive_bayes_result[t] = naive_bayes_result["tax_dict"].apply(
                                    lambda x: predict_from_emp(x, emp_dist, t)
                                )
    for t in ct:
        naive_bayes_result[t] = naive_bayes_result["tax_dict"].apply(
                                    lambda x: decimal.Decimal(str(predict_from_emp(x, emp_dist, t))).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_DOWN)
                                )
    # Save
    naive_bayes_result.rename(columns={'Feature ID': 'sequence'}, inplace=True)
    naive_bayes_result[["sequence"]+nt+ct].to_csv(out_trait, sep="\t", index=False)

    return

# Predict traits from taxonomy and empirical distribution
def predict_from_emp(tax_dict: dict, emp_dist: dict, t: str):
    emp = emp_dist[t]
    res = None
    # From species to higher taxonomic groups in order
    for k, v in list(reversed(tax_dict.items())):
        # If there is an empirical distribution for the target trait in taxon k, return it
        if v in emp[k] and emp[k][v] != "NA":
            res = emp[k][v]
            break
        # If the taxonomic group k does not exist or the empirical distribution is unknown, move to the higher taxonomic group k+1.
    if res is None:
        print("There is no record about input taxonomy.")
    return res
