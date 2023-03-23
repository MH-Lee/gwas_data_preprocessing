import subprocess
import os
import argparse
import shlex
import pandas as pd
from tqdm import tqdm
from glob import glob
from time import time

def main(args):
    os.makedirs(os.path.join(args.plink_path, 'binary'), exist_ok=True)
    os.makedirs(os.path.join(args.plink_path, 'prune'), exist_ok=True)
    os.makedirs(args.raw_path, exist_ok=True)
    os.makedirs(args.output_path, exist_ok=True)
    
    start_time = time()
    if args.bgzip_process:
        subprocess.call(shlex.split('sh ./shell_script/bgzip_vcf.sh'))
    if args.tabix_precess:
        subprocess.call(shlex.split('sh ./shell_script/tabix_vcf.sh'))
    if len(os.listdir(os.path.join(args.plink_path, 'binary'))) == 0:
        subprocess.call(shlex.split(f'sh ./shell_script/convert_plink.sh {args.vcf_path} {args.data_type} {args.plink_path}'))
    if  len(os.listdir(args.raw_path)) == 0:
        subprocess.call(shlex.split(f'sh ./shell_script/make_lookup_table.sh  {args.plink_path} {args.raw_path}'))
    end_time = time()
    print("Completed! : ", end_time - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select GWAS GC arguments')
    parser.add_argument('--bgzip_process', action='store_true', help='compress process vcf file')
    parser.add_argument('--tabix_precess', action='store_true', help='make vcf.gz index file')
    parser.add_argument('--vcf_path', default='../original_vcf', help='vcf.gz directory path')
    parser.add_argument('--plink_path', default='./plink_kchip/', type=str, help='plink ped/bed data directory')
    parser.add_argument('--raw_path', default='./lookup_table/', type=str, help='lookup data raw data directory')
    parser.add_argument('--data_type', default='1k', type=str, help='(1) 1k')
    args = parser.parse_args()
    main(args)