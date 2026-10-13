import streamlit as st
from openai import OpenAI

# 从 Streamlit Secrets 读取 API Key（安全，不会暴露在代码里）
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

st.set_page_config(page_title="AI 周报生成器", page_icon="📝")
st.title("📝 AI 周报生成器")
st.caption("把你本周的零散记录粘贴进来，AI 帮你整理成结构化周报。")

# 输入区域
notes = st.text_area(
    "粘贴你本周的零散工作记录",
    height=200,
    placeholder="例如：\n- 改了登录页的样式\n- 修复了3个bug\n- 下周要做支付功能\n- 和产品开了2次会"
)

# 可选：选择语气
tone = st.selectbox("选择周报语气", ["正式", "简洁", "OKR 风格"])

# 生成按钮
if st.button("生成周报", type="primary"):
    if not notes.strip():
        st.warning("请先粘贴一些工作记录")
    else:
        with st.spinner("AI 正在整理中..."):
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": f"""你是专业周报助手。请把用户的零散记录整理成结构化周报。
语气要求：{tone}。
只根据用户输入的内容整理，不要编造任何信息。
输出格式：
一、本周完成
（列出具体完成事项，动词开头，尽量量化）
二、问题与风险
（列出遇到的问题或风险，没有就写"无"）
三、下周计划
（列出下周计划，动词开头）
四、需要协调
（需要其他部门或同事配合的事项，没有就写"无"）
要求：简洁、专业、适合直接发给上级。"""
                    },
                    {"role": "user", "content": notes}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            result = resp.choices[0].message.content
            st.markdown("### 📄 生成的周报")
            st.markdown(result)

            # 复制按钮（Streamlit 原生支持一键复制）
            st.code(result, language=None)
            st.caption("点击右上角复制图标即可复制全文")
