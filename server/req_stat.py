import pandas as pd

def get_stat(from_time :str, to_time: str):
    STAT_FILE = '../log/image_classify_stats_history.csv'
    stat = pd.read_csv(STAT_FILE)
    stat = stat.loc[(stat['Timestamp'] >= int(from_time)) & (stat['Timestamp'] <= int(to_time))]
    first = stat.head(1)
    last = stat.tail(1)
    print(stat)
    total_request_count = int(last['Total Request Count'].iat[0] - first['Total Request Count'].iat[0])
    total_failure_count = int(last['Total Failure Count'].iat[0] - first['Total Failure Count'].iat[0])
    return {
        'total_request_count': total_request_count,
        'total_failure_count': total_failure_count
    }