# 乌克兰危机下经济数据可视化以及投资决策 
# 开发应用手册
---
@ 2022/06/09 by Renjie Zhu from ECNU 
@ contact : 1518725978@qq.com

本手册包含本项目各模块的使用说明以及可实现以及待开发的功能

***项目作者英文水平不佳,很多看似不相干的字母可能是拼音缩写***

---

## Part 1 初次使用

---

### 关于main.py文件使用

#### a.依赖模块
- os
- zhon
- numpy
- jieba
- pandas
- sklearn
- datetime
- baostock
- pycharts
- matplotlib
- tensorflow(kears)
  
==**请在使用前安装完各个模块**==

#### b.使用说明

在每一个函数上方均标以注释，注释显示起模块所担任的功能，\
==**请先使用示例程序来确保您的系统支持本程序**==
##### 示例数据集来源及其说明

*数据均保存在main.py的同级目录下的data文件夹中*

data 文件夹中所有历史数据结尾的数据均直接来自英为财经，开发者未做任何修改，具体参加readdata模块中子函数的简介

data/wordcloud 文件夹中包含的是百度的停用词，是程序运行==必需文件==

data/qgfx 在程序运行之前有

- 中远海控股吧.csv 
  - 该文件夹包含2月17日至今中远海控股吧利用八爪鱼爬取的所有帖子的标题，阅读量，评论量和时间
  - 该表格的列名为yll，pll，evaluation，date
  - ==在使用其他数据时，与他相同作用的需要列名及其顺序和该文件完全一致==

- train_Data.csv
  - 该文件是开发者标注的数据集，用来训练LSTM情感分析模型
  - 该表格列名为evaluatio，label
  - ==label中1为积极，2为消极==
  - ==在使用其他数据时，与他相同作用的需要列名及其顺序和该文件完全一致==

data/hysj 文件夹存放来自baostock的行业指数，运行前可以没有文件

data/sxfx 文件夹存放来自dwsxfx产生的训练文件，运行前可以没有文件

data/gssj 文件存放的stock_basic存放的是股票与代码的对照，是运行的==必需文件==

#### c.使用技巧

对函数参数不清楚时，只需鼠标落在函数上，开发者附加了注释(Vscode中)，也可以查询本手册

---

## Part 2 模块简介

---
---

### Module1 readdata

含义：读取和加载(在线/离线)数据模块

调用前提：联网/有numpy,pandas,baostock,datetime,os模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

调用方式：import readdata

---

#### 子模块介绍

---
#### readdata.readdata_dazong() 
-> return list,list,list

含义：大宗商品信息读取

==前提：在data文件夹里包含在以下四个网站下载的数据==
==文件命名必须包含 原油 天然气 小麦 黄金 且为csv格式==
https://cn.investing.com/commodities/gold-historical-data       黄金
https://cn.investing.com/commodities/us-wheat                   小麦
https://cn.investing.com/commodities/natural-gas                天然气
https://cn.investing.com/commodities/crude-oil-historical-data  原油

下载方式：点击网址 -> 选择日期(2022-02-17 至今)-> 下载数据 -> 移动数据至data文件夹下

##### 实现功能
(1) 计算日化夏普率 返回一维list与(3)中一一对应
(2) 处理data文件夹中数据  返回list 其中包含与(3)一一对应的DataFrame
==<列名：日期,收盘,开盘,高,低,交易量,涨跌幅,ljsy>(ljsy 为累计收益)==
(3) 返回类别名字 ['原油','天然气','小麦','黄金']

##### 调用实例
```
rhxpl,datali,name = readdata.readdata_dazong()
    rhxpl 日化夏普率
    datali 数据列表
    name 名称
```
---

#### readdata.readdata_huobi() 
-> return list,list,list

含义：美元兑人民币/卢布/欧元信息读取

