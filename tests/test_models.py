import sys
sys.path.insert(0, "./recon")

import models
import unittest
import logging

class TestPositionMethods(unittest.TestCase):

    def test_from_text(self):
        p = models.Position.from_text('AAPL 100')
        
        self.assertEqual('AAPL', p.ticker)
        self.assertEqual(100, p.shares)


class TestTransaction(unittest.TestCase):

    def test_from_text(self):
        t = models.Transaction.from_text('AAPL SELL 100 30000')

        self.assertEqual(t.ticker, 'AAPL')
        self.assertEqual(t.action, models.Action.SELL)
        self.assertEqual(t.shares, 100)
        self.assertEqual(t.notional, 30000)

class TestPortfolio(unittest.TestCase):

    def setUp(self):
        self.test_positions = [
            models.Position.from_text('AAPL 100'),
            models.Position.from_text('SPX 200'),
            models.Position.from_text('Cash 1000')
            ]        
    
    def test_from_positions(self):
        
        prtf = models.Portfolio.from_positions(self.test_positions)

        self.assertDictEqual({ 
            'AAPL': 100.0,
            'SPX': 200.0
        }, prtf.positions)

        self.assertEqual(1000.0, prtf.cash)

    def test_sell_process_transaction(self):

        prtf = models.Portfolio.from_positions(self.test_positions)

        prtf.process_transaction(models.Transaction.from_text('AAPL SELL 100 30000'))

        self.assertDictEqual({
            'SPX': 200.0
        }, prtf.positions)
        self.assertEqual(31000.0, prtf.cash)

    def test_buy_process_transaction(self):

        prtf = models.Portfolio.from_positions(self.test_positions)

        prtf.process_transaction(models.Transaction.from_text('AAPL BUY 100 30000'))

        self.assertDictEqual({
            'AAPL': 200.0,
            'SPX': 200.0
        }, prtf.positions)
        self.assertEqual(-29000.0, prtf.cash)

    def test_deposit_process_transaction(self):

        prtf = models.Portfolio.from_positions(self.test_positions)

        prtf.process_transaction(models.Transaction.from_text('Cash DEPOSIT 0 1000'))

        self.assertDictEqual({ 
            'AAPL': 100.0,
            'SPX': 200.0
        }, prtf.positions)
        self.assertEqual(2000.0, prtf.cash)

    def test_fee_process_transaction(self):

        prtf = models.Portfolio.from_positions(self.test_positions)

        prtf.process_transaction(models.Transaction.from_text('Cash FEE 0 50'))

        self.assertDictEqual({ 
            'AAPL': 100.0,
            'SPX': 200.0
        }, prtf.positions)
        self.assertEqual(950.0, prtf.cash)

    def test_dividend_process_transaction(self):

        prtf = models.Portfolio.from_positions(self.test_positions)

        prtf.process_transaction(models.Transaction.from_text('AAPL DIVIDEND 0 50'))

        self.assertDictEqual({ 
            'AAPL': 100.0,
            'SPX': 200.0
        }, prtf.positions)
        self.assertEqual(1050.0, prtf.cash)

    def test_reconcile(self):
        prtf = models.Portfolio.from_positions(self.test_positions)
        other_prtf = models.Portfolio.from_positions(self.test_positions)
        other_prtf.process_transaction(models.Transaction.from_text('AAPL BUY 1 700'))

        self.assertDictEqual({
            'AAPL': 1.0, 
            'Cash': -700.0
        }, prtf.reconcile(other_prtf))

if __name__ == '__main__':
    unittest.main()
