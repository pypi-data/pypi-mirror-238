# --- VARIABLES ---
# > input_type = indexed_bam
BASE_PATH="{ path base_exists }"
CPU_CORES="{ integer > 0 }"
CHR_SIZES_PATH="{ path file_exists }"
EDD_CONTROL_PATH="{ path file_exists }"
EDD_GAP_PENALTY="{ optional number > 0 }"


# --- MODULES ---
printf "\n\n%s\n" "# INITIALIZING ENVIRONMENT AND LOADING MODULES $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
module reset
export MUGQIC_INSTALL_HOME="/cvmfs/soft.mugqic/CentOS6"
module use "$MUGQIC_INSTALL_HOME/modulefiles"
module load bedtools/2.30 mugqic/ucsc/v387
source ~/projects/def-jdrouin/_common/environment/python/2.7.18-edd/bin/activate


# --- 1 EDD ---
printf "\n\n%s\n" "# EDD: START $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
EDD_UNALIGNABLE_REGIONS_PATH=empty_unalignable_regions.tmp.tsv
touch "$EDD_UNALIGNABLE_REGIONS_PATH"
EDD_BASE_NAME="$(basename "$BASE_PATH")"
if [ -z "$EDD_GAP_PENALTY" ] ; then
    EDD_BASE_NAME="$EDD_BASE_NAME.domains"
    edd "$CHR_SIZES_PATH" empty_unalignable_regions.tmp.tsv "$BASE_PATH.bam" "$EDD_CONTROL_PATH" "$BASE_PATH/$EDD_BASE_NAME" -p "$CPU_CORES" --write-log-ratios --write-bin-scores
else
    EDD_BASE_NAME="$EDD_BASE_NAME.gp$EDD_GAP_PENALTY.domains"
    edd "$CHR_SIZES_PATH" empty_unalignable_regions.tmp.tsv "$BASE_PATH.bam" "$EDD_CONTROL_PATH" "$BASE_PATH/$EDD_BASE_NAME" -p "$CPU_CORES" --write-log-ratios --write-bin-scores --gap-penalty "$EDD_GAP_PENALTY"
