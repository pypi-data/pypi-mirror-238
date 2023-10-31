# --- VARIABLES ---
# > input_type = indexed_bam
BASE_PATH="{ path base_exists }"
CPU_CORES="{ integer > 0 }"
BIGWIG_BIN_SIZE="{ integer > 0 }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
export MUGQIC_INSTALL_HOME="/cvmfs/soft.mugqic/CentOS6"
module use "$MUGQIC_INSTALL_HOME/modulefiles"
module load mugqic/deepTools/3.5.0


# --- 1 BIGWIG ---
printf "\n\n%s\n" "# BIGWIG: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bamCoverage -b "$BASE_PATH.bam" -o "$BASE_PATH.cpm.bigwig" -bs "$BIGWIG_BIN_SIZE" -e 150 --normalizeUsing BPM -p "$CPU_CORES"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
