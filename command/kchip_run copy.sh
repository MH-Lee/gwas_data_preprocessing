python genome_preprocessing.py --vcf_path ../filtered_vcf --geno 0.01 --maf 0.05 --hwe 0.001 \
                               --ld_windows 50 --ld_windows 5 --ld_r2 0.5 --plink_path ./kchip/plink_1k \
                               --raw_path ./kchip/lookup_table --output_path ./kchip/csv_file --data_type kchip