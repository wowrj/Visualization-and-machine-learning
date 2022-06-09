import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.utils import np_utils
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.layers import LSTM, Dense, Embedding,Dropout
from sklearn.model_selection import train_test_split

# 模型训练
##训练数据集 必须含有两列名称为 evaluation 和 label 分别包含待训练数据和数据标签
def model_train(filepath,n_units,input_shape,output_dim,model_save_path='data\\qgfx\\qgfx.h5',epochs=5,batch_size=32):
    '''
    #### qgfxmodel.model_train(filepath,n_units,input_shape,output_dim,model_save_path,epochs=5,batch_size=32) -> None

    含义：训练 LSTM 情感分析模型

    #### 参数介绍 
    filepath 训练集位置 n_units LSTM模型参数 \\
    output_dim LSTM模型参数 model_save_path 模型保存位置\\
    epochs LSTM模型参数 batch_size LSTM模型参数

    ==调用注意！！！==\\
    ==训练集必须包括两列 一列名为'evaluation'一列名为'label'其中积极为1消极为2==\\
    (详细参见示例训练集)

    #### 实现功能
    (1)利用训练集训练LSTM情感分析模型
    (2)保存模型至 model_save_path

    #### 调用实例
    ```
    qgfxmodel.model_train('data\\qgfx\\train_Data.csv',
                            100,
                            25,
                            25,
                            'data\\qgfx\\qgfx.h5',
                            5,
                            32)
    ```
    '''
    def load_data(filepath,input_shape=25):
        df=pd.read_csv(filepath)

        # 标签及词汇表
        labels,vocabulary=list(df['label'].unique()),list(df['evaluation'].unique())

        # 构造字符级别的特征
        string=''
        for word in vocabulary:
            string+=str(word)

        vocabulary=set(string)

        # 字典列表
        word_dictionary={word:i+1 for i,word in enumerate(vocabulary)}

        inverse_word_dictionary={i+1:word for i,word in enumerate(vocabulary)}
        label_dictionary={label:i for i,label in enumerate(labels)}

        output_dictionary={i:labels for i,labels in enumerate(labels)}

        # 词汇表大小
        vocab_size=len(word_dictionary.keys())
        # 标签类别数量
        label_size=len(label_dictionary.keys())

        # 序列填充,\按input_shape填充,\长度不足的按0补充
        x=[[word_dictionary[word] for word in str(sent)] for sent in df['evaluation']]
        x=pad_sequences(maxlen=input_shape,sequences=x,padding='post',value=0)
        y=[[label_dictionary[sent]] for sent in df['label']]
        y=[np_utils.to_categorical(label,num_classes=label_size) for label in y]
        y=np.array([list(_[0]) for _ in y])

        return x,y,output_dictionary,vocab_size,label_size,inverse_word_dictionary
    def create_LSTM(n_units,input_shape,output_dim,filepath):
        x,y,output_dictionary,vocab_size,label_size,inverse_word_dictionary=load_data(filepath)
        model=Sequential()
        model.add(Embedding(input_dim=vocab_size+1,output_dim=output_dim,
                            input_length=input_shape,mask_zero=True))
        model.add(LSTM(n_units,input_shape=(x.shape[0],x.shape[1])))
        model.add(Dropout(0.2))
        model.add(Dense(label_size,activation='softmax'))
        model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

        # 输出模型信息
        model.summary()

        return model
    # 将数据集分为训练集和测试集,\占比为9：1
    x,y,output_dictionary,vocab_size,label_size,inverse_word_dictionary=load_data(filepath,input_shape)
    train_x,test_x,train_y,test_y=train_test_split(x,y,test_size=0.1,random_state=42)

    # 模型训练
    lstm_model=create_LSTM(n_units,input_shape,output_dim,filepath)
    history = lstm_model.fit(train_x,train_y,epochs=epochs,batch_size=batch_size,verbose=1,validation_data=(test_x,test_y))
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.legend(['accuracy','val_accuracy'])
    plt.show()

    # 模型保存
    lstm_model.save(model_save_path)

    # 测试条数
    N= test_x.shape[0]
    predict=[]
    label=[]
    for start,end in zip(range(0,N,1),range(1,N+1,1)):
        print(f'start:{start}, end:{end}')
        sentence=[inverse_word_dictionary[i] for i in test_x[start] if i!=0]
        y_predict=lstm_model.predict(test_x[start:end])
        print('y_predict:',y_predict)
        label_predict=output_dictionary[np.argmax(y_predict[0])]
        label_true=output_dictionary[np.argmax(test_y[start:end])]
        print(f'label_predict:{label_predict}, label_true:{label_true}')
        # 输出预测结果
        print(''.join(sentence),label_true,label_predict)
        predict.append(label_predict)
        label.append(label_true)
    
    print('\n finsh training model: ',model_save_path)



