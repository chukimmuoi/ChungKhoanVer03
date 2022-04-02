import matplotlib.pyplot as plt
import pandas as pd
from caculator.Filter import AD_CLOSE_COLUMN


def plot_chart(symbols, time_unit, time_name_type):
    for index, code in enumerate(symbols):
        df = pd.read_csv(f"../data/symbol/{time_unit}_{time_name_type}/{code}.csv")
        df = df[AD_CLOSE_COLUMN]
        df.plot(figsize=(16, 8))
        plt.ylabel("Price")
        plt.title(f"{index}.{code}", fontsize=16)
        plt.legend(fontsize=14)
        plt.show()