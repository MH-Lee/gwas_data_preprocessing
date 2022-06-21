vcf_dir=$1
search_dir=`ls $vcf_dir/*.vcf.gz`

missing_threshold=$2
maf=$3
hwe=$4

echo "VCF file directory $vcf_dir"
echo "plink algorithms $missing_threshold $maf $hwe"

for vcf_file in $search_dir
do
    file_name="$(basename -s .vcf.gz $vcf_file)"
    echo "$file_name"
    chrname=$(echo "${filename}" | grep -o -E '[chrCHR0-9]+' | head -1)
    echo ${chrname} "start"
    /root/plink/plink --vcf ${file_name}.vcf.gz --keep ./t2dm_id.txt --snps-only --geno $missing_threshold --maf $maf --hwe $hwe --out ./plink_kchip/${chrname}_KCHIP_snp --recode
    /root/plink/plink --vcf ${file_name}.vcf.gz --keep ./t2dm_id.txt --snps-only --geno $missing_threshold --maf $msf --hwe $hwe --out ./plink_kchip/binary/${chrname}_KCHIP_snp --make-bed
done