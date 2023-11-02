#print("load time")

def FormatDuration(seconds:int) -> str:
    import time

    return time.strftime("%H:%M:%S", time.gmtime(seconds))

def Now() -> float:
    import time

    return time.time()

def Sleep(num:int=0, title:str=None, bar:bool=None):
    """
    Sleep(num:int, bar:bool=None)
    
    The first argument is an integer, and the second argument is a boolean. The second argument is
    optional, and if it is not provided, it will be set to True if the first argument is greater than 5,
    and False otherwise
    
    :param num: The number of seconds to sleep
    :type num: int
    :param bar: If True, a progress bar will be displayed. If False, no progress bar will be displayed.
    If None, a progress bar will be displayed if the number of seconds is greater than 5
    :type bar: bool
    """

    import time

    if num == 0:
        while True:
            time.sleep(333)
    else:
        if bar == None:
            if num > 5:
                bar = True 
            else:
                bar = False

        if bar:
            import tqdm

            num = int(num)
            for _ in tqdm.tqdm(range(num), total=num, leave=False, desc=title):
                time.sleep(1)
        else:
            time.sleep(num)

def Strftime(timestamp:float|int, format:str="%Y-%m-%d %H:%M:%S") -> str:
    """
    It converts a timestamp to a string.
    
    :param format: The format string to use
    :type format: str
    :param timestamp: The timestamp to format
    :type timestamp: float|int
    :return: A string
    """
    import datetime

    dobj = datetime.datetime.fromtimestamp(timestamp)
    return dobj.strftime(format)

def parseTimeago(timestring:str) -> int|None:
    from ..String import String

    if timestring == "just now":
        return int(Now())
    
    res = String(timestring).RegexFind('([0-9]+)([smhdw])')
    # print(res)
    if len(res) != 0:
        sm = {
            "s": "second",
            "m": "minute",
            "h": "hour",
            "d": "day",
            "w": "week",
        }
        timestring = res[0][1] + " " + sm[res[0][2]] + " ago"

    formates = [
        "([0-9]+) %ss{0,1} ago",
        "in ([0-9]+) %ss{0,1}",
        "([0-9]+) %s\. ago"
    ]

    step = {
        "second": 1,
        "minute": 60,
        "hour": 3600,
        "day": 86400,
        "week": 604800,
        "month": 2592000,
        "mo": 2592000,
        "year": 31536000,
        "yr": 31536000,
    }

    for s in step:
        for f in formates:
            f = f % s 

            res = String(timestring).RegexFind(f)
            if len(res) != 0:
                duration = step[s]
                num = int(res[0][1])

                return int(Now()) - duration * num 
    
    return None

def Strptime(timestring:str, format:str=None) -> int:
    """
    It takes a string of a date and time, and a format string, and returns the Unix timestamp of that
    date and time
    
    :param format: The format of the timestring
    :type format: str
    :param timestring: The string to be converted to a timestamp
    :type timestring: str
    :return: The timestamp of the datetime object.
    """

    from dateutil.parser import parse as dateparser
    from dateutil.parser import ParserError
    from ..String import String
    import datetime

    if format:
        dtimestamp = datetime.datetime.strptime(timestring, format).timestamp()
    else:
        if len(String(timestring).RegexFind('([0-9]+)([smhdw])')) != 0:
            dtimestamp = parseTimeago(timestring)
            if not dtimestamp:
                raise Exception(f"不能解析时间字符串: {timestring}")
        else:
            try:
                dtimestamp = dateparser(timestring).timestamp()
            except ParserError as e:
                dtimestamp = parseTimeago(timestring)
                if not dtimestamp:
                    raise Exception(f"不能解析时间字符串: {timestring}")

    return int(round(dtimestamp))

def DailyTimeBetween(start:str="00:00:00", end:str="07:00:00", now:float|int|str=None) -> bool:
    """
    This function checks if a given time falls between a start and end time.
    
    :param start: A string representing the starting time of a daily time interval in the format
    "HH:MM:SS", defaults to 00:00:00
    :type start: str (optional)
    :param end: The "end" parameter is a string representing the end time of a daily time interval in
    the format "HH:MM:SS". It defaults to "07:00:00", defaults to 07:00:00
    :type end: str (optional)
    :param now: The current time in either a string format (e.g. "12:30:00") or a float/int format
    representing the number of seconds since the epoch (e.g. 1612345678.0)
    :type now: float|int|str
    :return: a boolean value indicating whether the current time (represented by the `now` parameter) is
    between the start and end times (represented by the `start` and `end` parameters).
    """
    starttimestamp = Strptime(start)
    endtimestamp = Strptime(end)
    if type(now) == str:
        now = Strptime(now)
    elif now == None:
        now = Now()

    if endtimestamp < starttimestamp:
        endtimestamp += 86400

    return starttimestamp < now and now < endtimestamp

if __name__ == "__main__":
    # print(Strptime("2022-05-02 23:34:10", "%Y-%m-%d %H:%M:%S"))
    # print(Strftime(1651520050, "%Y-%m-%d %H:%M:%S"))
    # print(Strftime(Now()))
    # print(Strptime("2017-05-16T04:28:13.000000Z"))

    # print(Strptime("6 months ago"))
    # print(Strftime(Strptime("6 months ago")))
    # print(Strptime("just now"))
    # print(Strftime(Strptime("just now")))
    # print(Strptime("1 second ago"))
    # print(Strftime(Strptime("1 second ago")))
    # print(Strptime("in 24 days"))
    # print(Strftime(Strptime("in 24 days")))

    # print(FormatDuration(1750))
    # print(Strftime(Strptime("4m"))) # 4分钟前
    # print(Strftime(Strptime("2h"))) # 2小时前

    print(Strftime(Strptime("3 mo. ago"))) # 3个月前
    print(Strftime(Strptime("3 yr. ago"))) # 3年前