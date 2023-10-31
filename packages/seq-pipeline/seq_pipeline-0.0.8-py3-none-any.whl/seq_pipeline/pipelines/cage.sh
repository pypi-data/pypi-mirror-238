# --- VARIABLES ---
# > input_type = single_fastq
BASE_PATH="{ path base_exists }"
CPU_CORES="{ integer > 0 }"
HISAT2_INDEX_PATH="{ path base_exists }"
BIGWIG_BIN_SIZE="{ integer > 0 }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
module load python/3.9 java/13.0
module load fastqc/0.11 hisat2/2.2 samtools/1.12
virtualenv --no-download "$SLURM_TMPDIR/env.python.3"
source "$SLURM_TMPDIR/env.python.3/bin/activate" &&
pip install --no-index --quiet --upgrade pip &&
pip install --no-index --quiet numpy scipy matplotlib pandas deepTools==3.5.0
chmod +x "$SLURM_TMPDIR/env.python.3/bin/"* 2> /dev/null


# --- FUNCTIONS ---
function reads-count {
    case "$1" in
        fastq) echo "$(zcat "$2" | wc -l) / 4" | bc ;;
        fastqx2) echo "$(zcat "$2" | wc -l) / 4 * 2" | bc ;;
        bam) samtools idxstats "$2" | awk -F '\t' '{s+=$3}END{print s}' ;;
        *) echo "error: invalid format: $1" >&2 ; return 1 ;;
    esac
}
function reads-diff {
    local INITIAL="$(reads-count "$1" "$2")"
    local FINAL="$(reads-count "$3" "$4")"
    local PERCENT="$(echo "scale=2 ; $FINAL / $INITIAL * 100" | bc)"
    echo "reads: initial=$INITIAL final=$FINAL ($PERCENT% of initial)"
}


# --- 1 QC ---
printf "\n\n%s\n" "# QC: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
fastqc --quiet -t "$CPU_CORES" "$BASE_PATH.fastq.gz"
rm "${BASE_PATH}_fastqc.zip"
[ -d "$BASE_PATH.qc" ] || mkdir "$BASE_PATH.qc"
mv "${BASE_PATH}_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").qc.html"


# --- 2 ALIGNEMENT ---
printf "\n\n%s\n" "# ALIGNMENT: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
hisat2 -p "$CPU_CORES" --no-unal -x "$HISAT2_INDEX_PATH" "$BASE_PATH.fastq.gz" |
samtools view -@ "$CPU_CORES" -o "$BASE_PATH.bam" /dev/stdin


# --- 3 SORTING ---
printf "\n\n%s\n" "# SORTING: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
mv "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools sort -@ "$CPU_CORES" -o "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools index -@ "$CPU_CORES" "$BASE_PATH.bam"
echo "aligned reads: $(reads-diff fastqx2 "$BASE_PATH.r1.fastq.gz" bam "$BASE_PATH.bam")" >&2
rm "$BASE_PATH.unsorted.bam"


# --- 4 BIGWIG ---
printf "\n\n%s\n" "# BIGWIG: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bamCoverage -b "$BASE_PATH.bam" -o "$BASE_PATH.cpm.bigwig" -bs "$BIGWIG_BIN_SIZE" --normalizeUsing BPM -p "$CPU_CORES"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
