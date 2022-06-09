import os
import datetime
import numpy as np
import pandas as pd
import baostock as bs
#大宗商品数据读取 返回大宗商品日化夏普率 大宗商品数据储存列表 名称顺序
def readdata_dazong():
    '''
    ---
    #### readdata.readdata_dazong() -> return list,list,list

    含义:大宗商品信息读取

    ==前提:在data文件夹里包含在以下四个网站下载的数据==\\
    ==文件命名必须包含 原油 天然气 小麦 黄金 且为csv格式==\\
    https://cn.investing.com/commodities/gold-historical-data       黄金\\
    https://cn.investing.com/commodities/us-wheat                   小麦\\
    https://cn.investing.com/commodities/natural-gas                天然气\\
    https://cn.investing.com/commodities/crude-oil-historical-data  原油

    下载方式:点击网址 -> 选择日期(2022-02-17 至今)-> 下载数据 -> 移动数据至data文件夹下

    #### 实现功能
    (1) 计算日化夏普率 返回一维list与(3)中一一对应\\
    (2) 处理data文件夹中数据  返回list 其中包含与(3)一一对应的DataFrame\\
    ==<列名:日期,收盘,开盘,高,低,交易量,涨跌幅,ljsy>(ljsy 为累计收益)==\\
    (3) 返回类别名字 ['原油','天然气','小麦','黄金']

    #### 调用实例
    ```
    rhxpl,datali,name = readdata.readdata_dazong()
        rhxpl 日化夏普率
        datali 数据列表
        name 名称
    ```
    ---
    '''
    #利用os批量读取数据
    place = os.listdir('data')
    rawdata = [os.getcwd()+'\\'+'data'+'\\'+i for i in place]

    name=['原油','天然气','小麦','黄金']
    num=[]
    for i in range(len(rawdata)):
        for j in name:
            if j in rawdata[i]:
                num.append(i)
    rhxpl=[]
    datali=[]
    #遍历四种商品 计算日化夏普率
    for i in num:
        x = pd.read_csv(rawdata[i],thousands=',')
        x.涨跌幅 = x.涨跌幅.str[:-1].astype(float)*0.01
        x['日期'] = pd.to_datetime(x['日期'],format='%Y年%m月%d日')
        x.sort_values('日期',inplace=True)
        #计算累计收益
        x['ljsy'] = (1+x['涨跌幅']).cumprod().round(4)
        datali.append(x)
        #日收益率均值
        jz = np.mean(x.涨跌幅)
        #无风险收益率
        wfx = pow(1+0.015,1/365)-1
        #日收益率标准差
        bzc = x.涨跌幅.std()
        #日化夏普率
        xpl=(jz-wfx)/bzc
        rhxpl.append(round(xpl,4))
    return rhxpl,datali,name

#主要货币数据读取 返回主要货币日化夏普率 主要货币数据储存列表 名称顺序
def readdata_huobi():
    '''
    #### readdata.readdata_huobi() -> return list,list,list

    含义:美元兑人民币/卢布/欧元信息读取

    ==前提:在data文件夹里包含在以下三个网站下载的数据==\\
    ==文件命名必须包含 USD_CNY;USD_EUR';USD_RUB 且为csv格式==\\
    https://cn.investing.com/currencies/usd-cny-historical-data  人民币\\
    https://cn.investing.com/currencies/usd-eur-historical-data  卢布\\
    https://cn.investing.com/currencies/usd-rub-historical-data  欧元

    下载方式:点击网址 -> 选择日期(2022-02-17 至今)-> 下载数据 -> 移动数据至data文件夹下

    #### 实现功能
    (1) 计算日化夏普率 返回一维list与(3)中一一对应\\
    (2) 处理data文件夹中数据  返回list 其中包含与(3)一一对应的DataFrame\\
    <列名:日期,收盘,开盘,高,低,涨跌幅,ljsy>(ljsy 为累计收益)\\
    (3) 返回类别名字 ['USD_CNY','USD_EUR','USD_RUB']

    #### 调用实例 
    ```
    rhxpl,datali,name = readdata.readdata_huobi()
        rhxpl   日化夏普率
        datali  数据列表
        name    名称
    ```
    '''
    #利用os批量读取数据
    place = os.listdir('data')
    rawdata = [os.getcwd()+'\\'+'data'+'\\'+i for i in place]
    name=['USD_CNY','USD_EUR','USD_RUB']
    num=[]
    for i in range(len(rawdata)):
        for j in name:
            if j in rawdata[i]:
                num.append(i)
    #计算 日化夏普率
    rhxpl=[]
    datali=[]
    for i in num:
        x = pd.read_csv(rawdata[i],thousands=',')
        x.涨跌幅 = x.涨跌幅.str[:-1].astype(float)*0.01
        x['日期'] = pd.to_datetime(x['日期'],format='%Y年%m月%d日')
        x.sort_values('日期',inplace=True)
        #计算累计收益
        x['ljsy'] = (1+x['涨跌幅']).cumprod()
        datali.append(x)
        #日收益率均值
        jz = np.mean(x.涨跌幅)
        #无风险收益率
        wfx = pow(1+0.015,1/365)-1
        #日收益率标准差
        bzc = x.涨跌幅.std()
        #日化夏普率
        xpl=(jz-wfx)/bzc
        rhxpl.append(round(xpl,4))
    return rhxpl,datali,name

