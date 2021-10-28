BASIC_PRICE_COLUMN = 'basicPrice'
CEILING_PRICE_COLUMN = 'ceilingPrice'
FLOOR_PRICE_COLUMN = 'floorPrice'
OPEN_COLUMN = 'open'
HIGH_COLUMN = 'high'
#         basicPrice  ceilingPrice   floorPrice         open         high
# count  1250.000000   1250.000000  1250.000000  1250.000000  1250.000000
# mean     36.671960     39.210080    34.131680    36.833760    37.337160
# std      11.915042     12.741909    11.085949    11.698081    11.910301
# min       0.000000      0.000000     0.000000    15.300000    16.700000
# 25%      27.050000     28.900000    25.200000    27.362500    27.712500
# 50%      35.500000     37.950000    33.050000    35.600000    36.175000
# 75%      43.450000     46.450000    40.450000    43.500000    44.187500
# max      67.800000     72.500000    63.100000    67.700000    67.800000
LOW_COLUMN = 'low'
CLOSE_COLUMN = 'close'
AVERAGE_COLUMN = 'average'
AD_OPEN_COLUMN = 'adOpen'
AD_HEIGHT_COLUMN = 'adHigh'
#                low       close      average       adOpen       adHigh
# count  1250.000000  1250.00000  1250.000000  1250.000000  1250.000000
# mean     36.387080    36.87624    36.858460    19.681696    19.954139
# std      11.512375    11.73404    11.710957    12.086959    12.260929
# min      15.250000    16.20000    15.890000     8.148000     8.148000
# 25%      26.950000    27.30000    27.322500    12.889000    13.049000
# 50%      35.250000    35.60000    35.765000    15.430500    15.639000
# 75%      43.150000    43.60000    43.642500    19.873250    20.169750
# max      67.200000    67.80000    67.470000    58.000000    58.400000
AD_LOW_COLUMN = 'adLow'
AD_CLOSE_COLUMN = 'adClose'
AD_AVERAGE_COLUMN = 'adAverage'
NM_VOLUME_COLUMN = 'nmVolume'
NM_VALUE_COLUMN = 'nmValue'
#              adLow      adClose    adAverage      nmVolume       nmValue
# count  1250.000000  1250.000000  1250.000000  1.250000e+03  1.250000e+03
# mean     19.438499    19.703574    19.696291  9.808143e+06  3.983768e+11
# std      11.923237    12.095620    12.100376  9.473026e+06  4.850331e+11
# min       8.014000     8.106000     8.079000  9.073400e+05  3.829793e+10
# 25%      12.784000    12.871500    12.921500  3.652642e+06  1.180096e+11
# 50%      15.258000    15.454000    15.442000  5.710305e+06  1.912701e+11
# 75%      19.499000    19.887000    19.875250  1.277434e+07  4.071835e+11
# max      57.500000    58.000000    58.050000  7.550030e+07  3.372000e+12
PT_VOLUME_COLUMN = 'ptVolume'
PT_VALUE_COLUMN = 'ptValue'
CHANGE_COLUMN = 'change'
AD_CHANGE_COLUMN = 'adChange'
PCT_CHANGE_COLUMN = 'pctChange'
#            ptVolume       ptValue       change     adChange    pctChange
# count  1.250000e+03  1.250000e+03  1250.000000  1250.000000  1250.000000
# mean   5.475234e+05  2.029757e+10     0.062400     0.038040     0.170105
# std    1.193651e+06  4.613910e+10     0.837673     0.502199     2.055713
# min    0.000000e+00  0.000000e+00    -4.600000    -3.200000    -6.989200
# 25%    0.000000e+00  0.000000e+00    -0.300000    -0.138800    -0.907550
# 50%    1.664000e+05  5.423826e+09     0.050000     0.016000     0.114250
# 75%    6.992500e+05  2.292752e+10     0.450000     0.198300     1.188725
# max    2.430748e+07  8.210836e+11     3.900000     3.350000     6.868700
COUNT_ROW = 'count'
MEAN_ROW = 'mean'  # Giá trị trung bình
STD_ROW = 'std'    # Độ lệch chuẩn: dùng để đo mức độ phân tán của một tập dữ liệu đã được lập thành bảng tần số. Khi
                   # hai tập dữ liệu có cùng giá trị trung bình cộng, tập nào có độ lệch chuẩn lớn hơn là tập có
                   # dữ liệu biến thiên nhiều hơn.
MIN_ROW = 'min'    # Giá trị nhỏ nhất
_25_ROW = '25%'    # 25% giá trị nằm trong khoảng từ 0 đến bao nhiêu đó ..
_50_ROW = '50%'    # 50% giá trị nằm trong khoảng từ 0 đến bao nhiêu đó ..
_75_ROW = '75%'    # 75% giá trị nằm trong khoảng từ 0 đến bao nhiêu đó ..
MAX_ROW = 'max'    # Giá trị lớn nhất

COUNT_GD_IN_YEAR_CONSTANT = 250
VOLUME_GOOD_CONSTANT = 100000


def isVolumeMinFilter(data_describe):
    """
    Kiểm tra volume của mã cổ phiếu cố tốt hay không?
    Cổ phiếu có volume giao dịch lớn chứng tỏ tính thanh khoản tốt, nhiều người quan tâm.
    :param data_describe: Thông tin tổng quan có được từ bảng dữ liệu của mã cổ phiếu
    (min, 25%, 50%, 75% and max, ...)
    :return: giá trị cho biết mã cổ phiếu có volume tốt hay không False là Tốt, True là không tốt.
    """
    isVolumeMin = data_describe[NM_VOLUME_COLUMN][_25_ROW] <= 0 \
                  or data_describe[NM_VOLUME_COLUMN][_50_ROW] <= 0 \
                  or data_describe[NM_VOLUME_COLUMN][_75_ROW] <= 0

    return isVolumeMin


def isSymbolExistYear(data_describe, year):
    """
    Kiểm tra mã cổ phiếu đã được giao dịch trên sàn chứng khoán trong khoảng thời gian nhất định
    (ở đây là năm)
    :param data_describe: Thông tin tổng quan có được từ bảng dữ liệu của mã cổ phiếu
    (min, 25%, 50%, 75% and max, ...)
    :param year: số năm tối thiểu cần có.
    :return: True nếu cổ phiếu tồn tại lớn hơn số năm yêu cầu, ngược lại là False không đủ điều kiện.
    """
    isExist = data_describe[AD_CLOSE_COLUMN][COUNT_ROW] >= year * COUNT_GD_IN_YEAR_CONSTANT - 1
    return isExist


def isVolumeGood(data_describe):
    """
    Kiểm tra Mã cổ phiếu có volume tốt hay không?
    :param data_describe: Thông tin tổng quan có được từ bảng dữ liệu của mã cổ phiếu
    (min, 25%, 50%, 75% and max, ...)
    :return: True nếu volume lớn hơn giới hạn yêu cầu, ngược lại sẽ trả ra False
    """
    isGood = data_describe[NM_VOLUME_COLUMN][MEAN_ROW] >= VOLUME_GOOD_CONSTANT
    return isGood
