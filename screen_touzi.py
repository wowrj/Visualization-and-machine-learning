import jieba
import datetime
import zhon.hanzi
import pandas as pd 
import readdata as rd
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.globals import SymbolType
from pyecharts.charts import WordCloud,Line,Bar,Liquid,Gauge,Page


def touzi_toushi(name,pred,zs,raw_gb_data='data\\qgfx\\中远海控股吧.csv'):
    '''
    #### screen_touzi.touzi_toushi(name,pred,zs,raw_gb_data='data\\\qgfx\\\中远海控股吧.csv') -> None

    含义:产生单只股票投资数据透视大屏的待调整html文件

    #### 参数介绍
    name 股票中文名 pred 预测涨跌幅 zs 当日情绪质素\
    raw_gb_data 原始股吧数据

    #### 实现功能
    (1)绘制单只股票投资数据透视大屏\
    (2)保存在out文件夹

    #### 调用实例
    ```
    screen_touzi.touzi_toushi('中远海控',
                            2.5,
                            0.4,
                            raw_gb_data='data\\qgfx\\中远海控股吧.csv'
                            )
    ```
    ---
    '''
    #返回下面函数需要的与词云相关的名称
    def match(name):
        data = pd.read_csv('data\\gssj\\stock_basic.csv')
        num = data[data['name']==name]['ts_code'].values[0]
        #baostock 模块需要的输入
        bs_need = num[-2::].lower()+'.'+num[:6]
        #正则化 需要
        zzh_need = '\${}\({}\)\$'.format(name,num[-2::]+num[:6])
        
        return bs_need,zzh_need

    #词云分词词频
    def wordclouddata_raw(name,raw_gb_data='data\\qgfx\\zyhkgb.csv'):
        bs_need,zzh_need = match(name)
        jieba.load_userdict('data\\wordcloud\\baidu_stopwords.txt')
        jieba.add_word(name)
        pl = pd.read_csv(raw_gb_data)
        pl.iloc[:,2].replace(regex=True,inplace=True,to_replace=zzh_need,value='')
        text = ''.join(pl.iloc[:,2].tolist())
        ls = jieba.lcut(text)
        punc = zhon.hanzi.punctuation
        exclude = ['今天','明天','这个','什么','就是','这么','没有','怎么','一个']
        newls = []
        for i in ls:
            if i not in punc and i not in exclude and len(i)>1 and i.isdigit()==False:
                newls.append(i)
        ds = pd.Series(newls).value_counts()
        a = ds.index.to_list()
        b = ds.tolist()
        wordclouddata = list(zip(a,b))
        return wordclouddata

    #绘制投资透视图
    def pyedraw(name,pred,zs,raw_gb_data='data\\qgfx\\zyhkgb.csv'):

        def bg()-> Line:
            now=datetime.datetime.now().strftime('%Y/%m/%d')
            background = (
                Line(init_opts=opts.InitOpts(width='1518px',height='716px',theme=ThemeType.CHALK))
                .add_xaxis([None])
                .add_yaxis("", [None]) 
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name+"投资透视图",
                                            subtitle='更新日期:'+now,
                                            pos_left='center',
                                            title_textstyle_opts=opts.TextStyleOpts(font_size=25),
                                            pos_top='3%'),
                    yaxis_opts=opts.AxisOpts(is_show=False),
                    xaxis_opts=opts.AxisOpts(is_show=False))
            )
            return background

        def wordcloud(name,raw_gb_data='data\\qgfx\\zyhkgb.csv')->WordCloud:
            wordclouddata= wordclouddata_raw(name,raw_gb_data)
            c = (
            WordCloud(init_opts=opts.InitOpts(width="590px", height="375px",theme=ThemeType.CHALK))
            .add(
                "",
                wordclouddata, 
                word_size_range=[20, 100], 
                shape=SymbolType.DIAMOND,
                )
            .set_global_opts(title_opts=opts.TitleOpts(title="股吧词云"))
            )
            return c
        
        def amount_price(name) -> Bar:
            stock = rd.single_change(name)
            stock.amount=stock.amount.astype(float)/100000000
            x_data = stock['date'].astype(str).str[5::].tolist()
            bar = (
                Bar(init_opts=opts.InitOpts(width="1518px", height="330px",theme=ThemeType.CHALK))
                .add_xaxis(x_data)
                .add_yaxis("成交额", stock['amount'].astype(float).round(4).tolist())
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .extend_axis(yaxis=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(formatter="{value}"),name='收盘价'
                    )
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=name+"价量"),
                    yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}"),
                                            name='成交量(亿)',),
                    xaxis_opts=opts.AxisOpts(name='日期'),
                    datazoom_opts=[
                        opts.DataZoomOpts(
                            is_show=False,
                            type_='inside',
                            range_start=0,
                            range_end=100
                        )
                    ]
                )
            )
            line = (
                Line(init_opts=opts.InitOpts(theme=ThemeType.CHALK))
                .add_xaxis(x_data)
                .add_yaxis("收盘价", stock['close'].astype(float).round(4).tolist(),
                            label_opts=opts.LabelOpts(is_show=False),yaxis_index=1)
            )
            bar.overlap(line)
            return bar


        def qxzs(zs) -> Liquid:
            zs = round(float(zs),2)
            c = (
            Liquid(init_opts=opts.InitOpts(width="375px", height="295px",theme=ThemeType.CHALK))
            .add(
                "情绪指数",
                [zs, zs],
                is_outline_show=False,
                shape=SymbolType.ARROW,
                label_opts= opts.LabelOpts(font_size=30, position="outside")
                )
            .set_global_opts(title_opts=opts.TitleOpts(title="股吧情绪指数"))
            )
            return c

        def pred_gauge(pred) -> Gauge:
            c = (
                Gauge(init_opts=opts.InitOpts(width="535px", height="370px",theme=ThemeType.CHALK))
                .add(
                    "预测明日涨跌",
                    [('',round(float(pred),2))],
                    min_ = -10,
                    max_ = 10,
                    split_number=5,
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(
                            color=[(0.5, "#006400"), (1, "#FF0000")], width=30
                        )
                    ),
                    detail_label_opts=opts.LabelOpts(formatter="{value}%"),
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="明日涨跌预测"),
                    legend_opts=opts.LegendOpts(is_show=False),
                )
            )
            return c
        def page_draggable_layout(name,zs,pred,raw_gb_data):
            page = Page(layout=Page.DraggablePageLayout,page_title='投资透视图')
            page.add(
            bg(),
            amount_price(name),
            qxzs(zs),
            pred_gauge(pred),
            wordcloud(name,raw_gb_data)
            )
            page.render("out\\投资透视图待调整.html")
            print('请前往out\\投资透视图待调整.html调整网页布局')
        page_draggable_layout(name,zs,pred,raw_gb_data)
    pyedraw(name,pred,zs,raw_gb_data)

def buju(raw_path,jsonfile_path,dest_path):
    '''
    #### screen_touzi.buju(raw_path,jsonfile_path,dest_path) -> None

    含义：利用 json 文件 对未调整的html进行布局

    #### 参数介绍 
    raw_path 待调整网页位置 jsonfile_path json 配置文件位置

    dest_path 数据大屏输出位置

    调用前提:在未调整的 html 中进行布局后生成json文件

    #### 实现功能
    (1)利用 json 对未调整的 html 进行预制的布局

    (2)将排版完的 html 保存到 dest_path

    #### 调用实例
    ```
    screen_touzi.buju(raw_path,jsonfile_path,dest_path)
    ```
    ---
    '''
    Page.save_resize_html(raw_path,cfg_file=jsonfile_path,dest=dest_path)