#主要货币数据读取以及更新 返回涨跌情况
def readdata_zhangdie():
    '''
    ####  readdata.readdata_zhangdie() -> DataFrame

    含义:国内股市涨跌情况(涨跌家数)

    前提:联网\\
    ==包含有2月17开始的涨跌数据的母文件(\\data\\涨跌情况_raw.csv)==

    #### 实现功能
    (1)读取(https://q.stock.sohu.com/cn/zdt.shtml)网页数据并与母数据合并并保存\\
    (2)计算两市涨跌家数和涨跌比储存在sz(上涨),xd(下跌),p(平),dzb(涨跌比)中\\
    h:沪市(hsz,hxd,hp) s:深市(ssz,sxd,sp)\\
    ==<列名:日期	hsz	hp hxd ssz	sp sxd	sz xd pzdb>==

    #### 调用实例 
    ```
    readdata.readdata_zhangdie()
    ```
    '''
    #在线读取数据
    dataonline = pd.DataFrame(pd.read_html('https://q.stock.sohu.com/cn/zdt.shtml')[0])
    dataonline.drop([0,1],axis=0,inplace=True)
    dataonline.drop([1,2,3,4],axis=1,inplace=True)
    dataonline.columns=['日期', 'hsz', 'hp', 'hxd', 'ssz', 'sp', 'sxd']
    #读取原有数据并进行合并
    localpalce = os.getcwd()+'\\data\\涨跌情况_raw.csv'
    datalocal = pd.read_csv(localpalce)
    datalocal.columns=['日期', 'hsz', 'hp', 'hxd', 'ssz', 'sp', 'sxd']
    dataall = pd.concat([datalocal,dataonline]).drop_duplicates()
    dataall.to_csv(localpalce,index=False)
    dataall.loc[:,['hsz', 'hp', 'hxd', 'ssz', 'sp', 'sxd']]
    dataall.loc[:,['hsz', 'hp', 'hxd', 'ssz', 'sp', 'sxd']] = dataall.loc[:,['hsz', 'hp', 'hxd', 'ssz', 'sp', 'sxd']].apply(pd.to_numeric)
    #计算两市涨跌家数和涨跌比储存在sz(上涨),xd(下跌),p(平),dzb(涨跌比)中
    dataall['sz']=dataall['hsz']+dataall['ssz']
    dataall['xd']=dataall['hxd']+dataall['sxd']
    dataall['p']=dataall['hp']+dataall['sp']
    dataall['zdb']=dataall['sz']/dataall['xd']
    dataall['日期'] = dataall['日期']+'/2022'
    dataall['日期'] = pd.to_datetime(dataall['日期'],format='%m/%d/%Y')
    dataall.sort_values('日期',inplace=True,ignore_index=True)
    return dataall

