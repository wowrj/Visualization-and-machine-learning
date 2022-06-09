#pyecharts 可视化
import os
import datetime
import numpy as np
import pandas as pd
import readdata as rd
import pyecharts.options as opts
from sklearn.cluster import KMeans
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from sklearn.preprocessing import MinMaxScaler
from pyecharts.charts import Line, Page,Bar,Radar,Scatter

def pyedraw_sjdp():
    '''
    #### pyedraw.pyedraw_sjdp() -> None

    含义：利用 pyecharts 进行制作数据大屏

    调用前提：联网

    ###### 实现功能
    (1)制作数据大屏所需的未排版的初步html文件其中包括：
    - (a)大宗商品累计收益----------折线图
    - (b)大宗商品日化夏普率-------雷达图
    - (c)货币累计收益----------------折线图
    - (d)货币日化夏普率-------------横向柱形图
    - (e)涨跌家数----------------------堆叠柱状图
    - (f)沪市指数走势-----------------折线图

    (2)将初步html保存到out文件中

    #### 调用实例
    ```
    pyedraw.pydraw_sjdp()
    ```
    '''
    #background
    time_now=datetime.datetime.now().strftime('%Y-%m-%d')
    def bg()-> Line:
        background = (
            Line(init_opts=opts.InitOpts(
                width='1515px',
                height='710px',
                theme=ThemeType.CHALK,
                page_title='乌克兰危机以来经济数据'
                    )
                )
            .add_xaxis([None])
            .add_yaxis("", [None]) 
            .set_global_opts(
                title_opts=opts.TitleOpts(title="乌克兰危机以来经济数据",
                                        subtitle='更新日期:'+time_now,
                                        pos_left='center',
                                        title_textstyle_opts=opts.TextStyleOpts(font_size=25),
                                        pos_top='3%'),
                yaxis_opts=opts.AxisOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(is_show=False))
        )
        return background
    #大宗商品累计收益
    def dzsp_ljsy() -> Line:
        rhxpl,datali,name=rd.readdata_dazong()
        x_data = datali[0]['日期'].astype(str).tolist()
        c = (
            Line(init_opts=opts.InitOpts(width="500px", height="320px",theme=ThemeType.CHALK))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name=name[0],
                y_axis=datali[0]['ljsy'].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name=name[1],
                y_axis=datali[1]['ljsy'].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name=name[2],
                y_axis=datali[2]['ljsy'].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name=name[3],
                y_axis=datali[3]['ljsy'].tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="大宗商品累计收益变化",title_textstyle_opts=opts.TextStyleOpts(font_size=10)),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="time", boundary_gap=True),
                yaxis_opts=opts.AxisOpts(min_=0.7)
            )
            
        )
        return c

    #大宗商品日化夏普率
    def dzsp_rhxpl() -> Radar:
        rhxpl,datali,name=rd.readdata_dazong()
        c_schema=[]
        for i in range(4):
            d = {}
            d['name']=name[i]
            d['max']=0.25
            d['min']=-0.1
            c_schema.append(d)
        data = [{"value":rhxpl, "name": "日化夏普率"}]
        c = (
            Radar(init_opts=opts.InitOpts(width="500px", height="345px",theme=ThemeType.CHALK,))
    #        .set_colors(["#4587E7"])
            .add_schema(
                schema=c_schema,
                shape="circle",
                center=["50%", "50%"],
                radius="80%",
                angleaxis_opts=opts.AngleAxisOpts(
                    min_=0,
                    max_=360,
                    is_clockwise=False,
                    interval=4,
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                radiusaxis_opts=opts.RadiusAxisOpts(
                    min_=-0.1,
                    max_=0.25,
                    interval=0.05,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=0.1)
                    ),
                ),
                polar_opts=opts.PolarOpts(),
                splitarea_opt=opts.SplitAreaOpts(is_show=False),
                splitline_opt=opts.SplitLineOpts(is_show=False),
            )
            .add(
                series_name="日化夏普率",
                data=data,
                areastyle_opts=opts.AreaStyleOpts(opacity=0.1),
                linestyle_opts=opts.LineStyleOpts(width=1),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                    title_opts= opts.TitleOpts(title='大宗商品日化夏普率',title_textstyle_opts=opts.TextStyleOpts(font_size=15))
            )
        )
        return c

    #货币累计收益
    def hb_ljsy() -> Line:
        rhxpl,datali,name=rd.readdata_huobi()
        x_data = datali[0]['日期'].astype(str).tolist()
        c=(
            Line(init_opts=opts.InitOpts(width="500px", height="320px",theme=ThemeType.CHALK))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name=name[0],
                y_axis=datali[0]['ljsy'].round(4).tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name=name[1],
                y_axis=datali[1]['ljsy'].round(4).tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name=name[2],
                y_axis=datali[2]['ljsy'].round(4).tolist(),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(title="主要货币累计收益变化",title_textstyle_opts=opts.TextStyleOpts(font_size=10)),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="time", boundary_gap=True),
                yaxis_opts=opts.AxisOpts(min_=0.6)
            )
        )
        return c

    #货币日化夏普率
    def hb_rhxpl() ->Bar:
        rhxpl,datali,name=rd.readdata_huobi()
        c = (
            Bar(init_opts=opts.InitOpts(width="500px", height="360px",theme=ThemeType.CHALK,))
            .add_xaxis(name)
            .add_yaxis('',rhxpl)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="货币日化夏普率",title_textstyle_opts=opts.TextStyleOpts(font_size=15)))
        )
        return c
    
    #涨跌家数
    def zdjs() -> Bar:
        zdqk=rd.readdata_zhangdie()
        x_data = zdqk['日期'].astype(str).tolist()
        c = (
            Bar(init_opts=opts.InitOpts(width="500px", height="360px",theme=ThemeType.CHALK,))
            .add_xaxis(x_data)
            .add_yaxis('上涨', zdqk['sz'].tolist(), stack="stack1")
            .add_yaxis("平盘", zdqk['p'].tolist(), stack="stack1")
            .add_yaxis("下跌", zdqk['xd'].tolist(), stack="stack1")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="沪深两市涨跌家数",title_textstyle_opts=opts.TextStyleOpts(font_size=15)))
        )
        return c

    #沪市指数走势
    def zszs() -> Line:
        guzhi = rd.readdata_guzhi()
        x_data = guzhi['date'].astype(str).tolist()
        c = (
            Line(init_opts=opts.InitOpts(width="500px", height="360px",theme=ThemeType.CHALK))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name='沪市',
                y_axis=guzhi['close'],
                label_opts=opts.LabelOpts(is_show=False),
            )

            .set_global_opts(
                title_opts=opts.TitleOpts(title="沪市指数走势",title_textstyle_opts=opts.TextStyleOpts(font_size=15)),
                tooltip_opts=opts.TooltipOpts(trigger="axis"),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                xaxis_opts=opts.AxisOpts(type_="time", boundary_gap=True),
                yaxis_opts=opts.AxisOpts(type_='value',min_=2800)
            )
        )
        return c

    def page_draggable_layout():
        page = Page(page_title='乌克兰危机以来经济数据',layout=Page.DraggablePageLayout)
        page.add(
        bg(),
        dzsp_rhxpl(),
        dzsp_ljsy(),
        hb_ljsy(),
        hb_rhxpl(),
        zdjs(),
        zszs(),
        )
        page.render("out\\危机相关经济数据1.0.html")
        print('保存至 out\\危机相关经济数据1.0.html')
    page_draggable_layout()

