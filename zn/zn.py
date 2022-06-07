from pyecharts.globals import CurrentConfig, OnlineHostType
from pyecharts import options as opts  # 图形设置
from pyecharts.charts import Sankey  # 导入桑基图型的类

import pandas as pd
import numpy as np
import json
from pySankey.sankey import sankey

df = pd.read_excel("zn.xlsx")  # 直接写名字
df = df.loc[~(df["start_city"] == df["to_city"])]
print(df.head())

import matplotlib.pyplot as plt


plt.rcParams["font.family"] = ["Heiti TC"]


# 有中文出现的情况，需要u'内容'


# Create Sankey diagram again
sankey(
    left=df["start_city"],
    right=df["to_city"],
    leftWeight=df["bill供应链2021"],
    rightWeight=df["bill供应链2021"],
    aspect=20,
    fontsize=20,
)

# Get current figure
fig = plt.gcf()

# Set size in inches
fig.set_size_inches(6, 6)

# Set the color of the background to white
fig.set_facecolor("w")

# Save the figure
#
fig.savefig("customers-goods.png", bbox_inches="tight", dpi=150)
