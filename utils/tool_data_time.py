import calendar
import datetime
import time


class DateTimeTool:
    @classmethod
    def get_now_time(cls, format='%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(format)

    @classmethod
    def get_now_date(cls, format='%Y-%m-%d'):
        return datetime.date.today().strftime(format)

    @classmethod
    def get_now_time_stamp_with_second(cls):
        return int(time.time())

    @classmethod
    def get_now_time_stamp_with_millisecond(cls):
        return int(round(time.time() * 1000))

    @classmethod
    def timestamp_to_datetime(cls, timestamp: int, is_with_millisecond=False):
        if is_with_millisecond:
            timestamp = timestamp / 1000
        result_date_time = datetime.datetime.fromtimestamp(timestamp)
        return result_date_time

    @classmethod
    def str_to_timestamp(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S', is_with_millisecond=False):
        dst_datetime = datetime.datetime.strptime(str, str_format)
        if is_with_millisecond:
            timestamp = int(time.mktime(dst_datetime.timetuple()) * 1000)
        else:
            timestamp = int(time.mktime(dst_datetime.timetuple()))
        return timestamp

    @classmethod
    def get_week_day(cls):
        """
        获得今天星期几，从1开始
        :return:
        """
        return datetime.datetime.now().weekday() + 1

    @classmethod
    def get_how_days_ago(cls, now_datetime, now_datetime_format='%Y-%m-%d %H:%M:%S', how_days_ago=0):
        now_datetime = datetime.datetime.strptime(now_datetime, now_datetime_format)
        result_date_time = now_datetime - datetime.timedelta(days=how_days_ago)
        return result_date_time

    @classmethod
    def datetime_to_str(cls, the_datetime, format='%Y-%m-%d'):
        return the_datetime.strftime(format)

    @classmethod
    def str_to_datetime(cls, str, str_format: str = '%Y-%m-%d %H:%M:%S'):
        dst_datetime = datetime.datetime.strptime(str, str_format)
        return dst_datetime

    @classmethod
    def get_how_years_ago(cls, now_date, how_years_ago=0, now_date_format='%Y-%m-%d'):
        result_date = cls.get_how_days_ago(now_date, now_date_format, how_years_ago * 366)
        return result_date

    @classmethod
    def get_current_month_first_day_or_last_day(cls, type=1):
        """获取当前月第一天或者最后一天日期

        Args:
            type (int, optional): 第一天:1，最后一天:-1

        Returns:
            [type]: [description]
        """
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        last_day = calendar.monthrange(year, month)[1]
        if type == 1:
            start = datetime.date(year, month, 1)
            return start
        if type == -1:
            end = datetime.date(year, month, last_day)
            return end