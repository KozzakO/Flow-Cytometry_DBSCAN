import pandas as pd
import matplotlib.pyplot as plt
import os
import re

colors = plt.cm.tab10.colors

def count (df, name, label, nuclease, target, time, replicate, antibiotic):
    count_total = df[df.Labels != -1].shape[0]

    df0 = pd.DataFrame()
    df0 = df.loc[(df['Labels'] == label)]
    df0 = df0.reset_index()
    del df0['index']
    df0['R'] = df0['Pacific Blue-H'] / df0['FSC-H']
    mean0 = df0['R'].mean()
    median0 = df0['R'].median()
    stdev0 = df0['R'].std()
    count_label0 = df0[df0.Labels == label].shape[0]
    percentage0 = int(count_label0) * 100 / int(count_total)
    print(name, "DAPI/FSC Mean", "%.2f" % mean0, "%.2f" % percentage0, '%', 'Median', "%.2f" % median0, 'StDev', "%.2f" % stdev0)
    Text_file = '/your_directory/Data.csv'
    with open(Text_file, 'a') as file_object:
        file_object.write(str(mean0) + ',' + str(percentage0) + ',' + str(median0) + ',' + str(stdev0) + ',' + str(nuclease) + ',' + str(target) + ',' + str(time) + ',' + str(replicate) + ',' + str(antibiotic) +'\n')

def parser (df, name, nuclease, target, time, replicate, antibiotic):
    #Count the number of culters minus noise
    n = len(pd.unique(df['Labels']))
    if n == 2:
        count(df, name, 0, nuclease, target, time, replicate, antibiotic)
    if n == 3:
        index = 0
        for value in range(n-1):
            count(df, name, index, nuclease, target, time, replicate, antibiotic)
            index = index + 1
    if n == 4:
        index = 0
        for value in range(n - 1):
            count(df, name, index, nuclease, target, time, replicate, antibiotic)
            index = index + 1

path = r'/your_directory/'
fig = plt.figure()

if os.path.exists('/your_directory/Data.csv'):
    os.remove('/your_directory/Data.csv')

Text_file = '/your_directory/Data.csv'
with open(Text_file, 'a') as file_object:
    file_object.write(str("Mean") + ',' + str("Percentage") + ',' + str("Median") + ',' + str("Stdev") + ',' + str("Nuclease") + ',' + str("Target") + ',' + str("Time") + ',' + str("Replicate") + ',' + str("Antibiotic") +'\n')

for (dirpath, dirnames, filenames) in os.walk(path, topdown=False):
    for filename in filenames:
        if filename.__contains__('- labeled.csv'):
               nuclease = re.findall('^\S+', filename)
               target = re.findall('^\S+\s(\S+)', filename)
               time = re.findall('^\S+\s\S+\s\(.+\)\s(\d)', filename)
               replicate = re.findall('^\S+\s\S+\s\(.+\)\s\S+\s(\d)', filename)
               antibiotic = re.findall('^\S+\s\S+\s\(.+\)\s\S+\s\d+\s+(\w+)', filename)
               full_name = os.path.join(dirpath, filename)
               df = pd.read_csv(full_name)
               if filename.__contains__('SuCasO T'):
                   parser(df, 'SuCasO T', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])
               if filename.__contains__('SuCasO NT'):
                   parser(df,  'SuCasO NT', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])
               if filename.__contains__('LbCas12a T'):
                   parser(df, 'LbCas12a T', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])
               if filename.__contains__('LbCas12a NT'):
                   parser(df,  'LbCas12a NT', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])
               if filename.__contains__('LsCas13a T'):
                   parser(df, 'LsCas13a T', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])
               if filename.__contains__('LsCas13a NT'):
                   parser(df, 'LsCas13a NT', nuclease[0], target[0], time[0], replicate[0], antibiotic[0])