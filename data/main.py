import Vndirect
import time

from chart.Draw import plot_chart
from data.Units import TimeUnitsType, get_time_name_with_type
from data.Vndirect import get_all_symbol_in_file


def build(time_units, time_type, is_first_call, is_create_new_file_tssl, is_draw_chart):
    """
    Lấy thông tin dữ liệu chứng khoán VN theo chu kỳ: 1, 2, 3, 4 , 5 ... năm
    :param time_units: Số năm, tháng, tuần, ngày
    :param time_type:  Loại đơn vị thời gian
    :param is_first_call: Giá trị bằng True cho lần lấy dữ liệu mới đầu tiên của chu kỳ,
    sau đó sẽ là False để mục đích hiệu chỉnh filter dữ liệu được nhanh hơn.
    :param is_create_new_file_tssl: Tạo file tỷ suất sinh lời mới.
    :param is_draw_chart: Vẽ chart
    :return: not return
    """
    start = time.time()
    time_name_type = get_time_name_with_type(time_type)
    if is_create_new_file_tssl:
        symbols_csv = get_all_symbol_in_file('../data/securities/AllSymbol.csv')
        symbols = symbols_csv['stockSymbol']
        Vndirect.mining_data_from_vndirect(symbols, time_units, time_type, is_first_call)

    symbols_csv = get_all_symbol_in_file(f'../data/TSSL_In_{time_units}_{time_name_type}.csv')
    symbols = symbols_csv['Symbol']
    # Chạy các mã vừa tìm được trong 1 đơn vị để có cái nhìn gần nhất về cổ phiếu.
    if time_units > 1 and time_type != TimeUnitsType.DAY:
        Vndirect.mining_data_from_vndirect(symbols, 1, time_type, False)

    end = time.time()
    print(f"Total run time: {round(end - start)}s")

    if is_draw_chart:
        plot_chart(symbols, time_units)


# Step 00
# build(time_units=1, time_type=TimeUnitsType.YEAR, is_first_call=True, is_create_new_file_tssl=True, is_draw_chart=False)

# Step 01
# build(time_units=6, time_type=TimeUnitsType.YEAR, is_first_call=True, is_create_new_file_tssl=True, is_draw_chart=False)

# Step 02: Vẽ chart theo số năm
# build(time_units=6, time_type=TimeUnitsType.YEAR, is_first_call=False, is_create_new_file_tssl=True, is_draw_chart=True)

# Step 03: Vẽ chart 1 năm
build(time_units=1, time_type=TimeUnitsType.YEAR, is_first_call=False, is_create_new_file_tssl=False, is_draw_chart=True)