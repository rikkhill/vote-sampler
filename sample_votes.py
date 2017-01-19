# Given a list of postcodes, sample votes from the constituencies covering
# those postcodes, at rates proportional to those constituencies' turnouts

import pandas as pd
import numpy as np
import getopt
import sys


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "f:")
    except getopt.GetoptError:
        print('python sample_votes.py [ -f <inputfile> ] | [ postcode_1 ... ]')
        sys.exit(2)

    postcodes = []

    for opt, arg in opts:
        # parse the file if given the -f opt
        if opt == "-f":
            # Append all lines in the file to the postcode list
            with open(arg) as file:
                postcodes += [p.strip() for p in file.readlines()]


    # Then parse all the remaining arguments as separate postcodes
    postcodes += args

    # Remove spaces
    postcodes = [p.replace(" ", "") for p in postcodes]
    # Read in postcode lookup
    postcode_lookup = pd.read_csv("./data/postcodes.csv")

    # Filter for postcodes of interest
    postcode_lookup = postcode_lookup[postcode_lookup["postcode"].isin(postcodes)]
    postcode_lookup["weights"] = postcode_lookup["valid_turnout"] / postcode_lookup["valid_turnout"].sum()

    # Sample a thousand postcodes from the selection
    postcode_sample = postcode_lookup.sample(n=10000, axis=0, replace=True, weights="weights")
    # Dummy count variable
    postcode_sample["count"] = 1
    postcode_sample = postcode_sample[["constituency_id", "count"]]

    constituency_counts = postcode_sample.groupby("constituency_id").count()
    constituency_counts.reset_index(inplace=True)

    # Load constituency results
    results = pd.read_csv("./data/candidates.csv")
    constituencies = constituency_counts["constituency_id"].tolist()
    results = results[results["constituency_id"].isin(constituencies)]

    # Weight results by sample counts
    weighted_results = pd.merge(results, constituency_counts, on="constituency_id")
    weighted_results["votes"] = weighted_results["votes"] / weighted_results["count"]

    # Pivot into matrix
    results_matrix = results.pivot(index="constituency_id", columns="party", values="votes")
    results_matrix.fillna(0, inplace=True)

    # Sum over existing constituencies
    results_sum = results_matrix.sum(axis=0)
    results_sum = results_sum / results_sum.sum()
    results_sum = results_sum.sort_values(ascending=False)
    results_sum.columns = ["Party", "Proportion of Vote"]

    print(results_sum)

if __name__ == "__main__":
    main(sys.argv[1:])
