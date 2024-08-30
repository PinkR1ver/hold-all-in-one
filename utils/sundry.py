from datetime import datetime

def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')