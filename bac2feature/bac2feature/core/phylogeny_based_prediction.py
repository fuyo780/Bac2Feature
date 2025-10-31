### library ###
from os.path import dirname, join
import subprocess

import pandas as pd
from picrust2.place_seqs import place_seqs_pipeline

import bac2feature.core.default as default

### main func ###
def predict_by_phylogeny(
    input_fasta:str, out_trait:str, intermediate_dir:str,
    ref_dir_placement=default.ref_dir_placement,
    ref_trait=default.ref_trait, check_nsti=False, threads=1,
    filter_by_nsti=True, threshold_phylodistance=default.threshold_phylodistance,
    threshold_column='cor_0.5') -> None:
    """
    Predict microbial traits from fasta file by phylogenetic placement and ASR.
    """
    out_tree = join(intermediate_dir, 'placed_seqs.tre')
    # Phylogenetic placement by PICRUSt2's pipeline
    place_seqs_pipeline(study_fasta=input_fasta,
                        ref_dir=ref_dir_placement,
                        placement_tool="epa-ng",
                        out_tree=out_tree,
                        threads=threads,
                        out_dir=intermediate_dir,
                        min_align=0,
                        chunk_size=5000,
                        verbose=False
                        )
    # Call HSP function in R package castor (always calculate NSTI)
    call_castor_hsp(tree_path=out_tree,
                    ref_trait_path=ref_trait,
                    out_trait_path=out_trait,
                    check_nsti=True  # Always calculate NSTI
                    )

    # Filter predictions based on NSTI threshold if enabled
    if filter_by_nsti:
        filter_predictions_by_nsti(
            prediction_path=out_trait,
            threshold_path=threshold_phylodistance,
            threshold_column=threshold_column
        )

    # Remove NSTI columns if check_nsti=False
    if not check_nsti:
        predictions = pd.read_csv(out_trait, sep='\t', dtype=str)
        nsti_columns = [col for col in predictions.columns if col.endswith('_nsti')]
        predictions = predictions.drop(columns=nsti_columns)
        predictions.to_csv(out_trait, sep='\t', index=False)

    return

### func ###
def call_castor_hsp(
    tree_path, ref_trait_path, out_trait_path, check_nsti) -> None:
    """
    Call HSP function in R package castor.
    """
    cmd = ["Rscript",
           join(dirname(__file__), "castor_hsp.R"),
           tree_path,
           ref_trait_path,
           out_trait_path,
           str(int(check_nsti))
           ]
    subprocess.run(cmd)
    return

def filter_predictions_by_nsti(
    prediction_path: str, threshold_path: str, threshold_column: str) -> None:
    """
    Filter trait predictions based on NSTI threshold.
    Set prediction values to NaN when NSTI exceeds the threshold.
    Drop trait and NSTI columns when threshold is 0.

    Args:
        prediction_path: Path to prediction results file (will be overwritten)
        threshold_path: Path to NSTI threshold file
        threshold_column: Column name in threshold file to use ('cor_0.5' or 'cor_0')
    """
    # Load prediction results as strings to preserve categorical traits as integers
    predictions = pd.read_csv(prediction_path, sep='\t', dtype=str)

    # Load NSTI thresholds
    thresholds = pd.read_csv(threshold_path, sep='\t', index_col='trait')

    # Track columns to drop (traits with threshold = 0)
    columns_to_drop = []

    # Filter each trait based on its NSTI threshold
    for trait in thresholds.index:
        trait_col = trait
        nsti_col = f'{trait}_nsti'

        # Check if both trait and NSTI columns exist
        if trait_col in predictions.columns and nsti_col in predictions.columns:
            threshold_value = thresholds.loc[trait, threshold_column]

            # If threshold is 0, mark columns for deletion
            if threshold_value == 0:
                columns_to_drop.extend([trait_col, nsti_col])
            else:
                # Convert NSTI column to numeric for comparison
                nsti_numeric = pd.to_numeric(predictions[nsti_col], errors='coerce')

                # Set trait values to NaN where NSTI exceeds threshold
                mask = nsti_numeric > threshold_value
                predictions.loc[mask, trait_col] = ''

    # Drop columns where threshold is 0
    if columns_to_drop:
        predictions = predictions.drop(columns=columns_to_drop)

    # Save filtered predictions
    predictions.to_csv(prediction_path, sep='\t', index=False)
    return
