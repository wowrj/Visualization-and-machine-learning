#情感标记数据一般来自东方财富的股吧数据，低1到5列分别问阅读量、评论量、evaluation、日期、情感标签（1:积极，2:消极）
import numpy as np
import pandas as pd
import readdata as rd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import GridSearchCV
def process_data(name,qg_data_path,time_train_datapath='data\\sxfx\\time_train_Data.csv'):
    '''
    #### process_data(name,qg_data_path,time_train_datapath='data\\\sxfx\\\time_train_Data.csv') -> None

    含义:利用qgfxmodel模块生成的情感标注文件进行训练集生成

    #### 参数介绍 
    name 股票中文名 qg_data_path qgfxmodel.predict_qg(...) 输出的标记文件位置\\
    time_train_datapath 进行多维时序预测训练文件输出位置

    ==调用注意！！！== 

    ==生成的情感标注文件必须只包含五列==

    ==列名及其顺序分别为 ydl,pll,evaluation,date,label==

    ==<label中1代表积极2代表消极>==

    (详细参见示例训练集)

    #### 实现功能
    (1)处理数据数据集生成训练集
    
    (2)训练集结果保存至 time_train_datapath 默认路径(data\\\sxfx\\\time_train_Data.csv)

    #### 调用实例
    ```
    process_data('中远海控',
                'data\\qgfx\\qg_predicted.csv',
                'data\\sxfx\\time_train_Data.csv'
                )
    ```
    ---
    '''
    single_data = rd.single_change(name)
    qg_data = pd.read_csv(qg_data_path)
    qg_data.columns=['ydl','pll','evaluation','date','label']
    qg_data['date'] = pd.to_datetime(qg_data['date'].str[0:5]+'-2022',format='%m-%d-%Y').apply(lambda x : x.strftime('%Y/%m/%d'))
    f= qg_data.groupby('date').count()[['label']]
    e = qg_data.groupby(['date','label']).count().reset_index('label')
    f['1']= e[e['label']==1]['evaluation']
    f['2']= e[e['label']==2]['evaluation']
    f['qxzs']=f['1']/f['2']
    qxzs = pd.merge(f.reset_index(),qg_data.groupby('date').sum()[['ydl','pll']].reset_index())
    single_data.date=pd.to_datetime(single_data.date)
    qxzs.date=pd.to_datetime(qxzs.date,)
    last = pd.merge(qxzs,single_data,on='date').sort_values('date').dropna()
    last[['date','amount','pctChg','ydl','pll','qxzs']].to_csv(time_train_datapath,index=False)


def readdata(trainfilepath,daypast=1):
    '''
    #### readdata(trainfilepath,daypast=1) -> ndarray, ndarray, ndarray, ndarray, MinMaxScaler,ndarray, ndarray, list

    含义：读取训练集拆分训练集

    #### 参数介绍 
    trainfilepath 训练集位置
    daypast 用过去几天的数据预测未来

    ==调用注意！！！== \\
    ==训练集必须是利用 dwsxfx.process_data()生成的==

    #### 实现功能
    (1)读取,归一化并拆分训练集 \\
    (2)返回训练集,测试集,归一化对象,全训练集和预测集

    #### 调用实例
    ```
    trainX,trainY,testX,testY,scaler,dfX,dfY,df_for_pred_scaled = process_data('data\\sxfx\\time_train_Data.csv',1)
    ```
    '''
    df=pd.read_csv(trainfilepath,parse_dates=["date"],index_col=[0])
    df.insert(0,'pctChg',df.pop('pctChg'))
    test_split=(-1)*round(len(df)*0.20)
    df_for_training=df[:test_split]
    df_for_testing=df[test_split:-1]
    df_for_pred = df[len(df)-daypast:len(df)]
    scaler = MinMaxScaler(feature_range=(0,1))
    df_scaled = scaler.fit_transform(df)
    df_for_training_scaled = scaler.transform(df_for_training)
    df_for_testing_scaled=scaler.transform(df_for_testing)
    df_for_pred_scaled = scaler.transform(df_for_pred)
    def createXY(dataset,n_past):
        dataX = []
        dataY = []
        for i in range(n_past, len(dataset)):
                dataX.append(dataset[i - n_past:i, 0:dataset.shape[1]])
                dataY.append(dataset[i,0])
        return np.array(dataX),np.array(dataY)
    trainX,trainY=createXY(df_for_training_scaled,daypast)
    testX,testY=createXY(df_for_testing_scaled,daypast)
    dfX,dfY = createXY(df_scaled,daypast)
    return trainX,trainY,testX,testY,scaler,dfX,dfY,df_for_pred_scaled


