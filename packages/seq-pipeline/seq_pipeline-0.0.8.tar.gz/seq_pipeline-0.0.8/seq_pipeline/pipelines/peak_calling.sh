# --- VARIABLES ---
# > input_type = indexed_bam
BASE_PATH="{ path base_exists }"
MACS2_CONTROL_PATH="{ optional path file_exists }"
MACS2_PVALUE="{ regex [0-9]+e-[0-9]+ }"
MACS2_GENOME_SIZE="{ regex mm|hs|cc|dm|[0-9]+ }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
module load python/3.9
virtualenv --no-download "$SLURM_TMPDIR/env.python.3"
source "$SLURM_TMPDIR/env.python.3/bin/activate" &&
pip install --no-index --quiet --upgrade pip &&
pip install --no-index --quiet numpy scipy matplotlib pandas MACS2==2.2.7.1
chmod +x "$SLURM_TMPDIR/env.python.3/bin/"* 2> /dev/null


# --- 1 PEAK CALLING ---
printf "\n\n%s\n" "# PEAK CALLING: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
MACS2_OUTPUT_PATH="$BASE_PATH.$MACS2_PVALUE.peaks"
[ -d "$MACS2_OUTPUT_PATH" ] || mkdir "$MACS2_OUTPUT_PATH"
if [ "$MACS2_CONTROL_PATH" = "" ]; then
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -f BAMPE -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
else
    macs2 callpeak -t "$BASE_PATH.bam" -n "$(basename "$BASE_PATH")" --outdir "$MACS2_OUTPUT_PATH" -f BAMPE -c "$MACS2_CONTROL_PATH" -p "$MACS2_PVALUE" -g "$MACS2_GENOME_SIZE" --call-summits --min-length 100 --max-gap 50
fi
REFORMAT_MACS2_SCRIPT_PATH="$BASE_PATH.tmp.reformat_macs2.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$REFORMAT_MACS2_SCRIPT_PATH"
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
EOM
python "$REFORMAT_MACS2_SCRIPT_PATH" "$MACS2_OUTPUT_PATH"
rm "$REFORMAT_MACS2_SCRIPT_PATH"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
