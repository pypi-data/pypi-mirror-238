import ccxt
from ccxtools.base.CcxtExchange import CcxtExchange
from ccxtools.tools import get_async_results


class Upbit(CcxtExchange):
    DEPOSIT_COMPLETE_STATUSES = ['ACCEPTED', 'CANCELLED', 'REJECTED', 'REFUNDED']
    WITHDRAWAL_COMPLETE_STATUSES = ['DONE', 'FAILED', 'CANCELLED', 'REJECTED']

    def __init__(self, who, env_vars):
        super().__init__(env_vars)
        self.ccxt_inst = ccxt.upbit({
            'apiKey': env_vars(f'UPBIT_API_KEY{who}'),
            'secret': env_vars(f'UPBIT_SECRET_KEY{who}')
        })

    def get_last_price(self, ticker):
        res = self.ccxt_inst.fetch_ticker(f'{ticker}/KRW')
        return res['last']

    def get_last_prices(self, tickers):
        ticker_datas = self.ccxt_inst.fetch_tickers()
        return {ticker: ticker_datas[f'{ticker}/KRW']['last'] for ticker in tickers}

    def get_best_book_price(self, ticker, side):
        order_book = self.ccxt_inst.fetch_order_book(f'{ticker}/KRW')[f'{side}s']
        return order_book[0][0]

    def is_transferring(self):
        [deposits, withdrawals] = get_async_results([
            {'func': self.ccxt_inst.fetch_deposits},
            {'func': self.ccxt_inst.fetch_withdrawals},
        ])

        for deposit in deposits:
            if deposit['info']['state'] not in self.DEPOSIT_COMPLETE_STATUSES:
                return True

        for withdrawal in withdrawals:
            if withdrawal['info']['state'] not in self.WITHDRAWAL_COMPLETE_STATUSES:
                return True

        return False

    def post_market_order(self, ticker, side, amount, price):
        res = self.ccxt_inst.create_order(f'{ticker}/KRW', 'market', side, amount, price)
        order_data = self.ccxt_inst.fetch_order(res['id'])
        return order_data['average']

    def post_withdraw(self, ticker, amount, destination):
        address = self.env_vars(f'{destination}_{ticker}_ADDRESS')
        tag = self.env_vars(f'{destination}_{ticker}_TAG') if ticker in self.WITHDRAW_TAG_NECESSARY_TICKERS else None

        self.ccxt_inst.withdraw(ticker, amount, address, tag, {
            'net_type': ticker
        })
