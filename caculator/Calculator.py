import pandas as pd
import numpy as np

from caculator.Filter import isVolumeMinFilter, isSymbolExistYear, AD_CLOSE_COLUMN, MIN_ROW, MAX_ROW, COUNT_ROW, \
    MEAN_ROW, STD_ROW, NM_VOLUME_COLUMN, isVolumeGood
from data.Units import get_time_name_with_type

SYMBOL_COLUMN = 'Symbol'
COUNT_YEAR_COLUMN = 'Count {time_units}'
FROM_COLUMN = 'From'
TO_COLUMN = 'To'
MIN_COLUMN = 'Min'
MAX_COLUMN = 'Max'
MEAN_PRICE_COLUMN = 'Mean Price'
STD_PRICE_COLUMN = 'STD Price'
MEAN_VOLUME_COLUMN = 'Mean Volume'
STD_VOLUME_COLUMN = 'STD Volume'
percent_text_format = "{:,.2f}"
percent_number_format = "{percent:.2f}"
column_format = "{time_units} {n}"
FULL_COLUMN = "Full"


def create_percent(code, data_frame, n, time_type):
    """
    Lấy tỷ suất sinh lời theo từng giai đoạn dựa vào data truyền vào
    :param code: mã chứng khoán
    :param data_frame: dữ liệu giao dịch của mã chứng khoán
    :param n: Chu kỳ, thường là số năm
    :param time_type: Loại đơn vị thời gian
    :return: data frame chứa thông tin tỷ suất sinh lời theo từng giai đoạn
    """
    data_describe = data_frame.describe()
    if isVolumeMinFilter(data_describe):
        return

    if not isSymbolExistYear(data_describe, 1, time_type):
        return

    if not isVolumeGood(data_describe):
        return

    df_output = pd.DataFrame(columns=[SYMBOL_COLUMN])
    df_output = df_output.append({SYMBOL_COLUMN: code}, ignore_index=True)

    count_time_not_round = addCountTimeColumn(data_describe, df_output, time_type)
    count_time_round = round(count_time_not_round)
    from_value = addFromColumn(data_frame, df_output)
    to_value = addToColumn(data_frame, df_output)
    min_price_value = addMinColumn(data_describe, df_output)
    max_price_value = addMaxColumn(data_describe, df_output)
    mean_price_value = addMeanPriceColumn(data_describe, df_output)
    std_price_value = addStdPriceColumn(data_describe, df_output)
    mean_volume_value = addMeanVolumeColumn(data_describe, df_output)
    std_volume_value = addStdVolumeColumn(data_describe, df_output)

    n = min(n, count_time_round)
    maps = create_new_data(data_frame, n, count_time_not_round)
    for key, value in maps.items():
        percent = float(percent_number_format.format(percent=value))
        # if percent <= 10:  # Loại bỏ cổ phiếu có phần trăm tăng trưởng trong 1 chu kỳ nhỏ hơn 10
        #     return

        year = column_format.format(
            time_units=get_time_name_with_type(time_type),
            n=key
        )
        df_output[year] = percent

        if key == FULL_COLUMN:
            key_percent = percent

    # if key_percent <= 20:  # Loại bỏ cổ phiếu có phần trăm tăng trưởng trong toàn chu kỳ nhỏ hơn 20
    #     return

    return df_output


def create_new_data(data_frame, n, count_year_not_round):
    """
    Tách dữ liệu theo từng chu kỳ để tính toán tỷ suất sinh lời
    :param data_frame: tất cả dữ liệu của mã chứng khoán
    :param n: chu kỳ
    :param count_year_not_round: chu kỳ không làm tròn, dùng để tính chính xác nhất tỷ suất sinh lời
    :return: map tên chu kỳ và phần trăm tỷ suất sinh lời trong chu kỳ đó
    """
    output = {}
    fv = float(data_frame.head(1)[AD_CLOSE_COLUMN].to_string(index=False))
    pv = float(data_frame.tail(1)[AD_CLOSE_COLUMN].to_string(index=False))
    full_data = calculator(fv, pv, count_year_not_round)

    dfs = np.array_split(data_frame, n, axis=0)
    for index in range(n):
        df = dfs[index]
        pv = float(df.tail(1)[AD_CLOSE_COLUMN].to_string(index=False))
        n_split = index + 1
        output[n_split] = calculator(fv, pv, n_split)

    output[FULL_COLUMN] = full_data

    return output


