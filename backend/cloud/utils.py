from email.utils import parsedate_to_datetime
from datetime import datetime
import pytz

def convert_to_date(date_str):
    # RFC 2822 형식의 문자열을 datetime.datetime 객체로 변환
    dt = parsedate_to_datetime(date_str)
    # 시간대를 UTC로 설정하고, 날짜 부분만 추출
    return dt.astimezone(pytz.utc).date()

