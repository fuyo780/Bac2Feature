### Library ###
import argparse

### Bac2Feature ###
import bac2feature.core.default as default
from bac2feature.core.utils import get_intermediate_dir, reorder_by_fasta
from bac2feature.core.homology_based_prediction import predict_by_homology
from bac2feature.core.taxonomy_based_prediction import predict_by_taxonomy
from bac2feature.core.phylogeny_based_prediction import predict_by_phylogeny

PREDICTION_METHOD = ['homology', 'taxonomy', 'phylogeny']

def main():
    ### Parser ###
    parser = argparse.ArgumentParser(

        description="This script predicts prokaryotic traits from 16S rRNA gene sequences.\n"
                    "Three methods are available: homology-based, taxonomy-based, and phylogeny-based prediction.\n"
                    "Citation: Fujiyoshi et al., Bioinform. Adv., 2025. DOI: 10.1093/bioadv/vbad070",
        epilog='''
Usage example:
bac2feature -s rep_seqs.fasta -o predicted_traits.tsv
''',
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Required arguments
    required = parser.add_argument_group('required arguments')
    # Input 16S rRNA gene sequences.
    required.add_argument('-s', '--seq', metavar='FASTA FILE', required=True,
                        help='Input 16S rRNA sequences in fasta format.')
    # Output predicted trait tables.
    required.add_argument('-o', '--output', metavar='TSV FILE', required=True,
                        help='Output predicted trait table in tsv format.')

    # Optional arguments (no need to create a group - use default)
    # Method to predict traits using 16S rRNA gene phylogeny.
    parser.add_argument('-m', '--method', default='phylogeny', choices=PREDICTION_METHOD,
                        help='Method to predict prokaryotic traits (default: phylogeny).\n'
                            '  "homology": predict prokaryotic traits using homology search.\n'
                            '  "taxonomy": predict prokaryotic traits using taxonomic classification.\n'
                            '  "phylogeny": predict prokaryotic traits using phylogenetic placement.'
                        )
    # Calculate phylogenetic distance to reference 16S rRNA gene sequence data (for the phylogeny-based prediction)
    parser.add_argument('--check_NSTI', action='store_true', required=False, default=False,
                        help='Check NSTI values for the phylogeny-based prediction,\n'
                            'or check alignment identity for the homology-based prediction.')
    # Filter predictions by NSTI threshold (for the phylogeny-based prediction)
    parser.add_argument('--without_filter', action='store_false', dest='filter_by_nsti', required=False, default=True,
                        help='Disable filtering by NSTI threshold for the phylogeny-based prediction.')
    # Intermediate directory
    parser.add_argument('--intermediate_dir', metavar='PATH', required=False, default=None,
                        help='Store intermediate file in this directory.')
    # CPU
    parser.add_argument('--threads', metavar='INT', required=False, default=1,
                        help='Specify the number of CPU in parallel (default: 1).')

    # Reference for phylogenetic placement
    parser.add_argument('--ref_dir_placement', metavar='PATH', required=False, default=default.ref_dir_placement,
                        help='Reference for phylogenetic placement (for developer use).')
    # Reference for homology search
    parser.add_argument('--ref_blastdb', metavar='PATH', required=False, default=default.ref_blastdb,
                        help='Reference for homology search (for developer use).')
    # Reference trait table (Madin et al., 2020, Sci. Data)
    parser.add_argument('--ref_trait', metavar='PATH', required=False, default=default.ref_trait,
                        help='Reference for trait prediction (for developer use).')

    # Read command-line arguments
    args = parser.parse_args()
    ## I/O
    input_fasta = args.seq
    out_trait = args.output
    estimation_method = args.method
    ## Option
    intermediate_dir = args.intermediate_dir
    threads = args.threads
    check_nsti = args.check_NSTI
    filter_by_nsti = args.filter_by_nsti
    ## Ref
    ref_trait = args.ref_trait
    ref_blastdb = args.ref_blastdb
    ref_dir_placement = args.ref_dir_placement


    predict_trait_by_three_methods(
        input_fasta=input_fasta, out_trait=out_trait, estimation_method=estimation_method,
        intermediate_dir=intermediate_dir, threads=threads, check_nsti=check_nsti,
        filter_by_nsti=filter_by_nsti,
        ref_trait=ref_trait, ref_blastdb=ref_blastdb, ref_dir_placement=ref_dir_placement)

    return

### Main func ###
def predict_trait_by_three_methods(
    input_fasta: str, out_trait: str, estimation_method: str,
    intermediate_dir: str, threads: int, check_nsti: bool,
    filter_by_nsti: bool = True,
    ref_trait=default.ref_trait, ref_blastdb=default.ref_blastdb,
    ref_nb_classifier=default.ref_nb_classifier, ref_trait_taxonomy=default.ref_trait_taxonomy,
    qiime_env=default.qiime_env, ref_dir_placement=default.ref_dir_phylogeny) -> None:
    """
    Predict prokaryotic traits using three methods.
    """
    with get_intermediate_dir(intermediate_dir) as work_dir:
        if estimation_method == 'homology':
            predict_by_homology(
                input_fasta=input_fasta,
                out_trait=out_trait,
                intermediate_dir=work_dir,
                ref_blastdb=ref_blastdb,
                ref_trait=ref_trait,
                perc_identity=None,
                check_nsti=check_nsti,
                threads=threads
            )
        elif estimation_method == 'taxonomy':
            predict_by_taxonomy(
                input_fasta=input_fasta,
                out_trait=out_trait,
                intermediate_dir=work_dir,
                ref_nb_classifier=ref_nb_classifier,
                ref_trait_taxonomy=ref_trait_taxonomy,
                qiime_env=qiime_env,
                threads=threads
            )
        elif estimation_method == 'phylogeny':
            predict_by_phylogeny(
                input_fasta=input_fasta,
                out_trait=out_trait,
                intermediate_dir=work_dir,
                ref_dir_placement=ref_dir_placement,
                ref_trait=ref_trait,
                check_nsti=check_nsti,
                filter_by_nsti=filter_by_nsti,
                threads=threads
            )

        # Reorder output to match input FASTA order
        reorder_by_fasta(output_path=out_trait, input_fasta=input_fasta)

    return

if __name__ == '__main__':
    main()
