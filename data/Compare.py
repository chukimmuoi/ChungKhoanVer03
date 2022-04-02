
import pandas as pd

from caculator.Calculator import SYMBOL_COLUMN
from data.Vndirect import get_all_symbol_in_file


def compare(from_csv, with_csv):
    from_csv = get_all_symbol_in_file(f'../data/{from_csv}.csv')
    with_csv = get_all_symbol_in_file(f'../data/{with_csv}.csv')

    from_symbols = from_csv[SYMBOL_COLUMN]
    with_symbols = with_csv[SYMBOL_COLUMN]

    df_symbols_exist = pd.DataFrame(columns=[SYMBOL_COLUMN])
    df_symbols_not_exist = pd.DataFrame(columns=[SYMBOL_COLUMN])

    for code_from in from_symbols:
        is_exist = False
        for code_with in with_symbols:
            if code_from == code_with:
                is_exist = True

        if is_exist:
            df_symbols_exist = df_symbols_exist.append({SYMBOL_COLUMN: code_from}, ignore_index=True)
        else:
            df_symbols_not_exist = df_symbols_not_exist.append({SYMBOL_COLUMN: code_from}, ignore_index=True)

    df_symbols_exist.to_csv("../data/securities/symbols_exist.csv")
    df_symbols_not_exist.to_csv("../data/securities/symbols_not_exist.csv")