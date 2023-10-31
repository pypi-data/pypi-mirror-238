# --- VARIABLES ---
# > input_type = single_fastq
BASE_PATH="{ path base_exists }"
CPU_CORES="{ integer > 0 }"
BOWTIE2_INDEX_PATH="{ path base_exists }"
BAM_WITH_DUPLICATES="{ choice keep|remove }"
BIGWIG_BIN_SIZE="{ integer > 0 }"
MACS2_CONTROL_PATH="{ optional path file_exists }"
MACS2_PVALUE="{ regex [0-9]+e-[0-9]+ }"
MACS2_GENOME_SIZE="{ regex mm|hs|cc|dm|[0-9]+ }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
module load python/3.9 java/13.0
module load fastqc/0.11 bowtie2/2.4 samtools/1.12
virtualenv --no-download "$SLURM_TMPDIR/env.python.3"
source "$SLURM_TMPDIR/env.python.3/bin/activate" &&
pip install --no-index --quiet --upgrade pip &&
pip install --no-index --quiet numpy scipy matplotlib pandas deepTools==3.5.0 MACS2==2.2.7.1
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


# --- 1 QC AND TRIMMING ---
printf "\n\n%s\n" "# QC AND TRIMMING: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
TRIM_READS_SCRIPT_PATH="$BASE_PATH.tmp.trim_reads.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$TRIM_READS_SCRIPT_PATH"
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
EOM
python "$TRIM_READS_SCRIPT_PATH" -i "$BASE_PATH.fastq.gz" -a "AGATCGGAAGAG" -p "$CPU_CORES"
rm "$TRIM_READS_SCRIPT_PATH"
fastqc --quiet -t "$CPU_CORES" "$BASE_PATH.fastq.gz" "$BASE_PATH.trimmed.fastq.gz"
rm "${BASE_PATH}_fastqc.zip" "$BASE_PATH.trimmed_fastqc.zip"
[ -d "$BASE_PATH.qc" ] || mkdir "$BASE_PATH.qc"
mv "${BASE_PATH}_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").qc.html"
mv "$BASE_PATH.trimmed_fastqc.html" "$BASE_PATH.qc/$(basename "$BASE_PATH").trimmed.qc.html"


# --- 2 ALIGNEMENT ---
printf "\n\n%s\n" "# ALIGNMENT: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bowtie2 -p "$CPU_CORES" --fr --no-unal --no-mixed --no-discordant -x "$BOWTIE2_INDEX_PATH" "$BASE_PATH.trimmed.fastq.gz" |
samtools fixmate -@ "$CPU_CORES" -m /dev/stdin "$BASE_PATH.bam"


# --- 3 SORTING ---
printf "\n\n%s\n" "# SORTING: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
mv "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools sort -@ "$CPU_CORES" -o "$BASE_PATH.bam" "$BASE_PATH.unsorted.bam"
samtools index -@ "$CPU_CORES" "$BASE_PATH.bam"
echo "aligned reads: $(reads-diff fastq "$BASE_PATH.trimmed.fastq.gz" bam "$BASE_PATH.bam")" >&2
rm "$BASE_PATH.unsorted.bam"


# --- 4 DUPLICATES ---
printf "\n\n%s\n" "# DUPLICATES: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
mv "$BASE_PATH.bam" "$BASE_PATH.with_duplicates.bam"
mv "$BASE_PATH.bam.bai" "$BASE_PATH.with_duplicates.bam.bai"
samtools markdup -@ "$CPU_CORES" -r -s "$BASE_PATH.with_duplicates.bam" "$BASE_PATH.bam"
samtools index -@ "$CPU_CORES" "$BASE_PATH.bam"
echo "duplicates: $(reads-diff bam "$BASE_PATH.with_duplicates.bam" bam "$BASE_PATH.bam")" >&2
[ "$BAM_WITH_DUPLICATES" = remove ] && rm "$BASE_PATH.with_duplicates.bam" "$BASE_PATH.with_duplicates.bam.bai"


# --- 5 BIGWIG ---
printf "\n\n%s\n" "# BIGWIG: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
bamCoverage -b "$BASE_PATH.bam" -o "$BASE_PATH.cpm.bigwig" -bs "$BIGWIG_BIN_SIZE" -e 150 --normalizeUsing BPM -p "$CPU_CORES"


# --- 6 PEAK CALLING ---
printf "\n\n%s\n" "# PEAK CALLING: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
MACS2_OUTPUT_PATH="$BASE_PATH.$MACS2_PVALUE.peaks"
[ -d "$MACS2_OUTPUT_PATH" ] || mkdir "$MACS2_OUTPUT_PATH"
if [ "$MACS2_CONTROL_PATH" = "" ]; then
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
else
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -c "$MACS2_CONTROL_PATH" -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
fi
REFORMAT_MACS2_SCRIPT_PATH="$BASE_PATH.tmp.reformat_macs2.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$REFORMAT_MACS2_SCRIPT_PATH"
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
EOM
python "$REFORMAT_MACS2_SCRIPT_PATH" "$MACS2_OUTPUT_PATH"
rm "$REFORMAT_MACS2_SCRIPT_PATH"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
