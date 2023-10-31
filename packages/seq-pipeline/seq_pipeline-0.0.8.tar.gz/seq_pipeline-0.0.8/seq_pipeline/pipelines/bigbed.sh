# --- VARIABLES ---
# > input_type = indexed_bam
BASE_PATH="{ path base_exists }"
CHR_SIZES_PATH="{ path file_exists }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
export MUGQIC_INSTALL_HOME="/cvmfs/soft.mugqic/CentOS6"
module use "$MUGQIC_INSTALL_HOME/modulefiles"
module load bedtools/2.30 mugqic/ucsc/v387


# --- 1 BIGBED ---
printf "\n\n%s\n" "# BIGBED: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bedtools bamtobed -i "$BASE_PATH.bam" > "$BASE_PATH.tmp.bed"
bedSort "$BASE_PATH.tmp.bed" "$BASE_PATH.tmp.sorted.bed"
rm "$BASE_PATH.tmp.bed"
bedToBigBed "$BASE_PATH.tmp.sorted.bed" "$CHR_SIZES_PATH" "$BASE_PATH.bigbed"
rm "$BASE_PATH.tmp.sorted.bed"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
