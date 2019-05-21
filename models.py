#%%
from enum import Enum
import re

#%%
class Action(Enum):
    BUY = 1
    SELL = 2
    DEPOSIT = 3
    FEE = 4
    DIVIDEND = 5

class Position ( object ):
    def __init__(self, ticker, shares):
        self.ticker = ticker
        self.shares = shares
    @classmethod
    def from_text(self, text):
        ticker, shares_str = text.split(' ')
        shares = float(shares_str)
        return Position(ticker, shares)

    def __repr__(self):
        return 'Position[ {}: {} ]'.format(self.ticker, self.shares)

class Portfolio( object ):
    def __init__(self, initial_positions={}, cash=0.):
        self.positions = initial_positions
        self.cash = cash

    def process_transaction(self, transaction):
        if transaction.ticker != 'Cash' and transaction.ticker not in self.positions:
            self.positions[transaction.ticker] = 0

        if transaction.action in (Action.DEPOSIT, Action.DIVIDEND):
            self.cash += transaction.notional
        elif transaction.action == Action.FEE:
            self.cash -= transaction.notional

        elif transaction.action == Action.BUY:
            self.positions[transaction.ticker] += transaction.shares
            self.cash -= transaction.notional
        elif transaction.action == Action.SELL:
            self.positions[transaction.ticker] -= transaction.shares
            self.cash += transaction.notional
            
    def reconcile(self, other_prtf):
        raise NotImplementedError()        

    @classmethod
    def from_positions(cls, positions):
        cash = 0.
        result_positions = {}
        for pos in positions:
            if pos.ticker == 'Cash':
                cash = pos.shares
            else:
                result_positions[pos.ticker] = pos.shares
        return cls(initial_positions=result_positions, cash=cash)

    def __repr__(self):
        return "Portfolio[ CASH: {}, POSITIONS: {} ]".format(self.cash, self.positions)

class Transaction( object ):
    def __init__(self, ticker, action, shares, notional):
        self.ticker = ticker
        self.action = action
        self.shares = shares
        self.notional = notional

    @classmethod
    def from_text(self, text):
        ticker, action_str, shares_str, notional_str = text.split(' ')
        action = Action[action_str]
        shares = int(shares_str)
        notional = float(notional_str)
        return Transaction(ticker, action, shares, notional)