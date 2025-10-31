### Utils func ###
from contextlib import contextmanager
import os
import tempfile
from typing import Optional

import pandas as pd


@contextmanager
def get_intermediate_dir(intermediate_dir: Optional[str]):
    """
    Get or create temporary directory as a context manager.
    """
    if intermediate_dir is None:
        # Use temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
    else:
        # Use provided directory
        if not os.path.exists(intermediate_dir):
            os.makedirs(intermediate_dir)
        yield intermediate_dir

def reorder_by_fasta(output_path: str, input_fasta: str) -> None:
    """
    Reorder prediction results to match the order of sequences in the input FASTA file.
    """
    # Get sequence order from FASTA
    fasta_order = []
    with open(input_fasta, 'r') as f:
        for line in f:
            if line.startswith('>'):
                # Extract entire sequence ID
                seq_id = line[1:].strip()
                fasta_order.append(seq_id)

    # Load prediction results as strings to preserve data types
    predictions = pd.read_csv(output_path, sep='\t', dtype=str)

    # Reorder based on FASTA order
    predictions['sequence'] = pd.Categorical(predictions['sequence'], categories=fasta_order, ordered=True)
    predictions = predictions.sort_values('sequence')

    # Save reordered results
    predictions.to_csv(output_path, sep='\t', index=False)
    return
