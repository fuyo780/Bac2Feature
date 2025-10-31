#!/usr/bin/env Rscript

# This file is derived from PICRUSt2 (https://github.com/picrust/picrust2)
# Original file: picrust2/Rscripts/castor_hsp.R
#
# PICRUSt2 is licensed under the GNU General Public License v3.0 (GPL-3.0)
# Copyright (c) 2016-2023, PICRUSt2 development team
#
# Modifications made for Bac2Feature:
# - Modified to support NSTI (Nearest Sequenced Taxon Index) calculation as optional
# - Enhanced to handle both numerical and categorical trait predictions
#
# This modified version is also distributed under GPL-3.0

suppressWarnings(library(ape, quietly = TRUE))
suppressWarnings(library(castor, quietly = TRUE))

### func ###

get_sorted_prob <- function(in_likelihood, study_tips_i, tree_tips) {

  # Subset to study sequences only and set as rownames.
  tmp_lik <- in_likelihood[study_tips_i, , drop=FALSE]
  rownames(tmp_lik) <- tree_tips[study_tips_i]

  # Set column names to be 1 to max num of counts.
  # colnames(tmp_lik) <- c(0:(ncol(tmp_lik)-1))
  colnames(tmp_lik) <- c(1:(ncol(tmp_lik)))

  # Remove columns that are 0 across all sequences.
  col2remove <- which(colSums(tmp_lik) == 0)
  if(length(col2remove) > 0) {
    tmp_lik <- tmp_lik[, -col2remove, drop=FALSE]
  }

  return(tmp_lik)

}

mp_study_probs <- function(in_trait, in_tree ,unknown_i, check_input) { # Perform MP-based hidden state prediction for categorical traits and return probability matrix

  mp_hsp_out <- hsp_max_parsimony(tree = in_tree,
                                  tip_states = in_trait,
                                  check_input=check_input,
                                  weight_by_scenarios = TRUE)

  return(get_sorted_prob(mp_hsp_out$likelihoods,
                         study_tips_i=unknown_i,
                         tree_tips=in_tree$tip.label))
}

prepare_full_traits <- function(full_tree, known_traits) {
  # Order the trait table to match the tree tip labels.
  # Set all tips without a value to be NA.
  unknown_tips_index <- which(! full_tree$tip.label %in% rownames(known_traits))
  unknown_tips <- full_tree$tip.label[unknown_tips_index]
  num_unknown <- length(unknown_tips)
  num_known <- length(full_tree$tip.label) - num_unknown
  unknown_traits <- as.data.frame(matrix(NA,
                                    nrow=num_unknown,
                                    ncol=ncol(known_traits)))
  rownames(unknown_traits) = unknown_tips
  colnames(unknown_traits) = colnames(known_traits)

  # Get combined dataframe with known and unknown tips
  # (unknown tips have NA as trait values).
  full_traits <- rbind(known_traits, unknown_traits)

  # Remove unknown_df object from memory.
  remove(unknown_traits)
  invisible(gc(verbose = FALSE))

  # Order this combined trait table by the order of tips in the tree.
  full_traits <- full_traits[full_tree$tip.label, , drop=FALSE]
  return(full_traits)
}



### main ###

# Read in command-line arguments.
Args <- commandArgs(TRUE)

# Note first column of the trait table must be species tax id.
full_tree <- read_tree(file=Args[1], check_label_uniqueness = TRUE)
known_traits <- read.delim(Args[2], check.names=FALSE, row.names=1,
                           na.strings=c("NA", "")) # read black as NA value
check_input_set <- as.logical(TRUE)
predict_outfile <- Args[3]
check_nsti <- as.logical(as.integer(Args[4]))

# Prepare data.frame including both known and unknown tips
full_traits <- prepare_full_traits(full_tree, known_traits)
unknown_tips_index <- which(! full_tree$tip.label %in% rownames(known_traits))
unknown_tips <- full_tree$tip.label[unknown_tips_index]

# HSP of numerical traits
n_full_traits <- Filter(is.double, full_traits)
# print(colnames(n_full_traits))
n_full_predict_out <- lapply(n_full_traits,
                             hsp_squared_change_parsimony,
                             tree=full_tree,
                             weighted=TRUE,
                             check_input=check_input_set)
n_unknown_predict_out <- lapply(n_full_predict_out,
                                function(x) {
                                  formatC(x$states[unknown_tips_index], 4)
                                })

# HSP of categorical traits
c_full_traits <- Filter(is.integer, full_traits)
# Convert character states to integer states
# c_full_traits <- c_full_traits + 1
# mapping <- lapply(c_full_traits,
#                   map_to_state_space,
#                   fill_gaps = FALSE,
#                   sort_order = "alphabetical",
#                   include_state_values = FALSE)
# c_full_traits_int <- (lapply(mapping,
#                               function(x) {
#                                 x$mapped_states
#                               }))
c_unknown_predict_out_lik <- lapply(c_full_traits,
                                    function(x) {
                                      mp_study_probs(
                                        in_trait = x+1,
                                        in_tree = full_tree,
                                        unknown_i = unknown_tips_index,
                                        check_input = check_input_set)})
c_unknown_predict_out <- lapply(c_unknown_predict_out_lik,
                                function(x) {
                                  as.numeric(colnames(x)[max.col(x)])-1
                                })
# c_unknown_predict_out <- c_unknown_predict_out - 1
# c_unknown_predict_out <- mapply(function(mapping, c_unknown_predict_out_int) {
#                                   mapping$state_names[c_unknown_predict_out_int]
#                                 },
#                                 mapping,
#                                 c_unknown_predict_out_int)
# Concatenate numerical and categorical traits
n_unknown_predict_out <- data.frame(n_unknown_predict_out, check.names = FALSE)
c_unknown_predict_out <- data.frame(c_unknown_predict_out, check.names = FALSE)
unknown_predict_out <- cbind(n_unknown_predict_out, c_unknown_predict_out)

# Add "sequence" as first column of HSP result
unknown_predict_out$sequence <- unknown_tips
unknown_predict_out <- unknown_predict_out[, c("sequence", colnames(full_traits))]

# Calculate NSTI
if (check_nsti) {
    hsp_nearest_neighbor_out <- lapply(full_traits,
                                       hsp_nearest_neighbor,
                                       tree=full_tree, check_input=check_input_set)
    nsti <- lapply(hsp_nearest_neighbor_out,
                          function(x) {
                            x$nearest_distances[unknown_tips_index]
                          })
    nsti <- data.frame(nsti, check.names = FALSE)
    colnames(nsti) <- lapply(colnames(full_traits),
                             paste,
                             sep = "_",
                             "nsti")
    unknown_predict_out <- cbind(unknown_predict_out, nsti)
}

# Write out predicted values.
write.table(unknown_predict_out, file=predict_outfile, row.names=FALSE, quote=FALSE, sep="\t")