def calculator(fv, pv, n=1):
    """
    Công thức tính tỷ suất sinh lời theo chu kỳ
    :param fv: giá trị tương lai
    :param pv: giá trị hiện tại
    :param n: chu kỳ, thường tính theo năm
    :return: phần trăm sinh lời
    """
    r = ((fv / pv) ** (1 / n) - 1) * 100
    return r


def addCountTimeColumn(data_describe, df_output, time_type):
    """
    Thêm cột đếm số thời gian tồn tại của cổ phiếu
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :param time_type: Loại đơn vị thời gian
    :return:
    """
    count_year = float(
        percent_number_format.format(
            percent=data_describe[AD_CLOSE_COLUMN][COUNT_ROW] / time_type.value
        )
    )
    count_name_column = COUNT_YEAR_COLUMN.format(time_units=get_time_name_with_type(time_type))
    df_output[count_name_column] = count_year
    return count_year


def addFromColumn(data_frame, df_output):
    """
    Thêm cột giá trị đầu tiên của cổ phiếu trong chu kỳ
    :param data_frame: dữ liệu của mã chứng khoán trong 1 chu kỳ
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    from_value = float(
        percent_number_format.format(
            percent=float(data_frame.tail(1)[AD_CLOSE_COLUMN].to_string(index=False))
        )
    )
    df_output[FROM_COLUMN] = from_value
    return from_value


def addToColumn(data_frame, df_output):
    """
    Thêm cột giá trị cuối cùng của cổ phiếu trong chu kỳ
    :param data_frame: dữ liệu của mã chứng khoán trong 1 chu kỳ
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    to_value = float(
        percent_number_format.format(
            percent=float(data_frame.head(1)[AD_CLOSE_COLUMN].to_string(index=False))
        )
    )
    df_output[TO_COLUMN] = to_value
    return to_value


def addMinColumn(data_describe, df_output):
    """
    Thêm cột giá trị nhỏ nhất của cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    min_value = float(
        percent_number_format.format(
            percent=data_describe[AD_CLOSE_COLUMN][MIN_ROW]
        )
    )
    df_output[MIN_COLUMN] = min_value
    return min_value


def addMaxColumn(data_describe, df_output):
    """
    Thêm cột giá trị lớn nhất của cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    max_value = float(
        percent_number_format.format(
            percent=data_describe[AD_CLOSE_COLUMN][MAX_ROW]
        )
    )
    df_output[MAX_COLUMN] = max_value
    return max_value


def addMeanPriceColumn(data_describe, df_output):
    """
    Thêm cột giá trị trung bình của giá cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    mean_value = float(
        percent_number_format.format(
            percent=data_describe[AD_CLOSE_COLUMN][MEAN_ROW]
        )
    )
    df_output[MEAN_PRICE_COLUMN] = mean_value
    return mean_value


def addStdPriceColumn(data_describe, df_output):
    """
    Thêm cột độ lệch chuẩn của giá cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    std_value = float(
        percent_number_format.format(
            percent=data_describe[AD_CLOSE_COLUMN][STD_ROW]
        )
    )
    df_output[STD_PRICE_COLUMN] = std_value
    return std_value


def addMeanVolumeColumn(data_describe, df_output):
    """
    Thêm cột giá trị trung bình của Volume cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    mean_value = float(
        percent_number_format.format(
            percent=data_describe[NM_VOLUME_COLUMN][MEAN_ROW]
        )
    )
    df_output[MEAN_VOLUME_COLUMN] = mean_value
    return mean_value


def addStdVolumeColumn(data_describe, df_output):
    """
    Thêm cột độ lệch chuẩn của Volume cổ phiếu trong chu kỳ
    :param data_describe: data thông tin tổng quan của dữ liệu.
    :param df_output: data thông tin của mã chứng khoán sau tính toán (1 row trong file csv output)
    :return:
    """
    std_value = float(
        percent_number_format.format(
            percent=data_describe[NM_VOLUME_COLUMN][STD_ROW]
        )
    )
    df_output[STD_VOLUME_COLUMN] = std_value
    return std_value