def buju(raw_path,jsonfile_path,dest_path):
    '''
    #### pyedraw.buju(raw_path,jsonfile_path,dest_path) -> None

    含义：利用 json 文件 对未调整的html进行布局

    ###### 参数介绍 
    raw_path 待调整网页位置 jsonfile_path json 配置文件位置\\
    dest_path 数据大屏输出位置

    调用前提：在未调整的 html 中进行布局后生成json文件

    #### 实现功能
    (1)利用 json 对未调整的 html 进行预制的布局\\
    (2)将排版完的 html 保存到 dest_path

    #### 调用实例
    ```
    pyedraw.buju(raw_path,jsonfile_path,dest_path)
    ```
    '''
    Page.save_resize_html(raw_path,cfg_file=jsonfile_path,dest=dest_path)
    print('保存至  ',dest_path)

def pyedraw_hychoose():
    '''
    #### pyedraw_hychoose() -> None

    含义：利用 pyecharts 制作交互网页

    #### 实现功能
    (1)制作包含散点图的动态网页实现数据动态查看\\
    (2)生成动态网页在out文件夹

    #### 调用实例
    ```
    pyedraw.pyedraw_hychoose()
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
    c = (
        Scatter(init_opts=opts.InitOpts(page_title='乌克兰危机以来至3月31日行业投资选择'))
        .add_xaxis(((pd.concat([cluster_data[cluster_data['pred'] == 1],cluster_data[cluster_data['pred'] == 0]]
    )['amount_mean'])/10000000).values)
        .add_yaxis(
            dic[1],
            [list(z) for z in zip(cluster_data[cluster_data['pred'] == 1]['ljsy'].round(4).values,
                            cluster_data[cluster_data['pred'] == 1]['name'].values)],
            label_opts=opts.LabelOpts(is_show=False),
            )
        .add_yaxis(
            dic[0],
            [list(z) for z in zip(cluster_data[cluster_data['pred'] == 0]['ljsy'].round(4).values,
                            cluster_data[cluster_data['pred'] == 0]['name'].values)],
            label_opts=opts.LabelOpts(is_show=False),)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="乌克兰危机以来至3月31日行业投资选择"),
            yaxis_opts=opts.AxisOpts(type_='value',name = '累计收益(%)' ,min_=0.82),
            xaxis_opts=opts.AxisOpts(type_='value',name = '平均成交额(亿)'),
            tooltip_opts=opts.TooltipOpts(
                formatter=JsCode(
                    "function (params) {return params.value[2] + ' : ' + params.value[1];}"
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                type_="color", max_=1.18, min_=0.82, dimension=1
            ),
            toolbox_opts=opts.ToolboxOpts(is_show=True)
        )
        .render("out\\聚类指导行业投资.html")
    )
    print('保存至 out\\聚类指导行业投资.html')

def pyedraw_all():
    '''
    #### pyedraw_all() -> None

    含义：一键制作数据大屏和散点两个网页

    #### 调用实例
    ```
    pyedraw.pyedraw_all()
    ```
    '''
    pyedraw_sjdp()
    pyedraw_hychoose()

def help():
    print('pyedraw include \n pyedraw_sjdp\nbuju\npyedraw_hychoose\npyedraw_all')