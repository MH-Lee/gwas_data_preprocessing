import subprocess
import os
import argparse
import shlex
import pandas as pd
from tqdm import tqdm
from glob import glob
from time import time

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
    os.makedirs(os.path.join(args.plink_path, 'binary'), exist_ok=True)
    os.makedirs(os.path.join(args.plink_path, 'prune'), exist_ok=True)
    os.makedirs(args.raw_path, exist_ok=True)
    os.makedirs(args.output_path, exist_ok=True)
    
    start_time = time()
    if args.bgzip_process:
        subprocess.call(shlex.split('sh ./bgzip_vcf.sh'))
    if args.tabix_precess:
        subprocess.call(shlex.split('sh ./tabix_vcf.sh'))
    if len(os.listdir(os.path.join(args.plink_path, 'binary'))) == 0:
        subprocess.call(shlex.split(f'sh ./convert_plink.sh {args.vcf_dir} {args.geno} {args.maf} {args.hwe} {args.data_type} {args.plink_path}'))
        # .format(vcf_dir=args.vcf_path, geno=args.geno, maf=args.maf, hwe=args.hwe, data_type=args.data_type, plink_path=args.plink_path)
    if  len(os.listdir(args.raw_path)) == 0:
        subprocess.call(shlex.split(f'sh ./make_lookup_table.sh {args.ld_windows} {args.ld_step} {args.ld_r2} {args.data_type} {args.plink_path} {args.raw_path}'))
        #.format(ld_windows=args.ld_windows, ld_step=args.ld_step, ld_r2=args.ld_r2, data_type=args.data_type, raw_path=args.raw_path)))
    
    ### convert lookup table to 
    print(len(os.listdir(args.output_path)))
    if len(os.listdir(args.output_path)) == 0:
        print("make snp csv file")
        path_list = glob(os.path.join(args.raw_path, '*.raw'))
        print(args.raw_path + '*.raw', ':', path_list)
        save_path = args.output_path
        label_csv = pd.read_csv('./sample_id/sample_cohort_{data_type}.csv'.format(data_type=args.data_type))
        if args.data_type == 'kchip':
            label_csv = label_csv[['DIST_ID', 'DM_YN', 'SEX', 'AGE']].rename(columns={'DIST_ID':'sample'})
            label_csv['SEX'] = label_csv['SEX'] - 1
        else:
            label_csv = label_csv[['DIST_ID', 'DM_YN', 'Sex', 'Age']].rename(columns={'DIST_ID':'sample'})
            label_csv['Sex'] = label_csv['Sex'].map({'M':0, 'F':1}) 
        for idx, path in enumerate(path_list):
            print(path)
            snp_df = make_lookup_df(path)
            save_fn = os.path.basename(path.split('.')[1]) + '_demo' + '.csv'
            print("filename : {}, df shape : {}".format(os.path.basename(path.split('.')[1]), snp_df.shape))
            labeled_df = label_csv.merge(snp_df, how='inner', on='sample')
            labeled_df.to_csv(os.path.join(save_path, save_fn), index=False)
    else:
        print("Completed!")
    end_time = time()
    print("Completed! : ", end_time - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select GWAS GC arguments')
    parser.add_argument('--bgzip_process', action='store_true', help='compress process vcf file')
    parser.add_argument('--tabix_precess', action='store_true', help='make vcf.gz index file')
    parser.add_argument('--vcf_path', default='../original_vcf', help='vcf.gz directory path')
    parser.add_argument('--geno', default=0.01, type=float, help='delete snp if missing value proportion greater than 0.01')
    parser.add_argument('--maf', default=0.05, type=float, help='minor allele frequency threshold')
    parser.add_argument('--hwe', default=0.001, type=float, help='hardy weinberg equation threshold (0.001 ~ 5.7*10^-7)')
    parser.add_argument('--ld_windows', default=50, type=int, help='LD snp window size')
    parser.add_argument('--ld_step', default=5, type=int, help='LD snp step size')
    parser.add_argument('--ld_r2', default=0.5, type=float, help='LD snp r2 value threshold')
    parser.add_argument('--plink_path', default='./plink_kchip/', type=str, help='plink ped/bed data directory')
    parser.add_argument('--raw_path', default='./lookup_table/', type=str, help='lookup data raw data directory')
    parser.add_argument('--output_path', default='./csv_file/', type=str, help='LD snp r2 value threshold')
    parser.add_argument('--data_type', default='1k', type=str, help='(1) 1k (2) kchip')
    args = parser.parse_args()
    main(args)