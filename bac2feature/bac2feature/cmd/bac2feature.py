### Library ###
import argparse
import tempfile
from typing import Optional
import os

### Bac2Feature ###
import bac2feature.core.default as default
from bac2feature.core.homology_based_prediction import predict_by_homology
from bac2feature.core.taxonomy_based_prediction import predict_by_taxonomy
from bac2feature.core.phylogeny_based_prediction import predict_by_phylogeny

PREDICTION_METHOD = ['homology', 'taxonomy', 'phylogeny']

### Main func ###
def main():
    parser = argparse.ArgumentParser(

        description="This script predicts prokaryotic traits from 16S rRNA gene sequences."
                    "Three methods are available: homology-based, taxonomy-based, and phylogeny-based prediction.",
        epilog='''
Usage example:
bac2feature -s rep_seqs.fasta -o predicted_traits.tsv
''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Input 16S rRNA gene sequences.
    parser.add_argument('-s', '--seq', metavar='FASTA FILE', required=True,
                        help='Input 16S rRNA sequences in fasta format.')
    # Output predicted trait tables.
    parser.add_argument('-o', '--output', metavar='TSV FILE', required=True,
                        help='Output predicted trait table in tsv format.')
    # Method to predict traits using 16S rRNA gene phylogeny.
    parser.add_argument('-m', '--method', default='phylogeny', choices=PREDICTION_METHOD,
                        help='Method to predict prokaryotic traits. See Paper in detail.'
                            '"homology": predict prokaryotic traits using homology search. '
                            '"taxonomy": predict prokaryotic traits using taxonomic classification. '
                            '"phylogeny": predict prokaryotic traits using phylogenetic placement.'
                        )
    # Reference for phylogenetic placement
    parser.add_argument('--ref_dir_placement', metavar='PATH', required=False, default=default.ref_dir_placement,
                        help='Ref for phylogenetic placement.')
    # Reference for homology search
    parser.add_argument('--ref_blastdb', metavar='PATH', required=False, default=default.ref_blastdb,
                        help='Ref for homology search.')
    # Reference trait table (Madin et al., 2020, Sci. Data)
    parser.add_argument('--ref_trait', metavar='PATH', required=False, default=default.ref_trait,
                        help='Ref for trait prediction.')
    # Intermediate directory
    parser.add_argument('--intermediate_dir', metavar='PATH', required=False, default=None,
                        help='Store intermediate file in this directory.')
    # CPU
    parser.add_argument('--threads', metavar='INT', required=False, default=1,
                        help='Specify the number of CPU in parallel.')
    # Calculate phylogenetic distance to reference 16S rRNA gene sequence data (for the phylogeny-based prediction)
    parser.add_argument('--calculate_NSTI', action='store_true')

    # Read command-line arguments
    args = parser.parse_args()
    ## I/O
    input_fasta = args.seq
    out_trait = args.output
    estimation_method = args.method
    ## Option
    intermediate_dir = args.intermediate_dir
    threads = args.threads
    check_nsti = args.calculate_NSTI
    ## Ref
    ref_trait = args.ref_trait
    ref_blastdb = args.ref_blastdb
    ref_dir_placement = args.ref_dir_placement


    predict_trait_by_three_methods(
        input_fasta=input_fasta, out_trait=out_trait, estimation_method=estimation_method,
        intermediate_dir=intermediate_dir, threads=threads, check_nsti=check_nsti,
        ref_trait=ref_trait, ref_blastdb=ref_blastdb, ref_dir_placement=ref_dir_placement)

    return

def predict_trait_by_three_methods(
    input_fasta: str, out_trait: str, estimation_method: str,
    intermediate_dir: Optional[str], threads: int, check_nsti: bool,
    ref_trait=default.ref_trait, ref_blastdb=default.ref_blastdb,
    ref_nb_classifier=default.ref_nb_classfier, ref_trait_taxonomy=default.ref_trait_taxonomy,
    qiime_env=default.qiime_env, ref_dir_placement=default.ref_dir_phylogeny) -> None:
    """
    Predict prokaryotic traits using three methods.
    """
    if intermediate_dir is not None:
        if not os.path.exists(intermediate_dir):
            os.makedirs(intermediate_dir)
        if estimation_method == 'homology':
            predict_by_homology(input_fasta=input_fasta,
                                out_trait=out_trait,
                                intermediate_dir=intermediate_dir,
                                ref_blastdb=ref_blastdb,
                                ref_trait=ref_trait,
                                perc_identity=None,
                                threads=threads
                                )
        # Taxonomy based prediction
        elif estimation_method == 'taxonomy':
            predict_by_taxonomy(input_fasta=input_fasta,
                                out_trait=out_trait,
                                intermediate_dir=intermediate_dir,
                                ref_nb_classifier=ref_nb_classifier,
                                ref_trait_taxonomy=ref_trait_taxonomy,
                                qiime_env=qiime_env,
                                threads=threads
                                )
        # Phylogeny based prediction
        elif estimation_method == 'phylogeny':
            predict_by_phylogeny(input_fasta=input_fasta,
                                out_trait=out_trait,
                                intermediate_dir=intermediate_dir,
                                ref_dir_placement=ref_dir_placement,
                                ref_trait=ref_trait,
                                check_nsti=check_nsti,
                                threads=threads
                                )
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            intermediate_dir = temp_dir
            # Homology based prediction
            if estimation_method == 'homology':
                predict_by_homology(input_fasta=input_fasta,
                                    out_trait=out_trait,
                                    intermediate_dir=intermediate_dir,
                                    ref_blastdb=ref_blastdb,
                                    ref_trait=ref_trait,
                                    perc_identity=None,
                                    threads=threads
                                    )
            # Taxonomy based prediction
            elif estimation_method == 'taxonomy':
                predict_by_taxonomy(input_fasta=input_fasta,
                                    out_trait=out_trait,
                                    intermediate_dir=intermediate_dir,
                                    ref_nb_classifier=ref_nb_classifier,
                                    ref_trait_taxonomy=ref_trait_taxonomy,
                                    qiime_env=qiime_env,
                                    threads=threads
                                    )
            # Phylogeny based prediction
            elif estimation_method == 'phylogeny':
                predict_by_phylogeny(input_fasta=input_fasta,
                                    out_trait=out_trait,
                                    intermediate_dir=intermediate_dir,
                                    ref_dir_placement=ref_dir_placement,
                                    ref_trait=ref_trait,
                                    check_nsti=check_nsti,
                                    threads=threads
                                    )
    return

if __name__ == '__main__':
    main()
