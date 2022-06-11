import subprocess
import os
import argparse
import shlex
import pandas as pd
from tqdm import tqdm
from glob import glob

def make_lookup_df(path):
    with open(path) as f:
        lines = list()
        for idx, l in tqdm(enumerate(f)):
            lines.append(l.split(' '))
        f.close()
    df = pd.DataFrame(lines[1:], columns=lines[0])
    df[lines[0][-1]] = df[lines[0][-1]].str.replace('\n', '')
    df.drop(['FID', 'PAT', 'MAT', 'SEX', 'PHENOTYPE'], axis=1, inplace=True)
    df.rename(columns={'IID':'sample', lines[0][-1]:lines[0][-1].replace('\n','')}, inplace=True)
    df.replace({'NA':None}, inplace=True)
    df.dropna(axis=1, inplace=True)
    print(df.shape)
    return df

def main(args):
    os.makedirs('./plink_kchip/binary', exist_ok=True)
    os.makedirs(args.raw_dir, exist_ok=True)
    os.makedirs(args.output_dir, exist_ok=True)
    
    if args.bgzip_process:
        subprocess.call(shlex.split('sh ./bgzip_vcf.sh'))
    if args.tabix_precess:
        subprocess.call(shlex.split('sh ./tabix_vcf.sh'))
    if len(os.listdir('./plink_kchip/binary/')) == 0:
        subprocess.call(shlex.split('sh ./convert_plink.sh {geno} {maf} {hwe}'.format(geno=args.geno, maf=args.maf, hwe=args.hwe)))
    if  len(os.listdir('./lookup_table')) == 0:
        subprocess.call(shlex.split('sh ./make_lookup_table.sh {ld_windows} {ld_step} {ld_r2}'.format(ld_windows=args.ld_windows, ld_step=args.ld_step, ld_r2=args.ld_r2)))
    
    ### convert lookup table to 
    print("make snp csv file")
    if len(os.listdir(args.output_dir)) == 0:
        path_list = glob(args.raw_dir + '/*.raw')
        save_path = args.output_dir
        label_csv = pd.read_csv('../t2dm_cohort.csv')
        label_csv = label_csv[['DIST_ID', 'DM_YN', 'SEX', 'AGE']].rename(columns={'DIST_ID':'sample'})
        label_csv['SEX'] = label_csv['SEX'] - 1
        for idx, path in enumerate(path_list):
            print(path)
            snp_df = make_lookup_df(path)
            save_fn = os.path.basename(path.split('.')[1]) + '_demo' + '.csv'
            print("filename : {}, df shape : {}".format(os.path.basename(path.split('.')[1]), snp_df.shape))
            labeled_df = label_csv.merge(snp_df, how='inner', on='sample')
            labeled_df.to_csv(save_path + save_fn, index=False)
    else:
        print("Completed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select GWAS GC arguments')
    parser.add_argument('--bgzip_process', action='store_true', help='compress process vcf file')
    parser.add_argument('--tabix_precess', action='store_true', help='make vcf.gz index file')
    parser.add_argument('--geno', default=0.01, type=float, help='delete snp if missing value proportion greater than 0.01')
    parser.add_argument('--maf', default=0.05, type=float, help='minor allele frequency threshold')
    parser.add_argument('--hwe', default=0.001, type=float, help='hardy weinberg equation threshold (0.001 ~ 5.7*10^-7)')
    parser.add_argument('--ld_windows', default=50, type=int, help='LD snp window size')
    parser.add_argument('--ld_step', default=5, type=int, help='LD snp step size')
    parser.add_argument('--ld_r2', default=0.5, type=float, help='LD snp r2 value threshold')
    parser.add_argument('--raw_dir', default='./lookup_table/', type=str, help='lookup data raw data directory')
    parser.add_argument('--output_dir', default='./csv_file/', type=str, help='LD snp r2 value threshold')
    args = parser.parse_args()
    main(args)