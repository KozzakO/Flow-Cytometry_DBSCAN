import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
from pathlib import Path
import seaborn as sns
plt.rc('figure', figsize=(15, 10))

# #############################################################################
def cluster_fig(df, printname, position, title, eps, min_s):
    df = df.loc[(df['Pacific Blue-H'] >= 1000)]
    df = df.reset_index()
    del df['index']
    X = df[['FSC-H', 'Pacific Blue-H']]
    X = X.to_numpy()
    # #############################################################################
    # Compute DBSCAN

    db = DBSCAN(eps=eps, min_samples=min_s).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    print_df = pd.DataFrame(labels, columns=["Labels"])
    print_df[['FSC-H', 'Pacific Blue-H']] = df[['FSC-H', 'Pacific Blue-H']]
    print_df.to_csv(printname)

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    name = Path(printname).stem
    print(name, 'Estimated number of clusters: %d' % n_clusters_)
    print('Estimated number of noise points: %d' % n_noise_)

    # #############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    ax1 = fig.add_subplot(2, 3, position)
    ax1.set_title(title, loc='center', fontsize=10, fontweight="bold")
    plt.subplots_adjust(hspace=0.05, wspace=0.05)

    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        # labels (k) assinged by training. Noise samples are assigned label -1
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]
        class_member_mask = (labels == k)
        xy = X[class_member_mask & core_samples_mask]
        ax1.plot(xy[:, 0], xy[:, 1], 'o', color=tuple(col), alpha=0.25, markersize=0.5)
        xy = X[class_member_mask & ~core_samples_mask]
        ax1.plot(xy[:, 0], xy[:, 1], 'o', color=tuple(col), alpha=0.25, markersize=0.5)

    if position == 1:
        ax1.set_ylabel('DAPI (Targeted)', fontsize=10, fontweight="bold")
        ax1.set_title("SuCasO", loc='center', fontsize=10, fontweight="bold")
        ax1.tick_params(bottom=False)
        ax1.set_xticklabels([])
    if position == 2:
        ax1.set_title("LbCas12a", loc='center', fontsize=10, fontweight="bold")
        ax1.set_yticklabels([])
        ax1.tick_params(left=False, bottom=False)
        ax1.set_xticklabels([])
    if position == 3:
        ax1.set_title("LsCas13a", loc='center', fontsize=10, fontweight="bold")
        ax1.set_yticklabels([])
        ax1.tick_params(left=False, bottom=False)
        ax1.set_xticklabels([])
    if position == 4:
        ax1.set_title('')
        ax1.set_ylabel("DAPI (Non-targeted)", fontsize=10, fontweight="bold")
        ax1.set_xlabel("FSC", fontsize=10, fontweight="bold")
        ax1.set_xticklabels([])
        ax1.tick_params(bottom=False)
    if position == 5 or position == 6:
        ax1.set_title('')
        ax1.set_xlabel('FSC', fontsize=10, fontweight="bold")
        ax1.tick_params(left=False)
        ax1.set_yticklabels([])
    plt.ylim(0, 60000)
    plt.xlim(0, 90000)
    return ax1

directory = r'/your_directory/'
fig = plt.figure()

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        name = Path(filename).stem
        filename = os.path.join('/your_directory/', filename)
        filename = os.path.abspath(os.path.realpath(filename))
        labeled = Path(filename).stem + " 4h" + " 4" + " No" + " - labeled.csv"
        printname = os.path.join('/', labeled)
        df = pd.read_csv(filename)
        if filename.__contains__('SuCasO T'):
            cluster_fig(df, printname, 1, 'SuCasO', your_eps_value, your_min_s_value)
        if filename.__contains__('SuCasO NT'):
            cluster_fig(df, printname, 4, 'SuCasO', your_eps_value, your_min_s_value)
        if filename.__contains__('LbCas12a T'):
            cluster_fig(df, printname, 2, 'LbCas12a', your_eps_value, your_min_s_value)
        if filename.__contains__('LbCas12a NT'):
            cluster_fig(df, printname, 5, 'LbCas12a', your_eps_value, your_min_s_value)
        if filename.__contains__('LsCas13a T'):
            cluster_fig(df, printname, 3, 'LsCas13a', your_eps_value, your_min_s_value)
        if filename.__contains__('LsCas13a NT'):
            cluster_fig(df, printname, 6, 'LsCas13a', your_eps_value, your_min_s_value)

pdf = "Name.pdf"
pdf = os.path.join('/your_directory/', pdf)
plt.savefig(pdf, format='pdf', transparent=True, bbox_inches='tight', pad_inches=0.3)
plt.show()