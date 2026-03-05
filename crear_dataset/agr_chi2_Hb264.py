#Análisis para Hb264 que es la alfa-amilasa de Bacillus licheniformis

import sys
import os
import re
from glob import glob
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.metrics import normalized_mutual_info_score
from math import log

# %% ========== functions =======
def msa_to_df(fasta):
    seqs = {}
    with open(fasta,'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                name = line.split()[0][1:]
                seqs[name]=''
            else:
                seqs[name] += line
    # Change the check to 'Hb264.bl' to match the key used below
    if not 'Hb264.bl' in seqs:
        sys.exit(f"Can't find seq for Hb264.bl") # Adjusted error message for clarity
    Hb264= seqs['Hb264.bl']
    chars = {name:list(seq) for name,seq in seqs.items()}
    return pd.DataFrame(chars).T, Hb264

def save_msa(df,file):
    with open(file,'w') as f:
        for idx,row in df.iterrows():
            f.write(f">{idx}\n{''.join(row.values)}\n")

def count_amino_acids(df):
    counts = pd.DataFrame(index=amino_acids, columns=df.columns)

    for col in df.columns:
        counts[col] = df[col].value_counts().reindex(amino_acids, fill_value=0)

    return counts

def count_categos_off(df):
    categos = pd.unique(df.values.ravel()).astype(str)
    categos = sorted([x for x in categos if x!='-'])
    counts = pd.DataFrame(0,index=categos, columns=df.columns)

    for col in df.columns:
        counts[col] = df[col].value_counts().reindex(categos, fill_value=0)

    return counts

def count_categos(df):
    # Get unique values from the DataFrame, which can include integers and the string '-'
    all_unique_values = pd.unique(df.values.ravel())

    # Filter to get only numerical categories (from recoding) for the index
    # This excludes any non-numeric values like '-' string, and handles numpy integers.
    categos_to_count = sorted([x for x in all_unique_values if isinstance(x, (int, np.integer))])

    # Initialize the counts DataFrame with zeros, using only numerical categories as index
    counts = pd.DataFrame(0, index=categos_to_count, columns=df.columns)

    # Count values in each column
    for col in df.columns:
        # Get value counts for the column. This will count all types.
        column_counts = df[col].value_counts()

        # If the string '-' is present in the counts, remove it
        if '-' in column_counts.index:
            column_counts = column_counts.drop(labels=['-'])

        # Reindex with the desired numerical categories, filling missing with 0
        counts[col] = column_counts.reindex(categos_to_count, fill_value=0)

    return counts

def pos2chi_square(H_cnts,T_cnts):
    p_values = {}
    for col in H_cnts.columns:
        a = H_cnts[col].values
        b = T_cnts[col].values
        contingency_table = np.array([a,b])
        contingency_table = contingency_table[:, np.sum(contingency_table, axis=0) > 0]
        if contingency_table.shape[1] <2:
            print(f"{col} is empty",file=sys.stderr)
            continue
        chi2, p_value, _, _ = chi2_contingency(contingency_table)
        p_values[col] = p_value
    return p_values

def get_good_cols(df):
    gap_count = df.apply(lambda col:
    (col == '-').sum())
    good_cols = df.loc[:,gap_count<5].copy()
    print("good_cols",good_cols.shape)
    return good_cols

def recode(df, code):
    df = df.copy()
    for i, aas in enumerate(code):
        df.replace(to_replace=f"[{aas}]", value=i+1, regex=True, inplace=True)
    return df

def read_classifications():
    classes = {}
    with open("/content/amino_acid_classifications.tsv") as f:
        _ = f.readline()
        for line in f:
            line = line.strip()
            name, *categos = line.split("\t")
            classes[name] = [x.replace(' ','') for x in categos if x]
    return classes
def compare_symbols(H_pcnt,T_pcnt):
    pairs ={}
    for symb in H_pcnt.index:
        if H_pcnt[symb] != 0 or T_pcnt[symb]!=0:
            pairs[symb] = (H_pcnt[symb],T_pcnt[symb])
    if len(pairs) > 3:
        sorted_pairs = dict(sorted(pairs.items(), key= lambda x: abs(log(((x[1][0]+5) / (x[1][1]+5)))), reverse=True))
    else:
        sorted_pairs = dict(sorted(pairs.items()))
    parts = [f"{k}:{v[0]}|{v[1]}" for k,v in sorted_pairs.items()]
    return ' '.join(parts)

def Hb264_pos(pos):
    Hb264p = pos +1 - Hb264[0:pos].count('-')
    Hb264aa = Hb264[pos]
    return Hb264p,Hb264aa

# %% ========== main =========

if __name__ == '__main__':
    amino_acids = list('ACDEFGHIKLMNPQRSTVWY-')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    # pd.set_option('future.no_silent_downcasting', True)
    classes =read_classifications()
    # if len(sys.argv) != 2:
    #     sys.exit("msa_count_gaps_v3.py <fasta>")
    fasta = "/content/result.fasta_aa_fm.fa" # Directly assign the fasta file path
    # fasta = sys.argv[1]
    fasta3di = fasta.replace('_aa','_3di')
    trim= fasta.replace('.fa','_trim.fa')
    df,Hb264 = msa_to_df(fasta)
    print(df.shape)
    good_cols = get_good_cols(df)
    keep_cols = good_cols.columns
    renum = {}
    for i, v in enumerate(good_cols.columns):
        renum[v]=i+1
    Hdf = good_cols.loc[good_cols.index.str.startswith('H')]
    Tdf = good_cols.loc[good_cols.index.str.startswith('T')]

    print(''.join(Hdf.loc['Hb264.bl'].astype(str))) # This line is correct, 'Hb264.bl' is in Hdf
    print(''.join(Tdf.loc['Tb7'].astype(str))) # Changed from 'Tb84' to 'Tb7' to use an existing Tdf sequence
    H_cnts = count_amino_acids(Hdf)
    T_cnts = count_amino_acids(Tdf)


    H_pcnt = H_cnts.apply(lambda x:(x/x.sum()) *100).astype(int)
    T_pcnt = T_cnts.apply(lambda x:(x/x.sum()) *100).astype(int)

    p_values = pos2chi_square(H_cnts,T_cnts)
    p_values = {k:v for k,v in p_values.items() if v < 1e-8}
    p_values = dict(sorted(p_values.items(), key=lambda x:x[0]))

    # print(H_pcnt.shape, T_pcnt.shape,len(p_values))
    print('amino_acids', amino_acids)
    for k,v in p_values.items():
        compare = compare_symbols(H_pcnt[k],T_pcnt[k])
        Hb264p,Hb264aa = Hb264_pos(k)
        print(f"  {k}\t{renum[k]}\t{Hb264aa}\t{Hb264p}\t{v:.3g}\t{compare}\taa")

    for class_name, categos in classes.items():
        recoded = recode(good_cols, categos)
        Hdf = recoded.loc[recoded.index.str.startswith('H')]
        Tdf = recoded.loc[recoded.index.str.startswith('T')]
        H_cnts = count_categos(Hdf)
        T_cnts = count_categos(Tdf)

        H_pcnt = (H_cnts / H_cnts.sum()) * 100
        H_pcnt = H_pcnt.fillna(0).astype(int)
        T_pcnt = (T_cnts / T_cnts.sum()) * 100
        T_pcnt = T_pcnt.fillna(0).astype(int)


        p_values = pos2chi_square(H_cnts,T_cnts)
        p_values = {k:v for k,v in p_values.items() if v < 1e-8}
        p_values = dict(sorted(p_values.items(), key=lambda x:x[0]))
        # print(class_name, categos)
        for k,v in p_values.items():
            Hb264p, Hb264aa = Hb264_pos(k) # Unpack the tuple here
            compare = compare_symbols(H_pcnt[k],T_pcnt[k])
            print(f"  {k}\t{renum[k]}\t{Hb264aa}\t{Hb264p}\t{v:.3g}\t{compare}\t{class_name}\t{categos}")

    # print(fasta3di)
    # sys.exit()
    df,_ = msa_to_df(fasta3di)
    good_cols = df.loc[:,keep_cols]
    Hdf = good_cols.loc[good_cols.index.str.startswith('H')]
    Tdf = good_cols.loc[good_cols.index.str.startswith('T')]

    # print(''.join(Hdf.loc['Hb264'].astype(str)))
    # print(''.join(Tdf.loc['Tb84'].astype(str)))

    H_cnts = count_amino_acids(Hdf)
    T_cnts = count_amino_acids(Tdf)

    H_pcnt = H_cnts.apply(lambda x:(x/x.sum()) *100).astype(int)
    T_pcnt = T_cnts.apply(lambda x:(x/x.sum()) *100).astype(int)

    p_values = pos2chi_square(H_cnts,T_cnts)
    p_values = {k:v for k,v in p_values.items() if v < 1e-8}
    p_values = dict(sorted(p_values.items(), key=lambda x:x[0]))
    # print(len(p_values))
    print('3di', amino_acids)
    for k,v in p_values.items():
        print(k,v)
        compare = compare_symbols(H_pcnt[k],T_pcnt[k])
        Hb264p, Hb264aa = Hb264_pos(k) # Unpack the tuple here
        print(f"  {k}\t{renum[k]}\t{Hb264aa}\t{Hb264p}\t{v:.3g}\t{compare}\t3di")
