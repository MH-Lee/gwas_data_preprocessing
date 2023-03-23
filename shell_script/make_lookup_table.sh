# SET=$(seq 1 22)
plink_path=$1
raw_path=$2

search_dir=`ls ${plink_path}/binary/*.bed`

echo "Plink path : $plink_path"
echo "loouk-up table path : $raw_path"

for bed_file in $search_dir
do 
    filename="$(basename -s .bed $bed_file)"
    echo ${filename}
    chrname=$(echo "${filename}" | grep -o -E '[chrCHR0-9]+' | head -1)
    echo ${chrname} "start"
    /root/plink/plink --bfile ${plink_path}/binary/${filename} --out ${raw_path}/${filename} --recode A
done