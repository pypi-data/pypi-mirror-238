import pytest

from src.ccxtools.upbit import Upbit


@pytest.fixture
def upbit(env_vars):
    return Upbit('', env_vars)


def test_get_last_price(upbit):
    price = upbit.get_last_price('BTC')
    assert isinstance(price, float)


def test_get_last_prices(upbit):
    # Test input Start
    tickers = ['ETH', 'XRP']
    # Test input End

    prices = upbit.get_last_prices(tickers)
    assert isinstance(prices, dict)
    for ticker in tickers:
        assert ticker in prices
        assert isinstance(prices[ticker], float)


def test_get_best_book_price(upbit):
    assert isinstance(upbit.get_best_book_price('BTC', 'ask'), float)
    assert isinstance(upbit.get_best_book_price('BTC', 'bid'), float)


def test_get_balances(upbit):
    # Test input Start
    tickers = ['ETH', 'XRP']
    balances_input = {
        'ETH': 0.004212,
        'XRP': 15698,
    }
    # Test input End

    balances = upbit.get_balances(tickers)
    assert isinstance(balances, dict)
    for ticker in tickers:
        ticker_balance = balances[ticker]
        assert ticker in balances
        assert isinstance(ticker_balance, float)
        assert balances_input[ticker] * 0.9 <= ticker_balance <= balances_input[ticker] * 1.1


def test_post_market_order(upbit):
    # Test input Start
    ticker = 'XRP'
    amount = 10
    # Test input End

    last_price = upbit.get_last_price(ticker)

    buy_price = upbit.post_market_order(ticker, 'buy', amount, last_price)
    assert 0.9 * last_price < buy_price < 1.1 * last_price
    sell_price = upbit.post_market_order(ticker, 'sell', amount, last_price)
    assert 0.9 * last_price < sell_price < 1.1 * last_price
