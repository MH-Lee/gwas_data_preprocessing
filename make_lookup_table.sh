# SET=$(seq 1 22)
search_dir=`ls ./plink_kchip/binary/*.bed`

snp_windows=$1
step_size=$2
r2square=$3
data_type=$4
echo "Linkage disequilibrium(LD) $snp_windows $step_size $r2square"

for bed_file in $search_dir
do 
    filename="$(basename -s .bed $bed_file)"
    echo ${filename}
    chrname=$(echo "${filename}" | grep -o -E '[chrCHR0-9]+' | head -1)
    echo ${chrname} "start"
    /root/plink/plink --bfile ./plink_kchip/binary/${filename} --indep-pairwise $snp_windows $step_size $r2square   --out ./prune/${chrname}_LD
    /root/plink/plink --bfile ./plink_kchip/binary/${filename} --exclude ./prune/${chrname}_LD.prune.out --out ./lookup_table/${filename} --recode A
done