vcf_dir=$1
search_dir=`ls $vcf_dir/*.vcf.gz`

missing_threshold=$2
maf=$3
hwe=$4
data_type=$5

echo "VCF file directory $vcf_dir"
echo "plink algorithms $missing_threshold $maf $hwe"

for vcf_file in $search_dir
do
    filename="$(basename -s .vcf.gz $vcf_file)"
    echo "$filename"
    chrname=$(echo "${filename}" | grep -o -E '[chrCHR0-9]+' | head -1)
    echo ${chrname} "start"
    /root/plink/plink --vcf ${vcf_dir}/${filename}.vcf.gz --keep ./sample_id/sample_id_${data_type}.txt --snps-only --geno $missing_threshold --maf $maf --hwe $hwe --out ./plink_kchip/${chrname}_${data_type}_snp --recode
    /root/plink/plink --vcf ${vcf_dir}/${filename}.vcf.gz --keep ./sample_id/sample_id_${data_type}.txt --snps-only --geno $missing_threshold --maf $msf --hwe $hwe --out ./plink_kchip/binary/${chrname}_${data_type}_snp --make-bed
done