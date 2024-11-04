import os
from venv import create
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

scopes = ["https://www.googleapis.com/auth/yt-analytics.readonly"]

api_service_name='y4outubeAnalytic'
api_version='v2'
client_secrets_file = 'te.json'

def get_service():
    flow=InstalledAppFlow.from_client_secrets_file(client_secrets_file,scopes)
    credentials = flow.run_local_server()
    return build(api_service_name,api_version,credentials=credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()
  return response

def create_table(table, headers=None):
    if headers:
        headerstring = "\t{}\t" * len(headers)
        print(headerstring.format(*headers))

    rowstring = "\t{}\t" * len(table[0])

    for row in table:
        print(rowstring.format(*row))

if __name__ == '__main__':
    youtubeAnalytics = get_service()
    result = execute_api_request(
        youtubeAnalytics.reports().query,
        ids='channel==UCgp3M3NC_5J-CbNPiqZbgXA',
        startDate='2017-05-01',
        endDate='2023-06-30',
        metrics='audienceWatchRatio',
        dimensions='elapsedVideoTimeRatio',
        filters='video==9EIUpe0qy_g',
       
    )
    array=np.array(result['rows'])
    print(array)
    x = array[:, 0]  # 取出第一列當作 x 軸
    y = array[:, 1]  # 取出第二列存儲在 y 中

    # 把结果保存到CSV文件裡面
    df = pd.DataFrame({'x': x, 'y': y})
    df.to_csv('ch10p2.csv', index=False)
    plt.plot(x, y)
    # 設置 x 軸和 y 軸的標籤
    plt.xlabel('time')
    plt.ylabel('retention')
    plt.show()
