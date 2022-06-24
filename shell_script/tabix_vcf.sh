vcf_dir=$1
search_dir=`ls $vcf_dir/*.vcf.gz`
for vcf_file in $search_dir
do
    echo "CHR"${i} "start"
    filename="$(basename -s .vcf.gz $vcf_file)"
    tabix -p vcf ${vcf_dir}/${filename}.vcf.gz
done