# 双十一电商全链路经营盘｜Streamlit数据分析项目
> 会计+数据分析方向项目，电商大盘指标、流量、营销、商品结构、风控全链路分析

## ✨ 项目介绍
模拟电商双十一经营数据集，完成数据清洗、指标体系搭建、多维度归因分析；
使用Streamlit搭建交互式看板，搭配Tableau可视化，输出经营分析报告，定位流量、转化、商品风险问题，给出运营策略。
**技术栈：Python, Streamlit, Pandas, Plotly, Tableau, Jupyter Notebook**

## 📁 文件说明
- app2.py：Streamlit交互式分析主程序
- 数据集.ipynb：数据清洗、EDA探索、指标计算全过程
- 双十一经营盘可视化.twb：Tableau大屏看板
- “双十一”电商全链路经营盘.pdf：完整项目分析报告
- assets/：项目截图
- 01_大盘指标.csv ~ 06_风控质量.csv：汇总指标表
- dim_product.csv、dim_user.csv：商品、用户维度表
- fact_order.csv、fact_review.csv、fact_traffic.csv：订单、评价、流量事实表

## 🚀 运行方式
```bash
pip install -r requirements.txt
streamlit run app2.py


## 📊 功能模块

1. 大盘指标：GMV、转化率、客单价、支付金额监控
2. 流量质量：渠道来源、点击率、转化漏斗
3. 营销活动效果：活动 ROI、补贴效益
4. 新老客贡献、商品结构分析
5. 订单风控质量识别

## 🖼️ 演示截图
![dashboard](assets/demo截图.png)
![dashboard2](assets/demo截图2.png)

## 🔗 在线演示
👉 【部署完成后，把 Streamlit 链接粘贴在这里】


