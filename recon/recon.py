from models import Position, Transaction, Portfolio
import re

def parse_portfolio_text(prtf_text):
    sections = prtf_text.split('\n\n')
    data = [s.strip().split('\n') for s in sections]
    
    header_pattern = re.compile(r'D(\d+)-(POS|TRN)')
    positions = {}
    transactions = {}
    for section in data:
        header_str = section[0]
        day_idx, input_type = header_pattern.search(header_str).groups()
        day_idx = int(day_idx)
        if input_type == 'POS':
            positions[day_idx] = [Position.from_text(s) for s in section[1:]]
        elif input_type == 'TRN':
            transactions[day_idx] = [Transaction.from_text(s) for s in section[1:]]

    return positions, transactions

def reconcile(initial_positions_day=0, compare_to_day=1, in_file='./data/recon.in', out_file='./data/recon.out'):
    with open(in_file, 'r') as f:
        text = f.read()
    
    positions, transactions = parse_portfolio_text(text)
    initial_portfolio = Portfolio.from_positions(positions[initial_positions_day])
    latest_prtf_state = Portfolio.from_positions(positions[compare_to_day])

    for day_idx in range(initial_positions_day, compare_to_day + 1):
        if day_idx in transactions:
            for trn in transactions[day_idx]:
                initial_portfolio.process_transaction(trn)
    
    prtf_diff = initial_portfolio.reconcile(latest_prtf_state)

    with open(out_file, 'w') as f:
        for ticker, diff in prtf_diff.items():
            f.write('{} {}\n'.format(ticker, diff))

if __name__ == '__main__':
    reconcile()