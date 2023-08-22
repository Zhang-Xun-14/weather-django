from django.http import HttpResponse
from django.shortcuts import render


def weathers():
    import pyecharts.options as opts
    from pyecharts.charts import Line
    from pyecharts.globals import ThemeType
    from datetime import datetime
    from requests import get
    from lxml import etree

    data = get('https://tianqi.so.com/weather/101090511', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (' \
          'KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'})
    data.encoding = data.apparent_encoding

    will = etree.HTML(data.text).xpath(
        "//div[@class='weather-card']/ul/li/div/text()"
    )
    will = [w for w in will if w not in ("优", "良", "轻度", "中度", "重度", "严重")]
    xaxis = tuple("{}\n{}\n{}".format(s, r.strip(), d) for s, r, d in
                         zip(will[0::4], will[1::4], will[3::4]))
    low, high = zip(*[z.split('/', 1) for z in will[2::4]])

    weather_broken = Line(
        init_opts=opts.InitOpts(width="1500px", theme=ThemeType.CHALK)
    )
    weather_broken.add_xaxis(xaxis_data=xaxis)
    weather_broken.add_yaxis(
        series_name="最高气温", y_axis=tuple(h.strip('℃') for h in high),
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(type_="max", name="最大值"),
                  opts.MarkPointItem(type_="min", name="最小值")]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        )
    )
    weather_broken.add_yaxis(
        series_name="最低气温", y_axis=low,
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(
                    symbol="circle", type_="max", name="最高点"
                )
            ]
        )
    )
    weather_broken.set_global_opts(
        title_opts=opts.TitleOpts(
            title="未来15天气温变化", subtitle=datetime.now().strftime("%Y-%m-%d %H时%M分%S秒")
        ),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts={"interval": '0'}, type_="category",
            boundary_gap=False
        )
    )
    weather_broken.render_notebook()
    weather_broken.render('./templates/w/w.html')


def hello(request):
    # return HttpResponse("Hello world ! ")
    context = {'hello': 'Hello, welcome here!'}
    return render(request, 'index.html', context)


def weather_hello(request):
    weathers()
    return render(request, './w/w.html')
