import streamlit as st
import pandas as pd
import os
from openai import OpenAI



# ================= 1. 页面基础配置 =================
st.set_page_config(page_title="电商全链路分析 Demo", page_icon="🛒", layout="wide")
st.write("✅ 页面已经启动，正在加载")
st.title("🛒 双11电商全链路交互分析 Demo")
st.markdown("基于 7 万条电商数据 + DeepSeek 大模型辅助生成")

# ================= 2. 初始化 DeepSeek 客户端 =================
# ⚠️ 请在这里填入你的 DeepSeek API Key
DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY" 

@st.cache_resource
def get_ai_client():
    try:
        key = st.secrets["DEEPSEEK_API_KEY"]
        return OpenAI(api_key=key, base_url="https://api.deepseek.com/v1")
    except Exception:
        return None

client = get_ai_client()

if st.button("让AI分析当前数据组合"):
    if client is None:
        st.warning("未配置API密钥，AI分析功能不可用")
    else:
        # 这里放原来调用DeepSeek、生成报告的代码
        pass

# ================= 3. 数据读取与过滤 =================
file_path = 'fact_order.csv'
if not os.path.exists(file_path):
    st.error(f"❌ 找不到文件 {file_path}，请确保它和 app2.py 在同一个文件夹下！")
    st.stop()

# 自动处理编码
try:
    df_order = pd.read_csv(file_path, encoding='utf-8')
except:
    df_order = pd.read_csv(file_path, encoding='gbk')

# 侧边栏筛选器
st.sidebar.header("数据筛选")
campaign_list = ["双11满减", "百亿补贴", "品牌特卖", "无"]
campaign_filter = st.sidebar.multiselect("选择营销活动", campaign_list, default=["双11满减", "百亿补贴"])

# ================= 4. 数据计算与展示 =================
if campaign_filter:
    filtered_df = df_order[df_order['campaign'].isin(campaign_filter)]
    
    # 计算核心指标
    valid_pay = pd.to_numeric(filtered_df[filtered_df['order_status'] == '交易成功']['pay_amount'], errors='coerce')
    gmv = valid_pay.sum()
    order_count = filtered_df[filtered_df['order_status'] == '交易成功']['order_id'].nunique()
    aov = gmv / order_count if order_count > 0 else 0
    
    # 顶部 KPI 卡片
    col1, col2, col3 = st.columns(3)
    col1.metric(label="筛选后总 GMV", value=f"¥ {gmv:,.2f}")
    col2.metric(label="成功订单数", value=f"{order_count:,}")
    col3.metric(label="客单价 (AOV)", value=f"¥ {aov:,.2f}")
    
    # A/B 测试图表
    st.subheader("A/B 测试：各营销活动 GMV 对比")
    success_orders = filtered_df[filtered_df['order_status'] == '交易成功'].copy()
    success_orders['pay_amount'] = pd.to_numeric(success_orders['pay_amount'], errors='coerce')
    chart_data = success_orders.groupby('campaign')['pay_amount'].sum()
    st.bar_chart(chart_data)
    
else:
    st.warning("⚠️ 请在左侧至少选择一个营销活动！")

# ================= 5. 动态 AI 归因分析（接入 DeepSeek API） =================
st.subheader("🤖 DeepSeek 实时 AI 业务洞察")
st.markdown("点击下方按钮，AI 将根据你当前筛选的数据和底层业务痛点，生成定制化策略。")

if st.button("✨ 让 AI 分析当前数据组合", type="primary"):
    if not campaign_filter:
        st.error("请先在上方选择营销活动！")
    elif DEEPSEEK_API_KEY == "sk-你的DeepSeek_API_Key":
        st.error("⚠️ 请先在代码中填入你的真实 DeepSeek API Key！")
    else:
        selected_str = "、".join(campaign_filter)
        
        # 核心：构建给 AI 的 Prompt
        prompt = f"""
        你是一个资深电商商业分析师。
        当前我在双11大促看板上，筛选了以下营销活动：{selected_str}。
        筛选后的大盘数据为：总GMV {gmv:,.2f}元，成功订单数 {order_count}单，客单价 {aov:,.2f}元。
        
        已知底层业务痛点：
        1. 美妆类目差评率高达 11%，核心原因为包装破损。
        2. 手机数码类目客单价极高，但投诉单数全平台最高（28单）。
        
        请结合上述筛选数据，用不超过 150 字，输出 2 条极度务实的业务优化建议。要求语气专业，直接上干货，不要说废话。
        """

        with st.spinner("DeepSeek 正在阅读数据并思考中..."):
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个懂业务、懂数据的资深电商商业分析师。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )
                ai_result = response.choices[0].message.content
                st.success("### AI 洞察报告")
                st.info(ai_result)
            except Exception as e:
                st.error(f"AI 引擎调用失败，请检查网络或 API Key。错误信息：{e}")
