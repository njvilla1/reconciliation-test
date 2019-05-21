#%%
from models import Position, Transaction, Portfolio
import re

## Usage:
#%%
def read_file():
    with open('./recon.in', 'r') as f:
        sections = f.read().split('\n\n')
        data = [s.strip().split('\n') for s in sections]
    return data
#%%
data = read_file()
header_re = re.compile(r'D(\d+)-(POS|TRN)')
positions = {}
transactions = {}
for section in data:
    header_str = section[0]
    day_idx, inp_type = header_re.search(header_str).groups()
    if inp_type == 'POS':
        positions[day_idx] = [Position.from_text(s) for s in section[1:]]
    elif inp_type == 'TRN':
        transactions[day_idx] = [Transaction.from_text(s) for s in section[1:]]

#%%
initial_day_idx = '0'
portfolio = Portfolio.from_positions(positions[initial_day_idx])

for day_idx, trns_for_day in transactions.items():
    for trn in trns_for_day:
        portfolio.process_transaction(trn)

print('Calculated positions:')
print(portfolio)