def train_model(trainfilepath,batch_size=[6],epochs=[20],daypast_1=1):
    '''
    #### train_model(trainfilepath,batch_size=[6],epochs=[20],daypast_1=1) -> str,str

    含义：利用 LSTM 模型训练多维度时序预测模型

    #### 参数介绍 
    trainfilepath 训练集位置\\
    batch_size LSTM模型参数 epochs LSTM模型参数\\
    daypast_1 用过去几天的数据预测未来

    ==调用注意！！！==\\
    ==训练集必须是利用 dwsxfx.process_data()生成的==

    #### 实现功能
    (1)读取,归一化并拆分训练集\\
    (2)利用 process_data()生成的训练集和测试集进行模型训练\\
    (3)自动选择最优参数并绘制在整个数据集上的情况\\
    (3)返回预测值和当日情绪指数

    #### 调用实例
    ```
    pred,zs = train_model(trainfilepath,
                        [6],
                        [20],
                        1) 
    ```
    '''
    trainX,trainY,testX,testY,scaler,dfX,dfY,df_for_pred_scaled= readdata(trainfilepath,daypast_1)
    def build_model(optimizer,daypast=daypast_1):
        grid_model = Sequential()
        grid_model.add(LSTM(50,return_sequences=True,input_shape=(daypast,5)))
        grid_model.add(LSTM(50))
        grid_model.add(Dropout(0.2))
        grid_model.add(Dense(1))

        grid_model.compile(loss = 'mse',optimizer = optimizer)
        return grid_model

    grid_model = KerasRegressor(build_fn=build_model,verbose=1,validation_data=(testX,testY))
    parameters = {'batch_size' : batch_size,
                'epochs' : epochs,
                'optimizer' : ['adam','Adadelta'] }

    grid_search  = GridSearchCV(estimator = grid_model,
                                param_grid = parameters,
                                cv = 2)
    grid_search = grid_search.fit(trainX,trainY)
    print(grid_search.best_params_)
    my_model=grid_search.best_estimator_.model
    prediction=my_model.predict(dfX)
    prediction_copies_array = np.repeat(prediction,5, axis=-1)
    pred=scaler.inverse_transform(np.reshape(prediction_copies_array,(len(prediction),5)))[:,0]
    original_copies_array = np.repeat(dfY,5, axis=-1)
    original=scaler.inverse_transform(np.reshape(original_copies_array,(len(dfY),5)))[:,0]
    plt.style.use('seaborn')
    plt.plot(original, color = 'red', label = 'Real Stock Price')
    plt.plot(pred, color = 'blue', label = 'Predicted Stock Price')
    fontdict = {'family':'Times New Roman', 'size':12}
    plt.title('Stock Price Prediction',fontdict={'family':'Times New Roman', 'size':18})
    plt.xlabel('Time',fontdict)
    plt.ylabel('Stock Price',fontdict)
    plt.legend()
    plt.savefig('out\\time_pred.jpg',dpi=500)
    print('保存在 out\\time_pred.jpg')
    plt.show()
    prediction=my_model.predict(np.array([df_for_pred_scaled]))
    prediction_copies_array = np.repeat(prediction,5, axis=-1)
    pred=scaler.inverse_transform(np.reshape(prediction_copies_array,(len(prediction),5)))[:,0][0]
    return pred,df_for_pred_scaled[0][-1]