SET=$(seq 1 22)

snp_windows=$1
step_size=$2
r2square=$3
echo "Linkage disequilibrium(LD) $snp_windows $step_size $r2square"

for i in $SET
do 
    /root/plink/plink --bfile ./plink_kchip/binary/CHR${i}_KCHIP_snp --indep-pairwise $snp_windows $step_size $r2square   --out ./prune/CHR${i}_LD
    /root/plink/plink --bfile ./plink_kchip/binary/CHR${i}_KCHIP_snp --exclude ./prune/CHR${i}_LD.prune.out --out ./lookup_table/CHR${i}_KCHIP_t2dm --recode A
done