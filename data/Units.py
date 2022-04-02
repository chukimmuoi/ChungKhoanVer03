from enum import Enum

from dateutil.relativedelta import relativedelta


class TimeUnitsType(Enum):
    YEAR = 250
    MONTH = 20
    WEEK = 5
    DAY = 1


def get_from_date_with_type(time_type, time_units):
    from_date = {
        TimeUnitsType.YEAR: relativedelta(years=time_units),
        TimeUnitsType.MONTH: relativedelta(months=time_units),
        TimeUnitsType.WEEK: relativedelta(weeks=time_units),
        TimeUnitsType.DAY: relativedelta(days=time_units)
    }

    return from_date.get(time_type, "Param Invalid")


def get_time_name_with_type(time_type):
    from_date = {
        TimeUnitsType.YEAR: "Year",
        TimeUnitsType.MONTH: "Month",
        TimeUnitsType.WEEK: "Week",
        TimeUnitsType.DAY: "Day"
    }

    return from_date.get(time_type, "Param Invalid")