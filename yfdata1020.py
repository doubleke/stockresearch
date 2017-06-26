# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 23:29:19 2016

@author: doubleke
"""

#math 590 2nd data analysis
from matplotlib.finance import quotes_historical_yahoo_ochl
from datetime import date
import pandas as pd
import numpy as np
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.stats import norm
    
def myindex():
    "Basic data analysis of one stock or index."
    myquote=input('Enter your interested symbol (example:GE ^NY):')
    # Yahoo Finance 数据接口
    
    today=date.today()
    start=(today.year-5, today.month, today.day)
    aapl=quotes_historical_yahoo_ochl(myquote,start,today)
    aapldf=pd.DataFrame(aapl)
    #print(df)
    
    # 一、 数据清洗
    # 加columns & Index属性
    fields=['Date','Open','Close','High','Low','Volume']
    aapldf=pd.DataFrame(aapl,index=range(1,len(aapl)+1),columns=fields)
    #quotesdf.head()
    
    #日期格式处理
    #firstday=date.fromordinal(735883)
    
    #加columns & Index属性 + 改变yahoo财经数据的日期格式
    list1=[]
    for i in range(0,len(aapl)):
        x1=date.fromordinal(int(aapl[i][0])) #转化成常规时间
        x2=date.strftime(x1,'%Y-%m-%d') #转化成固定格式
        list1.append(x2)
    aapldf=pd.DataFrame(aapl,index=list1,columns=fields)
    aapldf.drop(['Date'],axis=1)
    
    aapldret=aapldf['Close']/aapldf['Open']-1
    
    aapldf['DRet']=pd.Series(aapldret,index=aapldf.index)

    # 二、 plotting画直方图以及概率分布
    bins = ([-0.06,-0.05,-0.04,-0.03,-0.02,-0.01, 0, 0.01,0.02,0.03, 0.04,0.05, 0.06])
    #plt.hist(aapldf['DRet'],bins,normed=1, histtype='bar', facecolor='green', rwidth=1)
    #plt.show()
    
    # Fit a normal distribution to the data:
    mu,sigma = norm.fit(aapldf.DRet)
    
    # Plot the histogram and fitted line.
    plt.hist(aapldf.DRet, bins, normed=True, alpha=0.6, color='green', rwidth=1)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, sigma)
    plt.plot(x, p, 'k', linewidth=1)
    title = "Fit results: $\mu = %.4f$,  $\sigma = %.4f$" % (mu, sigma)
    plt.title(title)
    plt.show()
    
    # 三、 数据分析
    print('1) Statistics', '\n')  
    
    print(aapldf.describe().T, '\n')
    
    print('The autocorrelation of daily return is %.4f \n' %pd.Series.autocorr(aapldf.DRet,lag=1))
    
    #统计股票涨价的每个月天数据
    list1 = []
    tmpdf = aapldf[:]
    for i in range(0, len(tmpdf)):
        list1.append(tmpdf.index[i][:7])
    
    #    list1.append(int(tmpdf.index[i][:4])*100+int(tmpdf.index[i][5:7]))
    tmpdf['YearMon'] = list1

    print('2) Stock increase summary', '\n')
    
    print('The days when the stock increase in a month:\n')     
    print(tmpdf[ tmpdf.Close > tmpdf.Open]['YearMon'].value_counts().head(3))

    #统计股票每个月的volatility。
    print('\n')
    print('3) Volatility by month', '\n')
    print('The monthly volatility of the stock returns:\n')      
    
    # 加columns & Index属性
    #voldf=pd.DataFrame(tmpdf.groupby('YearMon')['DRet'].std(),index=range(1,tmpdf['YearMon'].value_counts()+1), fields=['YM','Vol'])
    voldf=tmpdf.groupby('YearMon')['DRet'].std()
    print(voldf.head(3))
    
    plt.figure()
    voldf.plot(figsize = (6,3), title = 'Monthly Volatility', grid = True, legend =True)                          
    plt.show()


    
def stockmarket():
    "Calculate the correlation between stock and market of your choice."
    
    astock=input('Enter your interested symbol (example:GE):')
    amarket=input('Enter the relative market index (example:^NY):')
    # Yahoo Finance 数据接口
    
    today=date.today()
    start=(today.year-2, today.month, today.day)
    astock=quotes_historical_yahoo_ochl(astock,start,today)
    astockdf=pd.DataFrame(astock)
    amarket=quotes_historical_yahoo_ochl(amarket,start,today)
    amarketdf=pd.DataFrame(amarket)
    #print(df)
    
    # 一、 数据清洗
    # 加columns & Index属性
    fields=['Date','Open','Close','High','Low','Volume']
    #加columns & Index属性 + 改变yahoo财经数据的日期格式
    list1=[]
    for i in range(0,len(astock)):
        x1=date.fromordinal(int(astock[i][0])) #转化成常规时间
        x2=date.strftime(x1,'%Y-%m-%d') #转化成固定格式
        list1.append(x2)
    astockdf=pd.DataFrame(astock,index=list1,columns=fields)
    astockdf.drop(['Date'],axis=1)
    amarketdf=pd.DataFrame(amarket,index=list1,columns=fields)
    amarketdf.drop(['Date'],axis=1)
    
    astockret=astockdf['Close']/astockdf['Open']-1
    amarketret=amarketdf['Close']/amarketdf['Open']-1
    
    astockdf['DRet']=pd.Series(astockret,index=astockdf.index)
    amarketdf['DRet']=pd.Series(amarketret,index=amarketdf.index)
    
    s=astockdf['DRet']
    m=amarketdf['DRet']
    print('\n','The correlation between Stock and Market is: %.4f.' %np.corrcoef(s,m)[0][1])

    # 二、 plotting画直方图以及概率分布
    bins = ([-0.06,-0.05,-0.04,-0.03,-0.02,-0.01, 0, 0.01,0.02,0.03, 0.04,0.05, 0.06])
    #plt.hist(aapldf['DRet'],bins,normed=1, histtype='bar', facecolor='green', rwidth=1)
    #plt.show()
    
    # Fit a normal distribution to the data:
    astockmu,astocksigma = norm.fit(astockdf.DRet)
    amarketmu,amarketsigma = norm.fit(amarketdf.DRet)
    
    #Stock    
    # Plot the histogram and fitted line.
    plt.hist(astockdf.DRet, bins, normed=True, alpha=0.6, color='green', rwidth=1)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    sx = np.linspace(xmin, xmax, 100)
    sp = norm.pdf(sx, astockmu, astocksigma)
    plt.plot(sx, sp, 'k', linewidth=1)
    titles = "Stock fit results: $\mu = %.4f$,  $\sigma = %.4f$" % (astockmu, astocksigma)
    plt.title(titles)
    plt.show()
    
    #Market    
    # Fit a normal distribution to the data:
    # Plot the histogram and fitted line.
    plt.hist(amarketdf.DRet, bins, normed=True, alpha=0.6, color='blue', rwidth=1)
    
    # Plot the PDF.
    xmin, xmax = plt.xlim()
    mx = np.linspace(xmin, xmax, 100)
    mp = norm.pdf(mx, amarketmu, amarketsigma)
    plt.plot(mx, mp, 'k', linewidth=1)
    titlem = "Market fit results: $\mu = %.4f$,  $\sigma = %.4f$" % (amarketmu, amarketsigma)
    plt.title(titlem)
    plt.show()
    
    # 三、 数据分析
    
    print('============For Stock============','\n')
    print('1) Statistics', '\n')  
    
    print(astockdf.describe().T, '\n')
    
    print('The autocorrelation of daily return is %.4f \n' %pd.Series.autocorr(astockdf.DRet,lag=1))
   
    #统计股票涨价的每个月天数据
    list1 = []
    tmpdf = astockdf[:]
    for i in range(0, len(tmpdf)):
        list1.append(tmpdf.index[i][:7])
    
    #    list1.append(int(tmpdf.index[i][:4])*100+int(tmpdf.index[i][5:7]))
    tmpdf['YearMon'] = list1

    print('2) Stock increase summary', '\n')
    
    print('The days when the stock increase in a month:\n')     
    print(tmpdf[ tmpdf.Close > tmpdf.Open]['YearMon'].value_counts().head(3))

    #统计股票每个月的volatility。
    print('\n')
    print('3) Volatility by month', '\n')
    print('The monthly volatility of the stock returns:\n')      
    
    # 加columns & Index属性
    #voldf=pd.DataFrame(tmpdf.groupby('YearMon')['DRet'].std(),index=range(1,tmpdf['YearMon'].value_counts()+1), fields=['YM','Vol'])
    voldf=tmpdf.groupby('YearMon')['DRet'].std()
    print(voldf.head(3))
    
    plt.figure()
    voldf.plot(figsize = (6,3), title = 'Stock Monthly Volatility',color='green', grid = True, legend =True)                          
    plt.show()
    
    # 三、 数据分析
    
    print('============For Market============','\n')
    print('1) Statistics', '\n')  
    
    print(amarketdf.describe().T, '\n')
    
    print('The autocorrelation of daily return is %.4f \n' %pd.Series.autocorr(amarketdf.DRet,lag=1))
 
    #统计股票涨价的每个月天数据
    list1 = []
    tmpdf = amarketdf[:]
    for i in range(0, len(tmpdf)):
        list1.append(tmpdf.index[i][:7])
    
    #    list1.append(int(tmpdf.index[i][:4])*100+int(tmpdf.index[i][5:7]))
    tmpdf['YearMon'] = list1

    print('2) Stock increase summary', '\n')
    
    print('The days when the stock increase in a month:\n')     
    print(tmpdf[ tmpdf.Close > tmpdf.Open]['YearMon'].value_counts().head(3))

    #统计股票每个月的volatility。
    print('\n')
    print('3) Volatility by month', '\n')
    print('The monthly volatility of the stock returns:\n')      
    
    # 加columns & Index属性
    #voldf=pd.DataFrame(tmpdf.groupby('YearMon')['DRet'].std(),index=range(1,tmpdf['YearMon'].value_counts()+1), fields=['YM','Vol'])
    voldf=tmpdf.groupby('YearMon')['DRet'].std()
    print(voldf.head(3))
    
    plt.figure()
    voldf.plot(figsize = (6,3), title = 'Market Monthly Volatility', color='blue',grid = True, legend =True)                          
    plt.show()
    
    # Final
    