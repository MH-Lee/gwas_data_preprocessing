vcf_dir=$1
search_dir=`ls $vcf_dir/*.vcf`
for vcf_file in $search_dir
do
    filename="$(basename -s .vcf $vcf_file)"
    bgzip -c ${vcf_dir}/${filename}.vcf > ${vcf_dir}/${filename}.vcf.gz
done