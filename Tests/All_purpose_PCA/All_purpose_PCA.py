#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script is supposed to be used in a pipeline to conduct PCA

Simple description: A short script to QC a workflow that processes genetic data.
Shows that machine learning applied to the data newly generated with the 
workflow gives the same results as the same ml technique applied to data we know
is correct.

More technically: Recent implementation of tiling pipeline as workflows 
specified in CWL requires validation/QC. The pipelines produce tiled genomes.
If we apply PCA to these newly tiled genomes, we should get the same 
ethnicity-based spread that we've gotten in the past. If we don't get this, 
then there's clearly something wrong with our latest implementation of the 
tiling pipeline.

Inputs:
* Tiled genomes as 1hot numpy arrays.

Output:
* Plot of PCA results.

################################################################################
"""

"""
Steps:
Mount keep as read/write
Load data
PCA
Plot
Save plot to keep
"""
import os
os.environ.get('DISPLAY','')
import matplotlib as mpl
mpl.use('Agg')      # This line must come before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerPatch
import matplotlib.patches as mpatches
#import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("data_1hot_file")
args = parser.parse_args()
data_1hot_file = args.data_1hot_file



# Load data
data_1hot = np.load(data_1hot_file)

print('Shape of input data:')
print(repr(data_1hot.shape))

# We assume the data doesn't contain any no-calls, otherwise we'd need to do an
# additional step here to remove the no calls.

# Perform PCA
pca = PCA(n_components=2)
X = pca.fit_transform(data_1hot)


# Plot
xlabel = "Principal component 1"
ylabel = "Principal component 2"

plt.figure()
plt.scatter(X[:,0], X[:,1], alpha=0.2) # alpha is opacity

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title("PCA of\n" + data_1hot_file)


# Save figure
plt.savefig("All_purpose_PCA_output_plot.png", format='png',dpi=300)


