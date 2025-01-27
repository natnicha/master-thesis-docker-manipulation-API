import datetime
import logging
import time
import pandas as pd

import containers


def collect_metrics():
  metrics = pd.DataFrame({"timestamp": pd.Series(dtype='datetime64[ns]'), 
                          "cpu_pct": pd.Series(dtype='float'), 
                          "mem_pct": pd.Series(dtype='float'),
                          "online_pods": pd.Series(dtype='int'),
                          "total_pods": pd.Series(dtype='int')})
  pd.read_csv("metrics.csv")
  start_time = datetime.datetime.now()
  timeout_minute = 25
  timeout = start_time + datetime.timedelta(0,0,0,0,float(timeout_minute)) 
  logging.info(f"timeout: {timeout}")
  collected_time = start_time
  while collected_time < timeout :
    collected_time = datetime.datetime.now()
    try:
      containers_info = containers.get_containers_info()
    except Exception as e:
      logging.info(str(e))
      continue

    logging.info(containers_info["system"])
    if containers_info["system"]["online_pods"] == None:
      metrics.loc[0] = [collected_time, None, None, None, containers_info["system"]["total_pods"]]
    else:
      metrics.loc[0] = [collected_time, round(containers_info["system"]["cpu_percent"], 6), round(containers_info["system"]["mem_percent"], 6), containers_info["system"]["online_pods"], containers_info["system"]["total_pods"]]
    metrics.to_csv("metrics.csv", mode='a', index=False, encoding='utf-8', header=False)
    time.sleep(0.2)
