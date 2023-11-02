import jsonlines

with jsonlines.open('results_bel-rus.jsonl') as f:
    for line in f:
        if line['method'] == 'mbr':
            print(f"{line['num_samples']}\t{line['chrf']}")
        else:
            print(f"\t{line['chrf']}")

