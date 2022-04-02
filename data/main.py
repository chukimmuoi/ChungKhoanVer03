import Vndirect
import time

from chart.Draw import plot_chart
from data.Vndirect import get_all_symbol_in_file


def build(count_year, is_first_call, is_create_new_file_tssl, is_draw_chart):
    """
    Lấy thông tin dữ liệu chứng khoán VN theo chu kỳ: 1, 2, 3, 4 , 5 ... năm
    :param count_year: Số năm
    :param is_first_call: Giá trị bằng True cho lần lấy dữ liệu mới đầu tiên của chu kỳ,
    sau đó sẽ là False để mục đích hiệu chỉnh filter dữ liệu được nhanh hơn.
    :param is_create_new_file_tssl: Tạo file tỷ suất sinh lời mới.
    :param is_draw_chart: Vẽ chart
    :return: not return
    """
    start = time.time()
    if is_create_new_file_tssl:
        symbols_csv = get_all_symbol_in_file('../data/securities/AllSymbol.csv')
        symbols = symbols_csv['stockSymbol']
        Vndirect.mining_data_from_vndirect(symbols, count_year, is_first_call)

    symbols_csv = get_all_symbol_in_file(f'../data/TSSL_In_{count_year}_Year.csv')
    symbols = symbols_csv['Symbol']
    Vndirect.mining_data_from_vndirect(symbols, 1, False)

    end = time.time()
    print(f"Total run time: {round(end - start)}s")

    if is_draw_chart:
        plot_chart(symbols, count_year)


# Step 00
# build(count_year=1, is_first_call=True, is_create_new_file_tssl=True, is_draw_chart=False)

# Step 01
# build(count_year=6, is_first_call=True, is_create_new_file_tssl=True, is_draw_chart=False)

# Step 02
build(count_year=6, is_first_call=False, is_create_new_file_tssl=False, is_draw_chart=True)