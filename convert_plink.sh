SET=$(seq 1 22)

vcf_dir=$1
missing_threshold=$2
maf=$3
hwe=$4

echo "VCF file directory $vcf_dir"
echo "plink algorithms $missing_threshold $maf $hwe"

for i in $SET
do
    echo "CHR"${i} "start"
    /root/plink/plink --vcf ${vcf_dir}/CHR${i}_annoINFO_filINF0.8_Open_72K_190924_1.vcf.gz --keep ./t2dm_id.txt --snps-only --geno $missing_threshold --maf $maf --hwe $hwe --out ./plink_kchip/CHR${i}_KCHIP_snp --recode
    /root/plink/plink --vcf ${vcf_dir}/CHR${i}_annoINFO_filINF0.8_Open_72K_190924_1.vcf.gz --keep ./t2dm_id.txt --snps-only --geno $missing_threshold --maf $msf --hwe $hwe --out ./plink_kchip/binary/CHR${i}_KCHIP_snp --make-bed
done