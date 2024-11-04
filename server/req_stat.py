import logging
import subprocess
import pandas as pd

def get_stat():
    execute_test()
    STAT_FILE = '../log/results-tree-report.csv'
    stat = pd.read_csv(STAT_FILE)
    
    avg_latency = stat["Latency"].mean()
    stat_value_counts = stat.groupby("success")["success"].count()
    total_packet_count = len(stat)
    try:
        drop_packet_count = int(stat_value_counts.loc[False])
        drop_packet_percentage = stat_value_counts.loc[False]/total_packet_count*float(100)
    except KeyError:
        drop_packet_count = 0
        drop_packet_percentage = float(0)

    return {
        'avg_latency': avg_latency,
        'drop_packet_percentage': drop_packet_percentage,
        'drop_packet_count': drop_packet_count,
        'total_packet_count': total_packet_count
    }

def execute_test():
    JMETER_TEST_CMD = '''cmd /c "cd C:\\Users\\natni\\Downloads\\apache-jmeter-5.6.3\\bin && jmeter -f -n -t Thread-Group.jmx"'''
    p = subprocess.run(JMETER_TEST_CMD, shell=True, capture_output=True, text=True)
    logging.info(p)
