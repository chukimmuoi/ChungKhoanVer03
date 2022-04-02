from urllib.request import urlopen, Request
import ssl
import json
import pandas
from pathlib import Path
from datetime import datetime
import pandas as pd
from caculator.Calculator import create_percent, SYMBOL_COLUMN, column_format, FULL_COLUMN, MEAN_VOLUME_COLUMN, \
    STD_VOLUME_COLUMN, percent_text_format

# SSL certificate.
from data.Units import get_from_date_with_type, get_time_name_with_type

ssl._create_default_https_context = ssl._create_unverified_context

VN_DIRECT_COM_VN = "https://finfo-api.vndirect.com.vn/v4/stock_prices?"
PATH_FORMAT = "../data/symbol/{}_{}"
PATH_FULL_FORMAT = "../data/symbol/{}_{}/{}.csv"
TSSL_NAME_FORMAT = "TSSL_In_{}_{}.csv"


def mining_data_from_vndirect(symbols, time_units, time_type, is_online=False):
    """
    Mining data từ thời điểm hiện tại đến thời điểm from_year
    :param time_units: Số năm, tháng, tuần, ngày, cụ thể là số năm, tháng, tuần, ngày trước ngày hiện tại
    :param time_type: Loại đơn vị thời gian
    :param is_online: Dùng dữ liệu online hay offline, tiết kiệm thời gian và băng thông mạng.
    Chỉ nên để là True trong trường hợp muốn lấy giá trị mới nhất.
    :return: Danh sách các file csv được tạo trong folder symbol và file tỷ suất sinh lời.
    """
    df_sum = pd.DataFrame(columns=[SYMBOL_COLUMN])
    for code in symbols:
        print(code)
        if is_online:
            path = getSymbolData(
                code,
                time_units,
                time_type
            )
        else:
            path = PATH_FULL_FORMAT.format(
                time_units,
                get_time_name_with_type(
                    time_type
                ),
                code
            )

        if path:
            if Path(path).exists():
                df = pd.read_csv(path)
                row = create_percent(code, df, time_units, time_type)
                df_sum = df_sum.append(row)

    df_sum = df_sum.sort_values(
        by=[
            # MEAN_VOLUME_COLUMN,
            column_format.format(
                time_units=get_time_name_with_type(time_type),
                n=FULL_COLUMN
            )
        ],
        ascending=False,
        ignore_index=True
    )

    formatVolumeBeforeSaveCSV(df_sum)
    df_sum.to_csv(
        TSSL_NAME_FORMAT.format(
            time_units,
            get_time_name_with_type(
                time_type
            )
        )
    )


def formatVolumeBeforeSaveCSV(df_sum):
    """
    Định dạng lại 2 cột chứa giá trị volume giao dịch để hiển thị cho dễ nhìn.
    :param df_sum: Dữ liệu trước khi được format.
    :return:
    """
    df_sum[MEAN_VOLUME_COLUMN] = df_sum[MEAN_VOLUME_COLUMN].map(percent_text_format.format)
    df_sum[STD_VOLUME_COLUMN] = df_sum[STD_VOLUME_COLUMN].map(percent_text_format.format)
    return df_sum


def get_all_symbol_in_file(path):
    """
    Lấy danh sách mã chứng khoán Việt Nam từ file csv. Ex: data/securities/AllSymbol.csv
    :param path: Đường dẫn đến file csv lưu tất cả mã chứng khoán Việt Nam
    :return: Danh sách mã chững khoán [MWG, HPG, TPB,...]
    """
    all_symbol = pandas.read_csv(path, index_col=None)
    return all_symbol


