python genome_preprocessing.py --vcf_path /data/imhoon012/notebook/shared/korean_1k_genome_data --geno 0.01 --maf 0.05 --hwe 0.001 \
                               --ld_windows 50 --ld_windows 5 --ld_r2 0.5 --plink_path ./korean_1k/plink_1k \
                               --raw_path ./korean_1k/lookup_table --output_path ./korean_1k/csv_file --data_type 1k