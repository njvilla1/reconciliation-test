from enum import Enum
import re

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
        ''' 
        Processes single transaction against current state of 
        portfolio (positions + cash).
        DEPOSIT/DIVIDEND -> +cash
        FEE -> -cash
        BUY -> -cash, +shares
        SELL -> +cash, -shares
        '''
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
            if self.positions[transaction.ticker] == 0.0:
                del self.positions[transaction.ticker]
            
    def reconcile(self, other_prtf):
        ''' 
        Reconciles current state of positions and cash against another
        Portfolio object. Returns a dict containing all tickers and 'Cash' as
        keys, and the diff per ticker between the two portfolio positions as values
        '''
        diffs = {}
        for ticker in set(list(self.positions.keys()) + list(other_prtf.positions.keys())):
            ticker_diff = other_prtf.positions.get(ticker, 0.0) - self.positions.get(ticker, 0.0)
            if abs(ticker_diff) > 0.0: diffs[ticker] = ticker_diff
        
        cash_diff = other_prtf.cash - self.cash
        if abs(cash_diff) > 0.0: diffs['Cash'] = cash_diff

        return diffs

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