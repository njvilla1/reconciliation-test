from models import Position, Transaction, Portfolio
import re
import datetime
import argparse
import logging
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

def parse_portfolio_text(prtf_text):
    sections = prtf_text.split('\n\n')
    data = [s.strip().split('\n') for s in sections]
    
    header_pattern = re.compile(r'D(\d+)-(POS|TRN)')
    positions = {}
    transactions = {}
    for section in data:
        header_str = section[0].strip()
        day_idx, input_type = header_pattern.search(header_str).groups()
        day_idx = int(day_idx)
        if input_type == 'POS':
            positions[day_idx] = [Position.from_text(s.strip()) for s in section[1:]]
        elif input_type == 'TRN':
            transactions[day_idx] = [Transaction.from_text(s.strip()) for s in section[1:]]

    return positions, transactions

def reconcile(initial_positions_day=0, compare_to_day=1, in_file='./data/recon.in', out_file='./data/recon.out'):

    log.debug('Reading file {}'.format(in_file))
    with open(in_file, 'r') as f:
        text = f.read()
    
    positions, transactions = parse_portfolio_text(text)
    log.debug('Parsed positions and transactions text')
    initial_portfolio = Portfolio.from_positions(positions[initial_positions_day])
    log.debug('Initial portfolio: {}'.format(initial_portfolio))
    latest_prtf_state = Portfolio.from_positions(positions[compare_to_day])
    log.debug('Compare to portfolio: {}'.format(latest_prtf_state))

    for day_idx in range(initial_positions_day, compare_to_day + 1):
        if day_idx in transactions:
            for trn in transactions[day_idx]:
                initial_portfolio.process_transaction(trn)
    
    log.debug('Portfolio after processing transactions: {}'.format(initial_portfolio))
    prtf_diff = initial_portfolio.reconcile(latest_prtf_state)

    log.debug('Reconciliation diff: {}'.format(prtf_diff))

    with open(out_file, 'w') as f:
        for ticker, diff in prtf_diff.items():
            f.write('{} {}\n'.format(ticker, diff))
    log.debug('Wrote outfile {}'.format(args.out_file))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Reconcile initial positions plus transactions with another set of positions.')
    parser.add_argument('--initial_positions_day', type=int, help='day index of initial positions', default=0)
    parser.add_argument('--compare_to_day', type=int, help='day index of positions to compare', default=1)

    parser.add_argument('--in_file', type=str, help='input file (e.g. recon.in)', default='./data/recon.in')
    parser.add_argument('--out_file', type=str, help='output file (e.g. recon.out)', default='./data/recon.out')

    args = parser.parse_args()
    
    reconcile(initial_positions_day=args.initial_positions_day, \
        compare_to_day=args.compare_to_day, \
        in_file=args.in_file, \
        out_file=args.out_file)