fi
EDD_REFORMAT_PATH="$BASE_PATH.tmp.reformat_edd.py"
cat << EOM | tr -d "[:space:]" | base64 -d | gzip -dc > "$EDD_REFORMAT_PATH"
H4sIAAKQ9mMCA71Y55LjKBD+r6fo4hLatTTpoqt0OeecvC4VtrDMjQQqwJ7Z9O4HCGGzI0+6oA1D+Dp93aR5CbIHGSxFxXg9hY1eZW/bkeQlaDdKw4KaubYjmi0aChdMr6F7rNeCwykQXsFZkiSs7YTUQGTdEano
0G9EXRulQ1eooaU2i06KJVW7kcehqWnbrVhDk8TL5wui2PIjwVesxishW6IL9ApujTipaarQBBq6pU0x4L/49tPvUisNBTSkXVQEPHgKA4bxlQgqTAi/fvLjT198962RQKfHp2fZ8Wl2eoqSzz/5+ns7hlAiaW8b
aFWB2Ohuo8H6qZLEBL5pKddqmgC8fAJ7nyFuDVrsC1VM0qUW8rEFn46Bl2spWqGE8Q8Ue0KVM2Tg2RqybE2brodLxjW4ro/EZYReMm2xW4PdUqmY4APWdwMM8DaHp8/TxASY9+Fhz4QlJanoCmqqS+NQ6RzB1sXU
hgl9LYiOcjc4ASRRCqT31SHcF0ShMJbCsDEGDeMUGA8C4etnCvcjl0pL1uE0ArAVcKEdIJZ0JgXXjG/oQZWqa5jG6JFGQWvs68zCZsfzuZEwvGHXPZn3aEn1RvId2PO0Ypflgla1JN0aM24yXTpeXNpDJ0h5EnXb
lTb+PXq0fNzPxSR7lRHV/diOvzF2xzE383wz1+N834nzYKGh3LGcQlHA2R3tWFJZNQGlidQToNy0t6TZeONXBRzQ59a1r/hklXiAaV2ZDnmEYq9qej/mI/F5i+8G8B0jZCvr0I3yzumAiSFxZUVfqEIoQvNwNPRy
STsNX9HHn0gp5E0aw4ae/2waQhL5+FPTw62oaIEuHqL0kILYjz3fkkPg/EIyTTF6+vyR3vvHw+YWSd5YPmk6sg6j5Ywu+oXoB0dXotdv16ISUtMKh9jyc/pY4dTvBffOSAhfUXqOj4PXY/tBAI/nLQQSyLRyvcYV
46RpQgk5tYO6SLXKHX0K28DG/Fw2QlGc+p2zJee0XLD6gtWY8ZG98upG6hUvRdsSV/MztKDVZ3bv/Vl8yOrfWI0mcEtlPaG7S0m+XNPlebk0wWJvYXB1uASUtKpwxeS1yosZGg4ENPceN6LGKMsyiK4TeDu1xzCY
iSvncM/9gihactLaghAqt2ZyO2aHgiMWGp+48eEdWju0Q9je7q70wOqcBit/Ccb3QkWoH7Eg75tLealFKan3cBbSPhv04xCB0WGyzUu1FJLmgaF0AqPYfAw7n9xkwRBdSqKZKE+Ov/rwFmaCwJ3MdJScKytxWHEl
WsK4B41qRMZ2ri/1tc4Z2XkyrLoD9wsz/mI2pkl8joe8MmWRmPFoTR0+i6xgrxKPWQ8FNbCn3JiKquH2CQ403SFbY/SY5ose/XuMHLryjW886f/snpVH/baKjB2fqUgmqp1iz6/ZNHtnDg8N0V5BcuM94j67eDJy
r/jE/XCvFGXHYkthD70gkrsX64oYVirQwnlgtlHAZisN22h0XBt1fs+6kbhQVjYHY/SFJdGKbZSVa/b5SnDqNvnd0cc4luSiJLK2T4JkMJ+tXc6GKRASUP/0i8Z37qjHKle6olIOl6Do4mMfsrm/4Q8UhLfMzup2
zKp/Nd7DcHyMxTZd3/2+QEIRfneQf+Df0t+7GZzuwXJSVSXx8xgNZxK6BhOK70ZkJtDEBtun2bS5DbNAD03TZIpsmvg8t4Ut2JKq/dFJWHD+rehYLAaL7oejb5fzZO9NGV8v7HS+O3hdN47HD/Yu25IyOSzdFlmW
9h2FytIWWFmiPl2u2my+jNh2djI1Tv4Nk7Qot/4RAAA=
EOM
python "$EDD_REFORMAT_PATH" "$BASE_PATH/$EDD_BASE_NAME" "$CHR_SIZES_PATH"
bedGraphToBigWig "$BASE_PATH/$EDD_BASE_NAME/$EDD_BASE_NAME.bin_score.bedgraph" "$CHR_SIZES_PATH" "$BASE_PATH/$EDD_BASE_NAME/$EDD_BASE_NAME.bin_score.bigwig"
bedGraphToBigWig "$BASE_PATH/$EDD_BASE_NAME/$EDD_BASE_NAME.log_ratio.bedgraph" "$CHR_SIZES_PATH" "$BASE_PATH/$EDD_BASE_NAME/$EDD_BASE_NAME.log_ratio.bigwig"
rm "$EDD_UNALIGNABLE_REGIONS_PATH" "$EDD_REFORMAT_PATH"


# --- DONE ---
printf "\n\n%s\n" "# DONE $(date '+%Y/%m/%d %H:%M:%S UTC%:::z')" >&2
