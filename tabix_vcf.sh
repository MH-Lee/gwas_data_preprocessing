SET=$(seq 1 22)
for i in $SET
do
    echo "CHR"${i} "start"
    tabix -p vcf ../original_vcf/CHR${i}_annoINFO_filINF0.8_Open_72K_190924_1.vcf.gz
done