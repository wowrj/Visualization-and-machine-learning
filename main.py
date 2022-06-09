
if __name__ == '__main__':
    import dwsxfx
    import qgfxmodel
    import pyedraw
    import matdraw
    import screen_touzi
    #matplotlib 绘制大宗商品

    matdraw.matdraw_dazong()

    #matplotlib 绘制主要货币

    matdraw.matdraw_huobi()

    #matplotlib 绘制国内股指

    matdraw.matdraw_gp()

    #matplotlib 绘制聚类指导行业投资

    matdraw.matdraw_hychoose()

    #pyecharts 绘制乌克兰危机下投资大屏

    pyedraw.pyedraw_sjdp()

    #pyecharts 绘制聚类指导行业投资

    pyedraw.pyedraw_hychoose()

    #LSTM 训练情感分析模型

    qgfxmodel.model_train('data\\qgfx\\train_Data.csv',100,25,25,'data\\qgfx\\qgfx.h5',5,32)

    #LSTM 预测情感(时间很长)

    qgfxmodel.predict_qg('中远海控','data\\qgfx\\qgfx.h5','data\\qgfx\\train_Data.csv','data\\qgfx\\中远海控股吧.csv',25)

    #LSTM 多维度时序预测

    dwsxfx.process_data('中远海控','data\\qgfx\\qg_predicted.csv','data\\sxfx\\time_train_Data.csv')
    pred,zs = dwsxfx.train_model('data\\sxfx\\time_train_Data.csv',[5],[5],1)

    #pyecharts 绘制单只股票投资透支图

    screen_touzi.touzi_toushi('中远海控',pred,zs,'data\\qgfx\\中远海控股吧.csv')

    #pyecharts 布局函数

    pyedraw.buju('out\\危机相关经济数据1.0.html','out\\j1.json','out\\危机相关经济数据.html')
    screen_touzi.buju('out\\投资透视图待调整.html','out\\j2.json','out\\中远海控投资透视.html')

