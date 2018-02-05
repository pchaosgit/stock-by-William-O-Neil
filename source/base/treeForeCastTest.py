from time import sleep
import SHSZStockCode
import treeForeCast
import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 获取股票代码
# todo 使用ts.get_stock_basics()获取股票代码
stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
output_file = 'BaiduStockInfo.txt'
slist=[]
SHSZStockCode.getStockList(slist, stock_list_url)

def saveList(filename, thelist):
    thefile = open(filename, 'w')
    for item in thelist:
        thefile.write("%s\n" % item)

uptrend=[] # 上升趋势
downtrend=[] # 下降趋势
kickpoint=[] # 转折点
ri=0
fii=0
kii=0
eii=0
for st in slist:
    if st[:3] not in {'sh2', 'sh5', 'sh9',  'sz1', 'sz2'}:
        df = ts.get_k_data(code = st, start = '2016-01-01') # 获取股票数据
        if len(df) > 100: # 剔除新股
            # 股票有数据
            e = pd.DataFrame()
            e['idx'] = df.index # 用索引号保证顺序X轴
            e['close'] = df['close'] # 用收盘价作为分类标准Y轴, 以Y轴高低划分X成段，并分段拟合
            arr = np.array(e)
            try:
                tree = treeForeCast.createTree(np.mat(arr), 100, 10)
                yHat = treeForeCast.createForeCast(tree, arr[:,0])
                d=yHat[-5:]
                if d[3]<= d[4]:
                    uptrend.append(st)
                    ri+=1
                    md=np.min(d)
                    if (md < d[0]) and (md < d[4]):
                        # 转折点
                        kickpoint.append(st)
                        kii+=1
                else:
                    downtrend.append(st)
                    fii+=1
            except Exception as ex:
                eii+=1
                print( ex)
            print(ri, fii, kii, eii, st)
            #sleep(0.5)

saveList("uptrend.txt",uptrend)
saveList("downtrend.txt",downtrend)
saveList("kickpoint.txt",kickpoint)
