import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
plt.rc('figure', figsize=(10, 5))

df = pd.read_csv('/your_directory/Data.csv')

def jitter(time, replicate):
    if replicate==1:
        new_time = time + -0.6
    if replicate==2:
        new_time = time + -0.2
    if replicate==4:
        new_time = time + 0.2
    if replicate==3:
        new_time = time + 0.6
    return new_time

df['Jitter'] = df.apply(lambda x: jitter(x['Time'], x['Replicate']), axis=1)
fig = plt.figure()

lists = ({'Target': 'T', 'Antibiotic': 'No'},
         {'Target': 'NT', 'Antibiotic': 'No'})

def plot_fig(df, antibiotic, target, position):
    color_dict_nuc = dict({'SuCasK': '#c42e4c', 'LbCas12a': '#93b5df', 'LsCas13a': '#f6c1c8'})
    color_dict_rep = dict({1: 'orange', 2: 'blue', 3: 'crimson', 4: 'pink'})
    df0 = df.loc[(df['Antibiotic'] == antibiotic) & (df['Target'] == target)]
    df0 = df0.reset_index()
    del df0['index']
    ax0 = fig.add_subplot(1, 2, position)
    minsize = min(df0['Percentage']) * 10
    maxsize = max(df0['Percentage']) * 10
    for key, grp in df0.groupby(['Replicate'] and ['Jitter']):
        ax0 = grp.plot(ax=ax0, kind='line', x='Jitter', y='Mean', linewidth=0.25, linestyle = '--', c='gray')
    ax0 = sns.scatterplot(x='Jitter', y='Mean', hue='Nuclease', size='Percentage', linewidth=0.5, alpha=0.5, edgecolor='black', sizes=(minsize, maxsize), data=df0, palette=color_dict_nuc) #x_jitter=True,
    plt.subplots_adjust(hspace=0.05, wspace=0.05)
    handles, labels = ax0.get_legend_handles_labels()
    if position == 1:
        ax0.set_title('Targeted', loc='center', fontsize=10, fontweight="bold")
        ax0.legend(handles[16:], labels[16:], bbox_to_anchor=(2.6, 1), handletextpad=1, columnspacing=1, loc="best", edgecolor='black', ncol=1, frameon=False)
        ax0.set_xlabel('Nuclease', fontsize=10, fontweight="bold")
        ax0.set_ylabel('Average DAPI/FSC', fontsize=10, fontweight="bold")
    if position == 2:
        ax0.set_title('Non-targeted', loc='center', fontsize=10, fontweight="bold")
        ax0.set_yticklabels([])
        ax0.set_ylabel('')
        ax0.set_xlabel('Nuclease', fontsize=10, fontweight="bold")
        ax0.tick_params(left=False)
        ax0.legend('', frameon=False)

    plt.xlim(1, 7)
    plt.ylim(0, 2)
    return ax0

for list in lists:
    if list['Target'] == 'T' and list['Antibiotic'] == 'No':
        plot_fig(df, list['Antibiotic'], list['Target'], 1)
    if list['Target'] == 'NT' and list['Antibiotic'] == 'No':
        plot_fig(df, list['Antibiotic'], list['Target'], 2)

pdf = "your_file_name.pdf"
pdf = os.path.join('/your_directory/', pdf)
plt.savefig(pdf, format='pdf', transparent=True, bbox_inches='tight', pad_inches=0.3)
plt.show()