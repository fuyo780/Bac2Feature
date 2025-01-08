### library ###
from os.path import dirname, join
import subprocess

from picrust2.place_seqs import place_seqs_pipeline

import bac2feature.core.default as default

### main func ###
def predict_by_phylogeny(
    input_fasta:str, out_trait:str, intermediate_dir:str,
    ref_dir_placement=default.ref_dir_placement,
    ref_trait=default.ref_trait, check_nsti=False, threads=1) -> None:
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
    # Call HSP function in R package castor
    call_castor_hsp(tree_path=out_tree,
                    ref_trait_path=ref_trait,
                    out_trait_path=out_trait,
                    check_nsti=check_nsti
                    )
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