==前提：在data文件夹里包含在以下三个网站下载的数据==
==文件命名必须包含 USD_CNY;USD_EUR';USD_RUB 且为csv格式==
https://cn.investing.com/currencies/usd-cny-historical-data  人民币
https://cn.investing.com/currencies/usd-eur-historical-data  卢布
https://cn.investing.com/currencies/usd-rub-historical-data  欧元

下载方式：点击网址 -> 选择日期(2022-02-17 至今)-> 下载数据 -> 移动数据至data文件夹下

##### 实现功能
(1) 计算日化夏普率 返回一维list与(3)中一一对应
(2) 处理data文件夹中数据  返回list 其中包含与(3)一一对应的DataFrame
<列名：日期,收盘,开盘,高,低,涨跌幅,ljsy>(ljsy 为累计收益)
(3) 返回类别名字 ['USD_CNY','USD_EUR','USD_RUB']

##### 调用实例 
```
rhxpl,datali,name = readdata.readdata_huobi()
    rhxpl   日化夏普率
    datali  数据列表
    name    名称
```
---

####  readdata.readdata_zhangdie() 
-> DataFrame

含义：国内股市涨跌情况(涨跌家数)

前提：联网
==包含有2月17开始的涨跌数据的母文件(\\data\\涨跌情况_raw.csv)==