def getSymbolData(code, time_units, time_type):
    """
    Lấy dữ liệu của một mã chứng khoản từ thời điểm from_year đến ngày hiện tại
    :param code: Mã chứng khoán của một công ty. Ex: MWG
    :param time_units: Số năm, tháng, tuần, ngày cụ thể là sô năm, tháng, tuần, ngày trước ngày hiện tại
    :param time_type: Loại đơn vị thời gian
    :return: Một path file csv chứa đầy đủ thông tin mã chứng khoán theo từng ngày làm việc
    """
    from_date = get_from_date_with_unit(time_units=time_units, time_type=time_type)
    url = get_url(code, from_date)
    json_string = get_json_from_url(url)
    panda = convert_json_to_pandas(json_string)
    if panda.empty:
        return ""
    else:
        return save_pandas_to_csv(
            panda,
            code,
            PATH_FORMAT.format(
                time_units,
                get_time_name_with_type(
                    time_type
                )
            )
        )


def get_from_date_with_unit(time_units, time_type):
    """
    Lấy ra ngày bắt đầu dựa vào ngày hiện tại và số năm (year)
    :param time_units: Số năm, tháng, tuần, ngày
    :param time_type: Loại đơn vị thời gian
    :return: Ngày bắt đầu lấy dữ liệu
    """
    current_date = datetime.today()
    from_date = current_date - get_from_date_with_type(time_type, time_units)
    from_date_string = from_date.strftime('%Y-%m-%d')
    return from_date_string


def get_url(code, from_date=datetime.today().strftime('%Y-%m-%d'), to_date=datetime.today().strftime('%Y-%m-%d')):
    """
    Tạo URL để sử dụng API của VnDirect
    :param code: Mã chứng khoán của công ty bất kỳ. Ex: MWG
    :param from_date: Ngày bắt đầu mining
    :param to_date: Ngày kết thúc mining
    :return: Đường dẫn API để truy vấn data từ server
    """
    query = "{VNDIRECT}sort=date&q=code:{code}~date:gte:{from_date}~date:lte:{to_date}&size={size}&page=1"
    query = query.format(
        VNDIRECT=VN_DIRECT_COM_VN,
        code=code,
        from_date=from_date,
        to_date=to_date,
        size=calculator_size(from_date, to_date)
    )
    print(query)
    return query


def calculator_size(from_date, to_date):
    """
    Đếm số ngày từ ngày bắt đầu đến ngày kết thúc.
    Mục đích nhằm lấy hết data của khoảng thời gian này trong 1 lần truy vấn duy nhất
    :param from_date: Ngày bắt đầu
    :param to_date: Ngày kết thúc
    :return: Số ngày từ ngày bắt đầu đến ngày kết thúc
    """
    size = convert_string_date(to_date) - convert_string_date(from_date)
    return size.days


def convert_string_date(date_string):
    """
    Đổi định dạng string về date
    Định dạng dữ liệu string của ngày là:YYYY-mm-dd để cho phù hợp với yêu cầu của API VnDirect
    :param date_string:
    :return: date
    """
    date = datetime.strptime(date_string, '%Y-%m-%d')
    return date


def get_json_from_url(url):
    """
    Truy vấn data với API được cung cấp
    :param url: link API
    :return: Dữ liệu dưới dạng json
    """
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # request = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
    response = urlopen(request)
    data_json = json.loads(response.read())['data']
    return data_json


def convert_json_to_pandas(json_string):
    """
    Chuyển đổi json sang dạng bảng Pandas
    :param json_string: Dữ liệu chứng khoán
    :return: Data pandas
    """
    result = pandas.DataFrame(json_string)
    return result


def create_directory(directory):
    """
    Tạo thư mục nếu nó chưa tồn tại
    :param directory: Địa chỉ, đường dẫn
    :return: thư mục được tạo nếu chưa tồn tại
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def save_pandas_to_csv(result, name_code, out_directory):
    """
    Lưu dữ liệu dạng bảng Pandas thành file csv.
    :param result: Dữ liệu kiểu Pandas
    :param name_code: Mã công ty
    :param out_directory: Thư mục lưu file
    :return: File path csv được tạo mới và lưu trong out_directory
    """
    create_directory(out_directory)

    full_path = out_directory + '/' + name_code + ".csv"
    result.to_csv(full_path, index=False)

    return full_path