##matplotlib 绘图
import os
import numpy as np
import pandas as pd
import readdata as rd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


#mkdir
def dir_if():

    '''
    #### matdraw.dir_if() -> None

    含义：判断out文件夹是否在运行文件夹之中

    #### 实现功能
    (1) 判断运行文件夹是否有out文件夹 若无则创建

    #### 调用实例
    ```
    matdraw.dir_if()
    ```
    '''
    if 'out' not in os.listdir():
        os.mkdir('out')

#调整时间坐标
def sjzb(ax):

    '''
    #### matdraw.sjzb(ax1) -> None

    含义：时间坐标调整

    #### 实现功能
    (1) 时间坐标的美观调整

    #### 调用实例
    ```
    matdraw.sjzb(ax1)
    ```
    '''

    locator = mdates.AutoDateLocator(minticks=6, maxticks=12)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

#设置字体
def zt():

    '''
    #### matdraw.zt() -> None

    含义：一键初始化字体

    #### 实现功能
    (1)初始化字体 汉字为楷体 数学为 stix 字号为20

    #### 调用实例
    ```
    matdraw.zt()
    ```
    '''

    config = {
    "font.family": "serif",  
    "font.serif": ["KaiTi"], 
    "font.size": 20,  
    "axes.unicode_minus": False,
    "mathtext.fontset": "stix",  
    }
    plt.rcParams.update(config)

#修改坐标文字为Times New Roman
def Tsnm(ax):

    '''
    #### matdraw.Tsnm(ax) -> None

    含义：Times New Roman(Tsnm)

    #### 实现功能
    (1)修改坐标轴文字为Times New Roman

    #### 调用实例
    ```
    matdraw.Tsnm(ax1)
    ```
    '''

    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