##### 实现功能
(1)读取(https://q.stock.sohu.com/cn/zdt.shtml)网页数据并与母数据合并并保存
(2)计算两市涨跌家数和涨跌比储存在sz(上涨),xd(下跌),p(平),dzb(涨跌比)中
h:沪市(hsz,hxd,hp) s:深市(ssz,sxd,sp)
==<列名：日期	hsz	hp hxd ssz	sp sxd	sz xd pzdb>==

##### 调用实例 
```
readdata.readdata_zhangdie()
```

---

#### readdata.readdata_guzhi()
-> DataFrame

含义：在线利用baostock模块读取上证综指信息

前提：联网

##### 实现功能
(1)读取2月17日至今上证综指数据返回在Dataframe中

##### 调用实例 
```
result = readdata.readdata_guzhi()
    result 上证综指 DataFrame <列名：date close>(日期,收盘价)
```
---

#### readdata.bx_hyzs() 
-> None

含义：读取暴雪模块2月17日至3月31日各一级行业指数
```
来自 http://baostock.com/baostock/index.php/%E5%85%AC%E5%BC%8F%E4%B8%8E%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F%E8%AF%B4%E6%98%8E#.E4.B8.80.E7.BA.A7.E8.A1.8C.E4.B8.9A.E6.8C.87.E6.95.B0
```

前提：联网

##### 实现功能
(1)读取各一级行业指数保存到data\\hysj 文件夹下

##### 调用实例 
```
readdata.bx_hyzs()
```
----
#### readdata.single_change(name) 
-> DataFrame

含义：根据输入的中文名称加载单质股票信息

前提：联网
==在data\\gssj 有 stock_basic.csv文件(股票中文名称与代码对应模块)==

##### 实现功能
(1) 根据输入的中文加载单质股票信息

##### 调用实例 
```
result = readdata.single_change('中远海控')
    result 单只股票信息Dataframe<列名：date amount close pctChg>
    (日期,成交量,收盘价,涨跌幅)
```
---


### Module2 matdraw

含义：利用 matplotlib 绘制可视化图形

调用前提：联网/有numpy,pandas,matplotlib,sklearn,os模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

==以及 自有 readdata 模块==

调用方式：import matdraw

---
#### 子模块介绍
---

#### matdraw.dir_if() 
-> None

含义：判断out文件夹是否在运行文件夹之中

##### 实现功能
(1) 判断运行文件夹是否有out文件夹 若无则创建

##### 调用实例
```
matdraw.dir_if()
```
---

#### matdraw.sjzb(ax1) 
-> None

含义：时间坐标调整

##### 实现功能
(1) 时间坐标的美观调整

##### 调用实例
```
matdraw.sjzb(ax1)
```
---

#### matdraw.zt() 
-> None

含义：一键初始化字体

##### 实现功能
(1)初始化字体 汉字为楷体 数学为 stix 字号为20

##### 调用实例
```
matdraw.zt()
```
---

#### matdraw.Tsnm(ax) 
-> None

含义：Times New Roman(Tsnm)

##### 实现功能
(1)修改坐标轴文字为Times New Roman

##### 调用实例
```
matdraw.Tsnm(ax1)
```
---

#### matdraw.matdraw_dazong() 
-> None

含义：利用 matplotlib 进行大宗商品相关信息可视化

##### 实现功能
(1)绘制自2月17日以来投资大宗商品累计收益----折线图
(2)绘制投资各大宗商品日化夏普率------------------雷达图
(3)绘制各大宗商品涨跌幅变化------------------------折线图
(4)绘制子子图涨跌幅变化------------------------------箱型图
(5)保存在out文件夹

##### 调用实例
```
matdraw.matdraw_dazong()
```
---

#### matdraw.matdraw_huobi() 
-> None

含义：利用 matplotlib 进行货币相关信息可视化

##### 实现功能
(1)绘制乌克兰危机下投资美元的累计收益----------------折线图
(2)绘制子子图绘制投资日化夏普率-------------------------横向柱形图
(3)绘制乌克兰危机以来各货币涨跌幅分布----------------琴型图
(4)绘制危机以来美元兑人民币/欧元/卢布涨跌幅走势---折线图
(5)绘制子子图美元兑卢布走势--------------------------------折线图
(6)保存在out文件夹

##### 调用实例
```
matdraw.matdraw_huobi()
```
---

#### matdraw.matdraw_gp() 
-> None

含义：利用 matplotlib 进行国股票市场相关可视化

调用前提：联网

##### 实现功能
(1)绘制危机以来沪深两市涨跌家数-------堆叠柱状图
(2)绘制危机以来沪市指数走势-------------折线图
(3)绘制沪深两市涨跌比----------------------折线图
(4)绘制子子沪深两市涨跌比占比----------饼状
(5)保存在out文件夹

##### 调用实例
```
matdraw.matdraw_gp()
```
---

#### matdraw.matdraw_hychoose() 
-> None

含义：利用 sklearn kmeans 聚类指导行业选择并可视化

调用前提：联网

##### 实现功能
(1)对利用 readdata.bx_hyzs()采集到的数据进行清洗
(2)利用 sklearn.kmeans 模块在归一化之后对成交量(amount_mean)和累计收益(ljsy)聚类
(3)绘制 散点 呈现聚类结果
(4)利用聚类指导行业投资并输出(不)值得投资行业

##### 调用实例
```
matdraw_hychoose()
```
---

#### matdraw.matdraw_all() 
-> None

含义：绘制所有图像

调用前提：联网

##### 调用实例
```
matdraw.matdraw_all()
```
---
---

### Module3 pyedraw

含义：利用 pyecharts 生成动态网页

调用前提：联网/有numpy,pandas,pyecharts,datetime模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

==以及 自有 readdata 模块==

调用方式：import pyedraw

---

#### 子模块介绍

---

#### pyedraw.pyedraw_sjdp() 
-> None

含义：利用 pyecharts 进行制作数据大屏

调用前提：联网

##### 实现功能
(1)制作数据大屏所需的未排版的初步html文件其中包括：
- (a)大宗商品累计收益----------折线图
- (b)大宗商品日化夏普率-------雷达图
- (c)货币累计收益----------------折线图
- (d)货币日化夏普率-------------横向柱形图
- (e)涨跌家数----------------------堆叠柱状图
- (f)沪市指数走势-----------------折线图

(2)将初步html保存到out文件中

##### 调用实例
```
pyedraw.pydraw_sjdp()
```
---

#### pyedraw.buju(raw_path,jsonfile_path,dest_path) 
-> None

含义：利用 json 文件 对未调整的html进行布局

####### 参数介绍
raw_path 待调整网页位置 jsonfile_path json 配置文件位置
dest_path 数据大屏输出位置

调用前提：在未调整的 html 中进行布局后生成json文件

##### 实现功能
(1)利用 json 对未调整的 html 进行预制的布局
(2)将排版完的 html 保存到 dest_path

##### 调用实例
```
pyedraw.buju(raw_path,jsonfile_path,dest_path)
```

---
#### pyedraw_hychoose() 
-> None

含义：利用 pyecharts 制作交互网页

##### 实现功能
(1)制作包含散点图的动态网页实现数据动态查看
(2)生成动态网页在out文件夹

##### 调用实例
```
pyedraw.pyedraw_hychoose()
```
---

#### pyedraw_all() 
-> None

含义：一键制作数据大屏和散点两个网页

##### 调用实例
```
pyedraw.pyedraw_all()
```
---
---

### Module4 qgfxmodel 

含义：利用 LSTM 训练情感分析(情感分析)模型并进行预测

调用前提 有numpy,pandas,matplotlib,sklearn,keras(tensorflow)模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

调用方式：import qgfxmodel

---
#### 子模块介绍
---

#### qgfxmodel.model_train(filepath,n_units,input_shape,output_dim,model_save_path,epochs=5,batch_size=32)
-> None

##### 参数介绍
filepath 训练集位置 n_units LSTM模型参数 
output_dim LSTM模型参数 model_save_path 模型保存位置
epochs LSTM模型参数 batch_size LSTM模型参数

含义：训练 LSTM 情感分析模型

==调用注意！！！==
==训练集必须包括两列 一列名为'evaluation'一列名为'label'其中积极为1消极为2==
(详细参见示例训练集)

##### 实现功能
(1)利用训练集训练LSTM情感分析模型
(2)保存模型至 model_save_path

##### 调用实例
```
qgfxmodel.model_train('data\\qgfx\\train_Data.csv',
                        100,
                        25,
                        25,
                        'data\\qgfx\\qgfx.h5',
                        5,
                        32)
```
---

####  qgfxmodel.predict_qg(name,model_path,traindata,predictdata,destfilepath,input_shape=25,) 
->None

含义：利用 model_train 生成的模型进行预测标注

##### 参数介绍
name 股票名字 model_path 已训练模型位置 traindata 模型的训练集 
predictdata 待预测数据 destfilepath 输出预测完成数据集位置
input_shape LSTM模型参数(默认 25)

==调用注意！！！==
==待预测集必须只包括四列(八爪鱼爬取结果可以直接用)==
==列名及其顺序分别为 ydl,pll,evaluation,date==
(详细参见示例训练集)

##### 实现功能
(1)利用LSTM情感分析模型预测大规模数据集
(2)预测结果保存至 destfilepath

##### 调用实例
```
qgfxmodel.predict_qg('中远海控',
                        'data\\qgfx\\qgfx.h5',
                        'data\\qgfx\\train_Data.csv',
                        'data\\qgfx\\中远海控股吧.csv',
                        'data\\qgfx\\qg_predicted.csv',
                        25)
```
---
---

### Module5 dwsxfx 

含义：利用 LSTM 模型训练并进行多维度时序预测

调用前提 有numpy,pandas,matplotlib,sklearn,keras(tensorflow)模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

==以及 自有 readdata 模块==

调用方式：import dwsxfx

---
#### 子模块介绍
---

#### dwsxfx.process_data(name,qg_data_path,time_train_datapath='data\\\sxfx\\\time_train_Data.csv') 
-> None

##### 参数介绍
name 股票中文名 qg_data_path qgfxmodel.predict_qg(...) 输出的标记文件位置
time_train_datapath 进行多维时序预测训练文件输出位置

含义：利用qgfxmodel模块生成的情感标注文件进行训练集生成

==调用注意！！！==
==生成的情感标注文件必须只包含五列==
==列名及其顺序分别为 ydl,pll,evaluation,date,label==
==<label中1代表积极2代表消极>==
(详细参见示例训练集)

##### 实现功能
(1)处理数据数据集生成训练集
(2)训练集结果保存至 time_train_datapath 默认路径(data\\\sxfx\\\time_train_Data.csv)

##### 调用实例
```
dwsxfx.process_data('中远海控',
            'data\\qgfx\\qg_predicted.csv',
            'data\\sxfx\\time_train_Data.csv'
            )
```
---

#### dwsxfx.readdata(trainfilepath,daypast=1) 
-> ndarray, ndarray, ndarray, ndarray, MinMaxScaler,ndarray, ndarray, list

含义：读取训练集拆分训练集

##### 参数介绍
trainfilepath 训练集位置
daypast 用过去几天的数据预测未来

==调用注意！！！==
==训练集必须是利用 dwsxfx.process_data()生成的==

##### 实现功能
(1)读取,归一化并拆分训练集
(2)返回训练集,测试集,归一化对象,全训练集和预测集

##### 调用实例
```
trainX,trainY,testX,testY,scaler,dfX,dfY,df_for_pred_scaled = dwsxfx.process_data('data\\sxfx\\time_train_Data.csv',1)
```
---

#### dwsxfx.train_model(trainfilepath,batch_size=[6],epochs=[20],daypast_1=1) 
-> str,str

含义：利用 LSTM 模型训练多维度时序预测模型

##### 参数介绍
trainfilepath 训练集位置
batch_size LSTM模型参数 epochs LSTM模型参数
daypast_1 用过去几天的数据预测未来

==调用注意！！！==
==训练集必须是利用 dwsxfx.process_data()生成的==

##### 实现功能
(1)读取,归一化并拆分训练集
(2)利用 process_data()生成的训练集和测试集进行模型训练
(3)自动选择最优参数并绘制在整个数据集上的情况
(3)返回预测值和当日情绪指数

##### 调用实例
```
pred,zs = dwsxfx.train_model(trainfilepath,
                    [5],
                    [5],
                    1) 
    pred 涨跌预测值
    zs 当日情绪指数
```
---
---

### Module6 screen_touzi

含义：绘制单只股票投资数据透视大屏

调用前提 有jiebaa,pandas,pyecharts,datetime,zhon模块
(清华源安装 pip install xxx -i https://pypi.tuna.tsinghua.edu.cn/simple)

==以及 自有 readdata 模块==

调用方式：import screen_touzi

---

子模块介绍

---

#### screen_touzi.touzi_toushi(name,pred,zs,raw_gb_data='data\\\qgfx\\\中远海控股吧.csv') 
-> None

含义：产生单只股票投资数据透视大屏的待调整html文件

##### 参数介绍
name 股票中文名 pred 预测涨跌幅 zs 当日情绪质素
raw_gb_data 原始股吧数据

##### 实现功能
(1)绘制单只股票投资数据透视大屏
(2)保存在out文件夹

##### 调用实例
```
screen_touzi.touzi_toushi('中远海控',
                        2.5,
                        0.4,
                        raw_gb_data='data\\qgfx\\中远海控股吧.csv'
                        )
```
---

#### screen_touzi.buju(raw_path,jsonfile_path,dest_path) 
-> None

含义：利用 json 文件 对未调整的html进行布局

##### 参数介绍
raw_path 待调整网页位置 jsonfile_path json 配置文件位置
dest_path 数据大屏输出位置

调用前提：在未调整的 html 中进行布局后生成json文件

##### 实现功能
(1)利用 json 对未调整的 html 进行预制的布局
(2)将排版完的 html 保存到 dest_path

##### 调用实例
```
screen_touzi.buju(raw_path,jsonfile_path,dest_path)
```
---

## Part 3 功能简介

### 已实现

- matplotlib 绘图接口
- pyechats 绘图接口
- 股票相关数据(行业指数/单只股票价格)
- LSTM 网络预测情感
- LSTM 进行多维度数据预测涨跌
- 聚类分析行业情况

### 待开发
- 东方财富股吧评论的一系列数据的抓取
- 英为财经货币和大宗商品的抓取
- 打包成exe可执行文件
- GUI图形交互使用界面

