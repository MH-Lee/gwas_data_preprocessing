# GWAS(SNP) data preprocessing

유전자 변이 정보를 담은 Single-nucleotide polymorphism (SNP) 데이터의 전처리 과정을 담고 있습니다.

사전에 plink 1.9 version과 bcftools 설치(선택)가 필요함.

### Prerequisite

+ plink 설치 [url](https://www.cog-genomics.org/plink/)
+ 설치 참고 사이트 [url](https://mopipe.tistory.com/8)

```{shell}
wget https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20220402.zip
```

(선택) bcftools VCF 파일을 처리해주는 프로그램
+ vcf 파일에 index를 달아주기 위해서는 필요

```{shell}
sudo apt-get update
sudo apt-get install bcftools
```

### Prerequisite

```{python}
python genome_preprocessing.py --geno [float:defalut=0.01] --maf [float:defalut=0.05] --hwe [float:defalut=0.001] \
                               --ld_windows [int:defalut=50] --ld_windows [inf:defalut=5] --ld_r2 [float:defalut=0.5] \
                               --raw_dir [str] --output_dir [str] \
                               --bgzip_process [store_true (optional)] --tabix_precess [store_true (optional)]
```

1. bgzip_vcf.sh
+ bgzip_process : vcf를 vcf.gz으로 압축

2. tabix_vcf.sh
+ tabix_precess : vcf.gz 파일에 index 파일(tbi) 생성

3. convert_plink.sh

+ geno : missing value가 일정 비율 이상인 샘플 제거
+ maf : minor allele frequency thredhold 설정 (default : 0.05)
+ hwe : hardy-weinberg 평형 threshold (0.001 ~ 5.7*10^-7)

4. make_lookup_table.sh

+ ld_windows : LD snp window size (indep-pairwise)
+ ld_step : LD snp step size (indep-pairwise)
+ ld_r2 : LD snp r2 value threshold (indep-pairwise)

### Reference

1. Romero, A. et al. Diet networks: Thin parameters for fat genomic. In International Conference on Learning Representations 2017 (Conference Track) 

2. Anderson, C. A., Pettersson, F. H., Clarke, G. M., Cardon, L. R., Morris, A. P., & Zondervan, K. T. (2010). Data quality control in genetic case-control association studies. Nature protocols, 5(9), 1564-1573.

3. Abdulaimma, B., Fergus, P., Chalmers, C., & Montañez, C. C. (2020, July). Deep learning and genome-wide association studies for the classification of type 2 diabetes. In 2020 International Joint Conference on Neural Networks (IJCNN) (pp. 1-8). IEEE.# gwas_data_preprocessing
