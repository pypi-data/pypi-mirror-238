import argparse
import shlex
import sys

from .process import process


HELP = """
usage: $ seq-pipeline $PIPELINE $INPUTS... $OPTIONS...

pipelines:
  chip, atac, chip-lab, atac-lab, rna, bis,
  bigwig, bigwig-lab, peak-calling, peak-calling-lab,
  chip-se-lab

inputs:
  paths to inputs directories and/or
  paths to inputs files (with or without file extension)

options:
  --out-dir --------- path to output directory
                      same directories as inputs by default
  --no-sub-dir ------ if flag set, scripts are written directly in --out-dir
                      and no sub directory per input will be made
  --account --------- account for job submission
                      rrg-jdrouin by default
  --time ------------ requested time as dd-hh:mm:ss or hh:mm:ss
                      03:00:00 by default
  --cpu ------------- requested cpu cores
                      20 by default (64 max on narval)
  --memory ---------- requested memory per core
                      3800M by default (~76G for --cpu 20, ~240G for --cpu 64)
  --bowtie2-index --- path to bowtie2 reference genome index directory
                      path must include the base name of the files inside
                      ~/projects/.../genomes/mm10/bowtie2_index/mm10 by default
  --bam-with-dups --- keep or remove original bam file with duplicated reads
                      remove by default
  --bigwig-bin ------ bin size in base pairs for bigwig
                      10 by default
  --macs2-control --- path to indexed bam file to use as a control
                      experiment (eg, input) for peak calling
                      no control experiment used by default
  --macs2-pvalue ---- macs2 peak treshold pvalue
                      1e-3 by default
  --macs2-genome ---- reference genome size used by macs2
                      mm by default (for mouse, use hs for human)
  --edd-control ----- path to indexed bam file to use as a control
                      experiment (eg, input) for domain calling
  --edd-gap-penalty - edd gap penalty
                      none by default (automatic detection)
  --chr-sizes ------- reference genome chromosome sizes as tsv file
                      ~/projects/.../genomes/mm10/mm10_chr_sizes.tsv by default
  --bismark-genome -- path to bismark reference genome directory
                      ~/projects/.../genomes/mm10/bismark_genome by default
  --hisat2-index ---- path to hisat2 reference genome index directory
                      path must include the base name of the files inside
                      ~/projects/.../genomes/mm10/hisat2_index/mm10 by default
"""


class ArgumentParser(argparse.ArgumentParser):

    def error(self, message):
        message = f"failed to parse command line: {message}"
        raise RuntimeError(message)


def main(raw_args):

    cmd_line = shlex.join(raw_args)

    if "-h" in raw_args or "--help" in raw_args:
        sys.stderr.write(f"{HELP}\n")
        raise SystemExit(0)
    
    while '--from-file' in raw_args:
        index = raw_args.index('--from-file')
        with open(raw_args[index + 1], 'r') as file:
            file_args = [arg
                for line in file
                for arg in shlex.split(line.strip())
                if arg.strip()]
        raw_args = raw_args[:index] + file_args + raw_args[index + 2:]
    
    parser = ArgumentParser()
    parser.add_argument("pipeline")
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--out-dir", dest="out_dir", default=None)
    parser.add_argument("--no-sub-dir", dest="no_sub_dir", action="store_true")
    parser.add_argument("--account", default="rrg-jdrouin")
    parser.add_argument("--time", default="03:00:00")
    parser.add_argument("--cpu", dest="cpu_cores", default="20")
    parser.add_argument("--memory", dest="memory_per_core", default="3800M")
    parser.add_argument("--bowtie2-index", dest="bowtie2_index_path",
        default="$HOME/projects/def-jdrouin/_common/genomes/mm10/bowtie2_index/mm10")
    parser.add_argument("--bam-with-dups", dest="bam_with_duplicates", default="remove")
    parser.add_argument("--bigwig-bin", dest="bigwig_bin_size", default="10")
    parser.add_argument("--macs2-control", dest="macs2_control_path", default="")
    parser.add_argument("--macs2-pvalue", dest="macs2_pvalue", default="1e-3")
    parser.add_argument("--macs2-genome", dest="macs2_genome_size", default="mm")
    parser.add_argument("--edd-control", dest="edd_control_path", default="")
    parser.add_argument("--edd-gap-penalty", dest="edd_gap_penalty", default="")
    parser.add_argument("--chr-sizes", dest="chr_sizes_path",
        default="$HOME/projects/def-jdrouin/_common/genomes/mm10/mm10_chr_sizes.tsv")
    parser.add_argument("--bismark-genome", dest="bismark_genome_path",
        default="$HOME/projects/def-jdrouin/_common/genomes/mm10/bismark_genome")
    parser.add_argument("--hisat2-index", dest="hisat2_index_path",
        default="$HOME/projects/def-jdrouin/_common/genomes/mm10/hisat2_index/mm10")
    arguments = vars(parser.parse_args(raw_args))
    pipeline_name, inputs_locs, out_dir, no_sub_dir = list(arguments.values())[:4]
    settings = dict(list(arguments.items())[4:])

    process(pipeline_name, inputs_locs, out_dir, no_sub_dir, settings, cmd_line=cmd_line)
