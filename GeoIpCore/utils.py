# build in
import datetime
import random
import secrets
from string import punctuation, digits, ascii_letters

# libs
import khayyam
from celery import Celery, Task
# framework
from flask import Flask, request


def user_real_ip() -> str:
    """ This Function returns users actual public IP address, base on ArvanCloud HTTP header

    according to arvancloud documentations `True-Client-Ip` http header contains users actual IP address 
    """
    return request.headers.get('True-Client-Ip', request.headers.get("Ar-Real-Ip", None))


def make_api_ip_cache_key(*args, **kwargs) -> str:
    """ every time an api view  called this function is calling
    and base on api url this function generate a unique key for that view 
    for searching in redis cache server
    """
    more = request.args.get("more", type=int, default=0)
    if more and more == 1:  # if ?more is passing
        return str(request.url)
    else:
        # base url path:
        # http://127.0.0.1:8080/api/v1/ipv4/128.45.45.2/?more=983->> http://127.0.0.1:8080/api/v1/ipv4/128.45.45.2/
        return str(request.path)


def generateRandomString(len_prob: int = 6) -> str:
    """This function generates random strings including punctuation number and ascii_letters
    #TODO:
        this function should act base on input flags
                    punctuation: bool = True, digits: bool = True,
                         ascii_letters: bool = True
    """
    token = [each for each in secrets.token_hex(80 * len_prob)]
    token += random.choices(punctuation, k=80)
    token += random.choices(digits, k=80)
    token += random.choices(ascii_letters, k=80)
    random.shuffle(token)
    return "".join(token)


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        """Every time a task is added to queue __call__ is called """

        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():  # under flask context
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.Task = FlaskTask
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


class TimeStamp:
    """
        a base class for working with time&times in app
        ~!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~!~
        #todo :
            utils
    """

    __now_gregorian = None
    __now_jalali = None
    __now_timestamp = None
    __now_time = None

    def __init__(self):
        # constructor method
        self.__now_jalali = self.now_jalali()
        self.__now_gregorian = self.now_gregorian()
        self.__now_timestamp = self.now_unixtime()
        self.__now_time = self.now_time()

    @property
    def time(self):
        """Return time That Object created"""
        return self.__now_time

    @property
    def gregorian(self):
        """Return Gregorian time That Object created"""
        return self.__now_gregorian

    @property
    def jalali(self):
        """Return Jalali time That Object created"""
        return self.__now_jalali

    @property
    def timestamp(self):
        """Return timestamp time That Object created"""
        return self.__now_timestamp

    @staticmethod
    def now_time():
        """this method return now time"""
        return datetime.datetime.now().time()

    @staticmethod
    def now_unixtime():
        """this method return now time in unix time"""
        return int(datetime.datetime.now().timestamp())

    @staticmethod
    def now_gregorian():
        """this method return now time in gregorian time"""
        return datetime.date.today()

    @staticmethod
    def now_jalali():
        """this method return now time in jalali format"""
        return khayyam.JalaliDate.today()

    @staticmethod
    def is_persian_date(date: str) -> bool:
        """
            This function take a  date in format of string
            and check its valid jalali persian date or not
        """
        date = date.split("/")
        if len(date) == 3:
            try:
                khayyam.JalaliDate(year=date[0], month=date[1], day=date[2])
            except Exception as e:
                return False
            else:
                return True

        return False

    def convert_jlj2_georgian_d(self, value: khayyam.JalaliDate):
        """
            this method get a khayyam date<jalali> and convert it to gregorian object datetime.date
        """
        if not isinstance(value, khayyam.JalaliDate):
            raise ValueError(f"input {value} must be a khayyam.JalaliDate instance")
        year, month, day = value.year, value.month, value.day
        date = self._jalali_to_gregorian(year, month, day)
        return datetime.date(year=date[0], month=date[1], day=date[2])

    def convert_grg2_jalali_d(self, value: datetime.date):
        """
            this method get a datetime.date object and convert it o khayyam object
        """
        if not isinstance(value, datetime.date):
            raise ValueError(f"input {value} - {type(value)} must be a Datetime.Date instance")

        year, month, day = value.year, value.month, value.day
        date = self._gregorian_to_jalali(year, month, day)
        return khayyam.JalaliDate(year=date[0], month=date[1], day=date[2])

    def convert_jlj2_georgian_dt(self, value: khayyam.JalaliDatetime):
        """
            this method get a khayyam date<jalali> and convert it to gregorian object datetime.datetime
        """
        if not isinstance(value, khayyam.JalaliDatetime):
            raise ValueError("input must be a khayyam.JalaliDatetime instance")

        year, month, day, hour, minute, second, microsecond = value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond
        date = self._jalali_to_gregorian(year, month, day)
        return datetime.datetime(year=date[0], month=date[1], day=date[2], hour=hour, minute=minute, second=second,
                                 microsecond=microsecond)

    def convert_grg2_jalali_dt(self, value: datetime.datetime):
        """
            this method get a datetime.date object and convert it o khayyam.KhayyamDatetime object
        """
        year, month, day, hour, minute, second, microsecond = value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond
        date = self._gregorian_to_jalali(year, month, day)
        return khayyam.JalaliDatetime(year=date[0], month=date[1], day=date[2], hour=hour, minute=minute, second=second,
                                      microsecond=microsecond)

    def _gregorian_to_jalali(self, gy, gm, gd):
        """
            this method convert a Gregorian to a Jalali date
            https://jdf.scr.ir/
        """
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if (gm > 2):
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if (days < 186):
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]

    def _jalali_to_gregorian(self, jy, jm, jd):
        """
            this method convert a Jalali time to a Gregorian time
            https://jdf.scr.ir/
        """
        jy += 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
        if (jm < 7):
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186
        gy = 400 * (days // 146097)
        days %= 146097
        if (days > 36524):
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
            if (days >= 365):
                days += 1
        gy += 4 * (days // 1461)
        days %= 1461
        if (days > 365):
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
        gd = days + 1
        if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            kab = 29
        else:
            kab = 28
        sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while (gm < 13 and gd > sal_a[gm]):
            gd -= sal_a[gm]
            gm += 1
        return [gy, gm, gd]

    def convert_string_jalali2_dateD(self, value: str) -> datetime.date:
        """
            this Method converts a string (Persian Date) to datetime.date object
        """
        if not self.is_persian_date(value):
            raise ValueError("Input is not a valid date format YYYY/MM/DD")

        value = value.split("/")
        jDate = khayyam.JalaliDate(year=value[0], month=value[1], day=value[2])
        return self.convert_jlj2_georgian_d(jDate)

    def bigger_date(self, date1, date2):
        """
           this method takes two dates and returns the biggest date
            :params: date1, date2
            - if both dates are equal return True
            - if date1 is biggest return date1
            - if date2 is biggest return date2
        """
        if date1 > date2:
            return date1
        elif date2 > date1:
            return date2
        else:
            return True

    def smaller_date(self, date1, date2):
        """
            this method takes two dates and returns the smallest date
            :params: date1, date2
            - if both dates are equal return True
            - if date1 is smallest return date1
            - if date2 is smallest return date2
        """
        if date1 < date2:
            return date1
        elif date2 < date1:
            return date2
        else:
            return True
