DOLA_VALUE = 24_000


def muc_tieu(lam_phat, so_ky):
    muc_tieu = DOLA_VALUE * 1_000_000 * (1 + (lam_phat / 100)) ** so_ky
    print('Muc tieu nam {} la: {}'.format(2020 + so_ky, '{:20,.0f}'.format(muc_tieu)))
    return muc_tieu


def dau_tu(so_tien_ban_dau, so_tien_bo_sung_hang_nam, phan_tram_lai, so_ky):
    tong_tien = 0
    for nam in range(so_ky):
        n = so_ky - nam
        if nam == 0:
            so_tien = so_tien_ban_dau * (1 + (phan_tram_lai / 100)) ** n
            # print('So tien {} dau tu sau {} nam la: {}'.format('{:20,.0f}'.format(so_tien_ban_dau), n, '{:20,.0f}'.format(so_tien)))
        else:
            so_tien = so_tien_bo_sung_hang_nam * (1 + (phan_tram_lai / 100)) ** n
            # print('So tien {} dau tu sau {} nam la: {}'.format('{:20,.0f}'.format(so_tien_bo_sung_hang_nam), n, '{:20,.0f}'.format(so_tien)))

        tong_tien += so_tien
    print('\n')
    muc_tieu(3, so_ky)
    print('Tong tai san dau tu nam {} la: {}'.format(2020 + so_ky, '{:20,.0f}'.format(tong_tien)))


so_nam_dau_tu = 16
for x in range(so_nam_dau_tu):
    dau_tu(300_000_000, 100_000_000, 30, x + 1)

# Muc tieu nam 2021 la:            24,720,000,000
# Tong tai san dau tu nam 2021 la:    390,000,000
#
#
# Muc tieu nam 2022 la:            25,461,600,000
# Tong tai san dau tu nam 2022 la:    637,000,000
#
#
# Muc tieu nam 2023 la:            26,225,448,000
# Tong tai san dau tu nam 2023 la:    958,100,000
#
#
# Muc tieu nam 2024 la:            27,012,211,440
# Tong tai san dau tu nam 2024 la:  1,375,530,000
#
#
# Muc tieu nam 2025 la:            27,822,577,783
# Tong tai san dau tu nam 2025 la:  1,918,189,000
#
#
# Muc tieu nam 2026 la:            28,657,255,117
# Tong tai san dau tu nam 2026 la:  2,623,645,700
#
#
# Muc tieu nam 2027 la:            29,516,972,770
# Tong tai san dau tu nam 2027 la:  3,540,739,410
#
#
# Muc tieu nam 2028 la:            30,402,481,953
# Tong tai san dau tu nam 2028 la:  4,732,961,233
#
#
# Muc tieu nam 2029 la:            31,314,556,412
# Tong tai san dau tu nam 2029 la:  6,282,849,603
#
#
# Muc tieu nam 2030 la:            32,253,993,104
# Tong tai san dau tu nam 2030 la:  8,297,704,484
#
#
# Muc tieu nam 2031 la:            33,221,612,897
# Tong tai san dau tu nam 2031 la: 10,917,015,829
#
#
# Muc tieu nam 2032 la:            34,218,261,284
# Tong tai san dau tu nam 2032 la: 14,322,120,578
#
#
# Muc tieu nam 2033 la:            35,244,809,123
# Tong tai san dau tu nam 2033 la: 18,748,756,751
#
#
# Muc tieu nam 2034 la:            36,302,153,397
# Tong tai san dau tu nam 2034 la: 24,503,383,776
#
#
# Muc tieu nam 2035 la:            37,391,217,998
# Tong tai san dau tu nam 2035 la: 31,984,398,909
#
#
# Muc tieu nam 2036 la:            38,512,954,538
# Tong tai san dau tu nam 2036 la: 41,709,718,582