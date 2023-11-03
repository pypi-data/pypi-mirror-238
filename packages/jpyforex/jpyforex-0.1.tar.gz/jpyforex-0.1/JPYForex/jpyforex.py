from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas as pd
import pandas_datareader as pdr # type: ignore


@dataclass
class JPYForex:
    currency: str = "USD"
    freq: str = "D"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    """
    Args:
        currency: 円建てデータを取得する通貨を指定
            現状は
            "USD" : 米ドル
            "EUR" : ユーロ
            "CNY" : 人民元
            の三通貨のみ対応。

        freq: データ取得頻度
            "D": 日々
            "W": 週（平均）
            "M": 月（平均）
            "Q": 4半期（平均）
            "Y": １年（平均）

        start_date, end_date
            ともにNoneであれば、直近５年分のデータを取得する
            'YYYYMMDD'

    Returns:
        pd.DataFrame

        index: 日付
        columns: 通貨名: データ

    """

    @property
    def cur_code(self) -> str:
        cur_dict = {"USD": "DEXJPUS", "EUR": "DEXUSEU", "CNY": "DEXCHUS"}
        return cur_dict[self.currency]

    @property
    def start_datetime(self) -> Optional[datetime]:
        if self.start_date is not None:
            st = self._date_splitter(self.start_date)
            return st
        else:
            return None

    @property
    def end_datetime(self) -> Optional[datetime]:
        if self.end_date is not None:
            et = self._date_splitter(self.end_date)
            return et
        else:
            return None

    def get_data(self) -> pd.DataFrame:
        if self.currency == "USD":
            df = pdr.get_data_fred(
                self.cur_code, start=self.start_datetime, end=self.end_datetime
            )
        elif self.currency == "EUR":
            df = pdr.get_data_fred(
                [self.cur_code, "DEXJPUS"],
                start=self.start_datetime,
                end=self.end_datetime,
            )
            df["DEXJPEU"] = df.apply(lambda x: x[0] * x[1], axis=1)
            df = df[["DEXJPEU"]]
        elif self.currency == "CNY":
            df = pdr.get_data_fred(
                [self.cur_code, "DEXJPUS"],
                start=self.start_datetime,
                end=self.end_datetime,
            )
            df["DEXJPCH"] = df.apply(lambda x: x[1] / x[0], axis=1)
            df = df[["DEXJPCH"]]
        else:
            raise ValueError("その通貨コードには対応していません")

        if self.freq != "D":
            try:
                df = df.resample(self.freq).mean()
            except ValueError:
                raise ValueError("invalid freq")
        return df

    def _date_splitter(self, d: str) -> datetime:
        if not isinstance(d, str):
            raise ValueError("Input must be a string.")
        if len(d) != 8:
            raise ValueError("Input string must be 8 characters.")
        try:
            str_d = str(d)
            year_int = int(str_d[:4])
            month_int = int(str_d[4:6])
            day_int = int(str_d[6:])
            dt = datetime(year_int, month_int, day_int)
        except ValueError:
            raise ValueError("Invalid date format.")

        return dt


if __name__ == "__main__":
    t = JPYForex("CNY", freq="Q", start_date="20211021", end_date="20220111")
    d = t.get_data()
    print(d)
