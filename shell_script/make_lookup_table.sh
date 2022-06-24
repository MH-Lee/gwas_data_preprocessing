# SET=$(seq 1 22)
snp_windows=$1
step_size=$2
r2square=$3
data_type=$4
plink_path=$5
raw_path=$6

search_dir=`ls ${plink_path}/binary/*.bed`

echo "Plink path : $plink_path"
echo "loouk-up table path : $raw_path"
echo "Linkage disequilibrium(LD) $snp_windows $step_size $r2square"

for bed_file in $search_dir
do 
    filename="$(basename -s .bed $bed_file)"
    echo ${filename}
    chrname=$(echo "${filename}" | grep -o -E '[chrCHR0-9]+' | head -1)
    echo ${chrname} "start"
    /root/plink/plink --bfile ${plink_path}/binary/${filename} --indep-pairwise $snp_windows $step_size $r2square   --out ${plink_path}/prune/${chrname}_LD
    /root/plink/plink --bfile ${plink_path}/binary/${filename} --exclude ${plink_path}/prune/${chrname}_LD.prune.out --out ${raw_path}/${filename} --recode A
done