#训练集的格式：第一列evaluation 第二列 label
def predict_qg(name,model_path,traindata,predictdata,destfilepath,input_shape=25):
    '''
    ####  qgfxmodel.predict_qg(name,model_path,traindata,predictdata,destfilepath,input_shape=25,) ->None

    含义：利用 model_train 生成的模型进行预测标注

    #### 参数介绍 
    name 股票名字 model_path 已训练模型位置 traindata 模型的训练集 \\
    predictdata 待预测数据 destfilepath 输出预测完成数据集位置\\
    input_shape LSTM模型参数(默认 25)

    ==调用注意！！！==\\
    ==待预测集必须只包括四列(八爪鱼爬取结果可以直接用)==\\
    ==列名及其顺序分别为 ydl,pll,evaluation,date==\\
    (详细参见示例训练集)

    #### 实现功能
    (1)利用LSTM情感分析模型预测大规模数据集\\
    (2)预测结果保存至 destfilepath

    #### 调用实例
    ```
    qgfxmodel.predict_qg('中远海控',
                            'data\\qgfx\\qgfx.h5',
                            'data\\qgfx\\train_Data.csv',
                            'data\\qgfx\\中远海控股吧.csv',
                            'data\\qgfx\\qg_predicted.csv',
                            25)
    ```
    '''

    def load_data_1(name,traindata,predictdata,input_shape=25):
        def match(name):
            data = pd.read_csv('data\\gssj\\stock_basic.csv')
            num = data[data['name']==name]['ts_code'].values[0]
            #baostock 模块需要的输入
            bs_need = num[-2::].lower()+'.'+num[:6]
            #正则化 需要
            zzh_need = '\${}\({}\)\$'.format(name,num[-2::]+num[:6])
            
            return bs_need,zzh_need
        bs_need,zzh_need = match(name)
        df=pd.read_csv(traindata)

        # 标签及词汇表
        vocabulary=list(df['evaluation'].unique())

        # 构造字符级别的特征
        string=''
        for word in vocabulary:
            string+=str(word)

        vocabulary=set(string)

        # 字典列表
        word_dictionary={word:i+1 for i,word in enumerate(vocabulary)}
        df1=pd.read_csv(predictdata)
        df1['evaluation'].replace(regex=True,inplace=True,to_replace=zzh_need,value='')
        # 序列填充,\按input_shape填充,\长度不足的按0补充
        x=[[word_dictionary[word] for word in str(sent) if word in word_dictionary.keys()] for sent in df1['evaluation']]
        x=pad_sequences(maxlen=input_shape,sequences=x,padding='post',value=0)

        return x

    import sys
    def progress_bar(i,l):
        print("\r", end="")
        print("predict progress : {}/{} ".format(i+1,l),end="")
        sys.stdout.flush()
    
    def predict_last(name,model_path,traindata,predictdata,destfilepath='data\\qgfx\\qg_predicted.csv',input_shape=25):
        model = load_model(model_path)
        a = load_data_1(name,traindata,predictdata,input_shape)
        df = pd.read_csv(predictdata)
        df['label']=0
        N = len(df)
        out=[1,2]
        for start,end in zip(range(0,N,1),range(1,N+1,1)):
            y_predict=model.predict(a[start:end])
            df.iloc[start,-1] = out[np.argmax(y_predict[0])]
            progress_bar(start,N)
        df.to_csv(destfilepath,index=False)
        print('finsh predicting data:',destfilepath)
    predict_last(name,model_path,traindata,predictdata,destfilepath,input_shape)