#在线加载股指数据
def readdata_guzhi():
    '''
    #### readdata.readdata_guzhi() -> DataFrame

    含义:在线利用baostock模块读取上证综指信息

    前提:联网

    #### 实现功能
    (1)读取2月17日至今上证综指数据返回在Dataframe中

    #### 调用实例 
    ```
    result = readdata.readdata_guzhi()
        result 上证综指 DataFrame <列名:date close>(日期,收盘价)
    ```
    '''
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)
    time_now=datetime.datetime.now().strftime('%Y-%m-%d')
    print('今天是',time_now)
    rs = bs.query_history_k_data_plus("sh.000001",
        "date,close",
        start_date='2022-02-17', end_date=time_now, frequency="d")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录,将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result['date'] = pd.to_datetime(result['date'])
    # 登出系统
    bs.logout()
    return result


#在线读取行业数据
def bx_hyzs():
    '''
    #### readdata.bx_hyzs() -> None

    含义:读取暴雪模块2月17日至3月31日各一级行业指数
    ```
    来自 http://baostock.com/baostock/index.php/%E5%85%AC%E5%BC%8F%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E#.E4.B8.80.E7.BA.A7.E8.A1.8C.E4.B8.9A.E6.8C.87.E6.95.B0
    ```

    前提:联网

    #### 实现功能
    (1)读取各一级行业指数保存到data\\hysj 文件夹下

    #### 调用实例 
    ```
    readdata.bx_hyzs()
    ```
    '''
    if 'hysj' not in os.listdir('data'):
        os.mkdir('data\\hysj')
    onlineli = pd.read_html('http://baostock.com/baostock/index.php/%E5%85%AC%E5%BC%8F%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E#.E4.B8.80.E7.BA.A7.E8.A1.8C.E4.B8.9A.E6.8C.87.E6.95.B0')
    num = onlineli[2].iloc[:,0].tolist()[1::]
    name = onlineli[2].iloc[:,1].tolist()[1::]
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('\rlogin respond error_code:'+lg.error_code,end='')
    print('\rlogin respond  error_msg:'+lg.error_msg,end='')
    for i in range(len(num)):
        rs = bs.query_history_k_data_plus(num[i],
            "date,code,amount,pctChg",
            start_date='2022-02-17', end_date='2022-03-31', frequency="d")
        print('\rquery_history_k_data_plus respond error_code:'+rs.error_code,end='')
        print('\rquery_history_k_data_plus respond  error_msg:'+rs.error_msg,end='')
        # 打印结果集
        data_list = []
        while (rs.error_code == '0') & rs.next():
            # 获取一条记录,将记录合并在一起
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        # 结果集输出到csv文件
        result.to_csv("data\\hysj\\"+name[i]+".csv", index=False)
        print('\rread ok',end='')
    # 登出系统
    bs.logout()


#根据输入的中文名称加载单质股票信息
def single_change(name):
    '''
    #### readdata.single_change(name) -> DataFrame

    含义:根据输入的中文名称加载单质股票信息

    前提:联网\\
    ==在data\\gssj 有 stock_basic.csv文件(股票中文名称与代码对应模块)==

    #### 实现功能
    (1) 根据输入的中文加载单质股票信息

    #### 调用实例 
    ```
    result = readdata.single_change('中远海控')
        result 单只股票信息Dataframe<列名:date amount close pctChg>
        (日期,成交量,收盘价,涨跌幅)
    ```
    '''
    def match(name):
        data = pd.read_csv('data\\gssj\\stock_basic.csv')
        num = data[data['name']==name]['ts_code'].values[0]
        #baostock 模块需要的输入
        bs_need = num[-2::].lower()+'.'+num[:6]
        #正则化 需要
        zzh_need = '\${}\({}\)\$'.format(name,num[-2::]+num[:6])
    
        return bs_need,zzh_need
    bs_need,zzh_need = match(name)
    now_time=datetime.datetime.now().strftime('%Y-%m-%d')
        #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    rs = bs.query_history_k_data_plus(bs_need,
        "date,amount,close,pctChg",
        start_date='2022-02-17', end_date=now_time,
        frequency="d", adjustflag="3")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录,将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 登出系统 ####
    bs.logout()
    return result

def help():
    print('readdata incldude\n readdata_dazong \n readdata_huobi \n readdata_zhangdie \nreaddata_guzhi\n bx_hyzs\n single_change ')