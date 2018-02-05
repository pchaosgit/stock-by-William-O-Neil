# -*- coding: utf-8 -*-
# 参见 http://blog.csdn.net/xieyan0811/article/details/78581974

import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mp
import time

#日期格式YYYYMMDD转为YYYY-MM-DD
def formatDate(Date, formatType='YYYYMMDD'):
    formatType = formatType.replace('YYYY', Date[0:4])
    formatType = formatType.replace('MM', Date[4:6])
    formatType = formatType.replace('DD', Date[-2:])
    return formatType

def get_data(code=None, start='', end='',
                  ktype='D', autype='qfq',
                  index=False,
                  retry_count=3):
        """
        获取k线数据
        ---------
        Parameters:
        code:string
                  股票代码 e.g. 600848
        start:string
                  开始日期 format：YYYY-MM-DD 为空时取上市首日
        end:string
                  结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
        autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
        ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
        retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
        return
        -------
        DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          amount 成交额
          turnoverratio 换手率
          code 股票代码
        """
        dh=ts.get_k_data(code,start=start,end=end) #不复权
        dg=ts.get_k_data(code,start=start,end=end,autype='hfq')     #后复权
        del dg['code']
        del dg['date']
        del dg['volume']
        dg.rename(columns={'open':'fopen', 'close':'fclose', 'high':'fhigh', 'low':'flow'}, inplace = True)
        mergeColumn=pd.concat([dh,dg],axis=1)
        return mergeColumn

# 用feature把dataSet按value分成两个子集
def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[np.nonzero(dataSet[:,feature] > value)[0],:]
    mat1 = dataSet[np.nonzero(dataSet[:,feature] <= value)[0],:]
    return mat0,mat1

# 求给定数据集的线性方程
def linearSolve(dataSet):
    m,n = np.shape(dataSet)
    X = np.mat(np.ones((m,n))); # 第一行补1，线性拟合要求
    Y = np.mat(np.ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1];
    Y = dataSet[:,-1] # 数据最后一列是y
    xTx = X.T*X
    if np.linalg.det(xTx) == 0.0:
        raise NameError('This matrix is singular, cannot do inverse,\n\
        try increasing dur')
    ws = xTx.I * (X.T * Y) # 公式推导较难理解
    return ws,X,Y

# 求线性方程的参数
def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

# 预测值和y的方差
def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(np.power(Y - yHat,2))

def chooseBestSplit(dataSet, rate, dur):
    # 判断所有样本是否为同一分类
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return None, modelLeaf(dataSet)
    m,n = np.shape(dataSet)
    S = modelErr(dataSet) # 整体误差
    bestS = np.inf
    bestIndex = 0
    bestValue = 0
    for featIndex in range(n-1): # 遍历所有特征, 此处只有一个
        # 遍历特征中每种取值
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (np.shape(mat0)[0] < dur) or (np.shape(mat1)[0] < dur):
                continue # 样本数太少, 前剪枝
            newS = modelErr(mat0) + modelErr(mat1) # 计算整体误差
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < rate: # 如差误差下降得太少，则不切分
        return None, modelLeaf(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    return bestIndex,bestValue

def isTree(obj):
    return (type(obj).__name__=='dict')

# 预测函数,数据乘模型,模型是斜率和截距的矩阵
def modelTreeEval(model, inDat):
    n = np.shape(inDat)[1]
    X = np.mat(np.ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

# 预测函数
def treeForeCast(tree, inData):
    if not isTree(tree):
        return modelTreeEval(tree, inData)
    if inData[tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'], inData)
        else:
            return modelTreeEval(tree['left'], inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'], inData)
        else:
            return modelTreeEval(tree['right'], inData)

# 对测试数据集预测一系列结果, 用于做图
def createForeCast(tree, testData):
    m=len(testData)
    yHat = np.mat(np.zeros((m,1)))
    for i in range(m): # m是item个数
        yHat[i,0] = treeForeCast(tree, np.mat(testData[i]))
    return yHat

# 绘图
def draw(dataSet, tree, title, loc='left', color ='red',drawEnd=True):
    #plt.figure(figsize=[20,11]) # 改变画布大小
    plt.ion()
    plt.title(title, loc=loc, color='#123456');
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.xlabel('Time')
    plt.ylabel('收盘价')
    plt.scatter(dataSet[:,0], dataSet[:,1], s=5) # 在图中以点画收盘价
    yHat = createForeCast(tree, dataSet[:,0])
    plt.plot(dataSet[:,0], yHat, linewidth=1.0, color=color)
    plt.draw()
    plt.pause(0.08)
    #if drawEnd:
    #plt.draw()

# 生成回归树, dataSet是数据, rate是误差下降, dur是叶节点的最小样本数
def createTree(dataSet, rate, dur):
    # 寻找最佳划分点, feat为切分点, val为值
    feat, val = chooseBestSplit(dataSet, rate, dur)
    if feat == None:
        return val # 不再可分
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val) # 把数据切给左右两树
    retTree['left'] = createTree(lSet, rate, dur)
    retTree['right'] = createTree(rSet, rate, dur)
    return retTree

if __name__ == '__main__':
    sbdf=ts.get_stock_basics()
    Code=sbdf.index

    stCode='601155'
    idx=0
    stDate=sbdf.loc[stCode]['timeToMarket']                   #上市日期YYYYMMDD
    stDate=formatDate(str(stDate),'YYYY-MM-DD')            #改一下格式
    stDate='2015-01-01'
    step=5
    start = time.time()
#    df = ts.get_k_data(code = '002230', start = '2017-01-01') # 科大讯飞今年的股票数据
    # df = ts.get_k_data(code = '600026', start = '2016-01-01', ktype='30') # 股票数据
    df = get_data(code = stCode, start = stDate, index=(idx!=0))
    cons=None
    #cons=ts.get_apis()
    #df = ts.bar( '603766', conn=cons, freq='60min',adj='qfq', start_date='2016-01-01')
    # df = ts.bar( '603766', conn=cons, adj='qfq', start_date='2016-01-01')
    if cons:
        # 使用ts.bar的数据，需要reverse
        df = df.iloc[::-1]
        df.index = pd.RangeIndex(len(df.index))
    plt.figure(figsize=[20,11]) # 改变画布大小
    plt.xlim([0,len(df)+1])
    plt.ylim([min(df['fclose'])*0.9,max(df['fclose'])*1.05])
    i=0; sl=80
    for c  in mp.colors.cnames:
        start2 = time.time()
        e= pd.DataFrame()
        sl+=step
        if (sl > len(df)):
            break;
        e['idx'] = df.index[:sl]
        e['close'] = df['fclose'][:sl] # 用收盘价作为分类标准Y轴, 以Y轴高低划分X成段，并分段拟合
        arr = np.array(e)
        tree = createTree(np.mat(arr), 100, 10)
        end = time.time()
        draw(arr, tree, stCode + ' start: ' + stDate + " TotalTime:" + str(end-start) + " " + str((end-start)/len(df)) + " " + str(len(e)), color = c)
        # i+=1
        if end-start2 < 5:
            time.sleep(5+end-start2)


    if cons:
        ts.close_apis(cons)

    time.sleep(5)

