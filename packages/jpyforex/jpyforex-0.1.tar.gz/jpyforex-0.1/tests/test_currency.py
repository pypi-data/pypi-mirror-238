from datetime import datetime

import pandas as pd
import pytest

from JPYForex import jpyforex


def test_normal():
    usd = jpyforex.JPYForex()
    df = usd.get_data()
    assert isinstance(df, pd.DataFrame)


def test_currency_code():
    invalid_currencies = ["FAIL", None, "JPY"]
    for invalid_currency in invalid_currencies:
        jf = jpyforex.JPYForex(currency=invalid_currency)
        with pytest.raises(ValueError, match="その通貨コードには対応していません"):
            jf.get_data()


def test_currency_dict():
    cur_dict = {"USD": "DEXJPUS", "EUR": "DEXUSEU", "CNY": "DEXCHUS"}
    for k, v in cur_dict.items():
        jf = jpyforex.JPYForex(k)
        assert jf.cur_code == cur_dict[k]


def test_freq():
    freqs = ["JP", None, "123"]
    for freq in freqs:
        t = jpyforex.JPYForex(freq=freq)
        with pytest.raises((ValueError, TypeError, AssertionError, AttributeError)):
            t.get_data()


def test_dates_format():
    start_dates = ["202", "202001", "20202020202", ""]
    for start_date in start_dates:
        jf = jpyforex.JPYForex(start_date=start_date)
        with pytest.raises(ValueError, match="Input string must be 8 characters."):
            jf.get_data()


def test_dates_format2():
    end_dates = ["2020", "202001", "20200202020", ""]
    for end_date in end_dates:
        jf = jpyforex.JPYForex(end_date=end_date)
        with pytest.raises(ValueError, match="Input string must be 8 characters."):
            jf.get_data()


def test_dates_format3():
    start_dates = ["YYYYMMDD", "12349999", "20230150"]
    for start_date in start_dates:
        jf = jpyforex.JPYForex(start_date=start_date)
        with pytest.raises(ValueError, match="Invalid date format."):
            jf.get_data()


def test_dates_format4():
    end_dates = ["YYYYMMDD", "12349999", "20230150"]
    for end_date in end_dates:
        jf = jpyforex.JPYForex(end_date=end_date)
        with pytest.raises(ValueError, match="Invalid date format."):
            jf.get_data()


def test_date_splitter():
    dates = ["20221203", "20211111", "17771218"]
    for date in dates:
        jf = jpyforex.JPYForex(start_date=date)
        dt = jf._date_splitter(jf.start_date)
        assert isinstance(dt, datetime)


def test_edge_date_case():
    start_date = "20211212"
    end_date = "20210111"
    jf = jpyforex.JPYForex(start_date=start_date, end_date=end_date)
    with pytest.raises(ValueError, match="start must be an earlier date than end"):
        jf.get_data()


if __name__ == "__main__":
    t = jpyforex.JPYForex(start_date="20211212", end_date="20211122")
    t1 = t.get_data()
    print(t1)
