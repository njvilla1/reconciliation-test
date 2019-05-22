# Reconciliation Test
This module will read an input file (./data/recon.in), which contains postition (POS) and transaction (TRN) information for a given day (D0, D1), and reconcile the initial positions against the final state of positions after accounting for transactions in between. 

Tested with Python version 3.6.4

usage: 
```bash
python recon.py [-h] [--initial_positions_day INITIAL_POSITIONS_DAY]
                [--compare_to_day COMPARE_TO_DAY] [--in_file IN_FILE]
                [--out_file OUT_FILE]
```
e.g.
```bash
cd reconciliation-test
python ./recon/recon.py --initial_positions_day=0 --compare_to_day=1 --in_file=./data/recon.in --out_file=./data/recon.out
```
Produces outfile (data/recon.out)

Unit testing:
```bash
cd reconciliationt-test
python -m unittest discover ./tests
```