#大宗商品相关数据可视化
def matdraw_dazong():

    '''
    #### matdraw.matdraw_dazong() -> None

    含义：利用 matplotlib 进行大宗商品相关信息可视化

    #### 实现功能
    (1)绘制自2月17日以来投资大宗商品累计收益----折线图\\
    (2)绘制投资各大宗商品日化夏普率------------------雷达图\\
    (3)绘制各大宗商品涨跌幅变化------------------------折线图\\
    (4)绘制子子图涨跌幅变化------------------------------箱型图\\
    (5)保存在out文件夹

    #### 调用实例
    ```
    matdraw.matdraw_dazong()
    ```
    '''

    #读取数据
    rhxpl,datali,name=rd.readdata_dazong()
    #选择颜色主题
    plt.style.use('seaborn')
    zt()
    #创建画布
    fig = plt.figure(figsize=(14,9))

    #自2月17日以来投资大宗商品累计收益
    ax1 = plt.subplot2grid((2,2),(0,0))
    ax1.set_title('自2月17日以来投资大宗商品累计收益',fontsize=16)
    for x in datali:
        ax1.plot(x['日期'],x['ljsy'])
    ax1.legend(name,fontsize=10)
    ax1.set_yticks([1.0,1.2,1.4,1.6,1.8])
    Tsnm(ax1)
    sjzb(ax1)
    ax1.grid(True)

    #投资各大宗商品日化夏普率
    #绘制极坐标
    ax2 = plt.subplot2grid((2,2),(0,1),polar=True)
    angles=np.linspace(0, 2*np.pi,len(rhxpl), endpoint=False)+np.pi/6
    rhxpl1=np.concatenate((rhxpl,[rhxpl[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    name1=np.concatenate((name,[name[0]]))
    #注意首位封闭
    ax2.plot(angles, rhxpl1, 'o-', linewidth=2)
    ax2.fill(angles, rhxpl1, alpha=0.25)
    ax2.set_thetagrids(angles * 180/np.pi, name1,fontsize=15)
    ax2.set_ylim(-0.1,0.25)
    ax2.grid(True)
    ax2.set_title('各大宗商品日化夏普率',loc='right',fontsize=16)

    #各大宗商品涨跌幅变化
    ax3 = plt.subplot2grid((2,2),(1,0),colspan=2)
    for x in datali:
        plt.plot(x['日期'],x['涨跌幅'])
    ax3.legend(name,fontsize=10)
    tick = [-0.1,-0.05,0,0.05,0.10,0.15,0.20,0.25]
    label=[str(i*100)+'%' for i in tick]
    ax3.set_yticks(tick,label)
    Tsnm(ax3)
    ax3_1 = ax3.inset_axes([0.6,0.6,0.2,0.35])
    ax3_1.grid(True)
    bp=[]
    for x in datali:
        bp.append(x['涨跌幅'])
    color={'color':'skyblue'}
    #子子图 涨跌幅变化箱型
    ax3_1.boxplot(bp,boxprops = color, flierprops={'markeredgecolor':'skyblue'},medianprops=color, meanprops=color, capprops=color, whiskerprops=color,)
    ax3_1.set_xticks([1,2,3,4],name)
    sjzb(ax3)
    ax3.set_title('各大宗商品涨跌幅变化',fontsize=16)
    ax3.grid(True)

    plt.tight_layout()
    dir_if()
    plt.savefig('out\\大宗商品.jpg',dpi=600)
    print('保存在 out\\大宗商品.jpg')
    plt.show()

##危机中主要货币数据可视化
def matdraw_huobi():
    '''
    #### matdraw.matdraw_huobi() -> None

    含义：利用 matplotlib 进行货币相关信息可视化

    #### 实现功能
    (1)绘制乌克兰危机下投资美元的累计收益----------------折线图\\
    (2)绘制子子图绘制投资日化夏普率-------------------------横向柱形图\\
    (3)绘制乌克兰危机以来各货币涨跌幅分布----------------琴型图\\
    (4)绘制危机以来美元兑人民币/欧元/卢布涨跌幅走势---折线图\\
    (5)绘制子子图美元兑卢布走势--------------------------------折线图\\
    (6)保存在out文件夹

    #### 调用实例
    ```
    matdraw.matdraw_huobi()
    ```
    '''
    #读取数据
    rhxpl,datali,name=rd.readdata_huobi()
    #选择颜色主题
    plt.style.use('seaborn')
    zt()
    #创建画布
    fig = plt.figure(figsize=(15,10))

    #乌克兰危机下投资美元的累计收益
    ax1 = plt.subplot2grid((2,2),(0,0))
    ax1.set_title('乌克兰危机下投资美元的累计收益',fontsize=15)
    for x in datali:
        ax1.plot(x['日期'],x['ljsy'])
    fontdict = {'family':'Times New Roman', 'size':12}
    ax1.legend(name,prop=fontdict)
    Tsnm(ax1)
    sjzb(ax1)

    #投资日化夏普率
    ax1_1 = ax1.inset_axes([0.6,0.45,0.35,0.2])
    ax1_1.barh([1,2,3],rhxpl)
    ax1_1.set_yticks([1,2,3],name,)
    Tsnm(ax1_1)
    ax1_1.set_title('投资日化夏普率',fontsize=14)

    #乌克兰危机以来各货币涨跌幅分布
    ax2 = plt.subplot2grid((2,2),(0,1))
    vp=[]
    for x in datali:
        vp.append(x['涨跌幅'])
    ax2.violinplot(vp)
    ax2.set_xticks([1,2,3],name)
    tick = [-0.1,-0.05,0,0.05,0.10,0.15,0.20,0.25]
    label=[str(i*100)+'%' for i in tick]
    ax2.set_yticks(tick,label)
    ax2.set_title('乌克兰危机以来各货币涨跌幅分布',fontsize=16)
    Tsnm(ax2)

    #乌克兰危机以来美元兑人民币、欧元、卢布涨跌幅走势
    ax3 = plt.subplot2grid((2,2),(1,0),colspan=2)
    ax3.set_title('乌克兰危机以来美元兑人民币、欧元、卢布涨跌幅走势',fontsize=16)
    for x in datali:
        plt.plot(x['日期'],x['涨跌幅'])
    ax3.legend(name,prop=fontdict)
    tick = [-0.1,-0.05,0,0.05,0.10,0.15,0.20,0.25]
    label=[str(i*100)+'%' for i in tick]
    ax3.set_yticks(tick,label)
    Tsnm(ax3)
    sjzb(ax3)
    
    #美元兑卢布走势
    ax3_1 = ax3.inset_axes([0.6,0.55,0.2,0.35])
    ax3_1.plot(datali[2]['日期'],datali[2]['收盘'])
    ax3_1.set_title('美元兑卢布走势')
    labels = ax3_1.get_xticklabels() + ax3_1.get_yticklabels()
    Tsnm(ax3_1)
    sjzb(ax3_1)

    plt.tight_layout()
    dir_if()
    plt.savefig('out\\主要货币.jpg',dpi=600)
    print('保存在 out\\主要货币.jpg')
    plt.show()

## 我国沪深股指数据可视化
def matdraw_gp():

    '''
    #### matdraw.matdraw_gp() -> None

    含义：利用 matplotlib 进行国股票市场相关可视化

    调用前提：联网

    #### 实现功能
    (1)绘制危机以来沪深两市涨跌家数-------堆叠柱状图\\
    (2)绘制危机以来沪市指数走势-------------折线\\
    (3)绘制沪深两市涨跌比----------------------折线图\\
    (4)绘制子子沪深两市涨跌比占比----------饼状\\
    (5)保存在out文件夹

    #### 调用实例
    ```
    matdraw.matdraw_gp()
    ```
    '''

    plt.style.use('seaborn')
    zt()
    plt.figure(figsize=(15,10))
    #数据读取及其预处理
    dataall = rd.readdata_zhangdie()
    guzhi = rd.readdata_guzhi()
    guzhi['date'] =pd.to_datetime(guzhi['date'])
    guzhi['close'] = guzhi['close'].astype(float)
    ax1 = plt.subplot2grid((2,2),(1,0))
    data_pie= ax1.hist(dataall['zdb'],bins=[0,0.25,0.5,0.75,1,2,5,18])
    plt.delaxes(ax1)
    #乌克兰危机以来沪深两市涨跌家数
    ax1 = plt.subplot2grid((2,2),(1,0))
    ax1.set_title('乌克兰危机以来沪深两市涨跌家数')
    ax1.bar(dataall['日期'],dataall['sz'],color='r')
    ax1.bar(dataall['日期'],dataall['p'],bottom=dataall['sz'],color='orange')
    ax1.bar(dataall['日期'],dataall['xd'],bottom=dataall['sz']+dataall['p'],color='green')
    Tsnm(ax1)
    sjzb(ax1)

    #乌克兰危机以来沪市指数走势
    ax2=plt.subplot2grid((2,2),(0,0))
    ax2.set_xticks([])
    Tsnm(ax2)
    ax2.plot(guzhi['date'],guzhi['close'])
    ax2.set_title('乌克兰危机以来沪市指数走势')

    #沪深两市涨跌比及其占比
    ax3=plt.subplot2grid((2,2),(0,1),rowspan=2)
    ax3.set_xticks([])
    ax3.set_title('沪深两市涨跌比及其占比')
    ax3.plot(dataall['日期'],dataall['zdb'])
    Tsnm(ax3)

    ax3_1 = ax3.inset_axes([0.45,0.35,0.5,0.5])
    label=['%.1f-%.1f'%(data_pie[1][i],data_pie[1][i+1]) for i in range(len(data_pie[1])-1)]
    d = ax3_1.pie(data_pie[0],explode=(0.08,0.03,0.04,0.05,0.05,0.01,0),shadow=True,labels=label,autopct='%.1f%%')
    fontdict = {'family':'Times New Roman', 'size':6}
    for t in d[1]:
        t.set_fontproperties(fontdict)
    for t in d[2]:
        t.set_fontproperties(fontdict)
    ax3_1.set_axis_off()

    dir_if()
    plt.savefig('out\\国内股指.jpg',dpi=600)
    print('保存在 out\\国内股指.jpg')
    plt.show()

#利用聚类进行行业选择投资
def matdraw_hychoose():

    '''
    #### matdraw.matdraw_hychoose() -> None

    含义：利用 sklearn kmeans 聚类指导行业选择并可视化

    调用前提：联网

    #### 实现功能
    (1)对利用 readdata.bx_hyzs()采集到的数据进行清洗\\
    (2)利用 sklearn.kmeans 模块在归一化之后对成交量(amount_mean)和累计收益(ljsy)聚类\\
    (3)绘制 散点 呈现聚类结果\\
    (4)利用聚类指导行业投资并输出(不)值得投资行业

    #### 调用实例
    ```
    matdraw_hychoose()
    ```
    '''

    rd.bx_hyzs()
    place = os.listdir("data\\hysj")
    cluster_rawdata = []
    hyname = []
    for i in place:
        x = pd.read_csv('data\\hysj'+'\\'+i)
        if len(x) != 0:
            ljsy = (x['pctChg']*0.01+1).cumprod().iloc[-1]
            amount_mean = x['amount'].mean()
            j = [ljsy,amount_mean]
            hyname.append(i[0:-4])
            cluster_rawdata.append(j)
    cluster_data = pd.DataFrame(cluster_rawdata,columns=['ljsy','amount_mean'])
    cluster_data_trans = MinMaxScaler().fit_transform(cluster_data)
    model = KMeans(n_clusters=2)
    p = model.fit_predict(np.array(cluster_data_trans))
    cluster_data['pred'] = p
    cluster_data['name'] = hyname
    drawdata = pd.DataFrame(np.hstack([cluster_data_trans,p.reshape(-1,1)]),
                            columns=['ljsy','amount_mean','pred'])
    drawdata['name']=hyname
    dic = {}
    dic[drawdata.sort_values(['ljsy'])['pred'].iloc[-1]]='值得投资'
    dic[drawdata.sort_values(['ljsy'])['pred'].iloc[0]]='不值得投资'
    plt.style.use('seaborn')
    zt()
    plt.figure()
    ax = plt.subplot()
    ax.scatter(cluster_data[cluster_data['pred'] == 1]['amount_mean'],
                cluster_data[cluster_data['pred'] == 1]['ljsy'],
                s=180*drawdata[drawdata['pred'] == 1]['ljsy'],
                alpha=0.6)
    ax.scatter(cluster_data[cluster_data['pred'] == 0]['amount_mean'],
                cluster_data[cluster_data['pred'] == 0]['ljsy'],
                s=180*drawdata[drawdata['pred'] == 0]['ljsy'],
                alpha=0.6)
    ax.legend([dic[1],dic[0]])
    ax.set_title("聚类指导乌克兰危机以来至3月31日行业投资选择")
    ax.set_xlabel('成交额(元)')
    ax.set_ylabel('累计收益(%)')
    Tsnm(ax)
    print('\r'+dic[0],cluster_data[cluster_data['pred'] == 0]['name'].values)
    print(dic[1],cluster_data[cluster_data['pred'] == 1]['name'].values)
    dir_if()
    plt.savefig('out\\聚类指导行业选择.jpg',dpi=600)
    print('保存在 out\\聚类指导行业选择.jpg')
    plt.show()


def matdraw_all():
    '''
    #### matdraw.matdraw_all() -> None

    含义：绘制所有图像

    调用前提：联网

    #### 调用实例
    ```
    matdraw.matdraw_all()
    ```
    '''
    matdraw_dazong()
    matdraw_huobi()
    matdraw_gp()
    matdraw_hychoose()

def help():
    print('matdraw include\nmatdraw_dazong\nmatdraw_huobi\nmatdraw_gp\nmatdraw_hychoose')