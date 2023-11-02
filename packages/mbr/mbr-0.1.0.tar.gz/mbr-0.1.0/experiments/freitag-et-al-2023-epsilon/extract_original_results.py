# Header: LANGPAIR	MODEL_NAME	CORPUS	DECODING_METHOD	SAMPLE_ORIGIN	UTILITY_FUNCTION	LENGTH_PENALTY_ALPHA	NUM_SAMPLES	SEED	BLEU	CHRF_1	CHRF_2	CHRF_3	METEOR	METEOR_BALANCED
import csv
from collections import defaultdict
from pathlib import Path

language_pairs = [
    "dan-epo",
    "aze-eng",
    "bel-rus",
    "deu-fra",
]

original_results_path = Path(__file__).parent / "original_results.tsv"

print("MBR")
for language_pair in language_pairs:
    print(language_pair)
    mbr_results = defaultdict(int)  # average over two seeds
    with open(original_results_path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row["LANGPAIR"] != language_pair:
                continue
            if row["MODEL_NAME"] != "no_label_smoothing":
                continue
            if row["CORPUS"] != "test":
                continue
            if row["DECODING_METHOD"] != "mbr":
                continue
            if row["SAMPLE_ORIGIN"] != "sample":
                continue
            if row["UTILITY_FUNCTION"] != "sentence-chrf-2":
                continue
            score = float(row["CHRF_2"])
            mbr_results[int(row["NUM_SAMPLES"])] += score
    for num_samples, score in sorted(mbr_results.items()):
        print(f"{num_samples}\t{score / 2 * 100}")
    print()
print()

print("Beam")
for language_pair in language_pairs:
    print(language_pair)
    with open(original_results_path, "r") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row["LANGPAIR"] != language_pair:
                continue
            if row["MODEL_NAME"] != "no_label_smoothing":
                continue
            if row["CORPUS"] != "test":
                continue
            if row["DECODING_METHOD"] != "top":
                continue
            if row["SAMPLE_ORIGIN"] != "beam":
                continue
            if row["LENGTH_PENALTY_ALPHA"] != "1.0":
                continue
            if row["NUM_SAMPLES"] != "5":
                continue
            score = float(row["CHRF_2"])
            print(f"{score * 100}")
    print()
print()
