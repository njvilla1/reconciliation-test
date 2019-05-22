import sys
sys.path.insert(0, "./recon") #Inserts recon module dir to path in order to import models and recon
# unfortunately this means unit tests must be run from git repo base directory
# This avoids having to install module to local site-packages during development/testing

import recon
from models import Portfolio
import unittest
import logging

class TestParseMethod(unittest.TestCase):

    def test_parse_recon_text(self):
        test_recon_text = """D0-POS
            AAPL 100
            GOOG 200
            SP500 175.75
            Cash 1000

            D1-TRN
            AAPL SELL 100 30000
            GOOG BUY 10 10000
            Cash DEPOSIT 0 1000
            Cash FEE 0 50
            GOOG DIVIDEND 0 50
            TD BUY 100 10000

            D1-POS
            GOOG 220
            SP500 175.75
            Cash 20000
            MSFT 10"""
        positions, transactions = recon.parse_portfolio_text(test_recon_text)

        self.assertEqual(2, len(positions))
        self.assertEqual(1, len(transactions))

        test_prtf = Portfolio.from_positions(positions[0])
        self.assertDictEqual({
            'AAPL': 100,
            'GOOG': 200,
            'SP500': 175.75
        }, test_prtf.positions)
        self.assertEqual(1000, test_prtf.cash)        

if __name__ == '__main__':
    unittest.main()
