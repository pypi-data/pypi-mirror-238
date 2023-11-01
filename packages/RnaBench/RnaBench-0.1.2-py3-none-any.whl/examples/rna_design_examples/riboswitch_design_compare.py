import RnaBench
import pandas as pd
import numpy as np
from RnaBench.lib.rna_design_algorithms.riboswitch_design import OriginalProcedure
from RnaBench.lib.feature_extractors import StructuralMotifs
from argparse import ArgumentParser

# set seed
np.random.seed(42)

orig_data = pd.read_pickle('data_preprocessed/data/riboswitch_design_train.plk.gz')
# pick random 50k sequences out of orig_data
orig_data = orig_data.sample(50000).reset_index(drop=True)
gen_data = pd.read_pickle(
    'data_preprocessed/results/Riboswitch_design/custom/custom_1_gc_None_energy_None_12-06-2023-12:32:47.plk')
#gen_data = gen_data.sample(100).reset_index(drop=True)
if "sequence" in gen_data.columns and "predicted_sequence" in gen_data.columns:
    gen_data = gen_data.drop(columns=["sequence"])

if "length" not in gen_data.columns:
    gen_data["length"] = gen_data["predicted_sequence"].apply(len)

riboswitch_benchmark = RnaBench.CompartiveBenchmark()

metrics = riboswitch_benchmark(orig_data, gen_data)

print(metrics)


