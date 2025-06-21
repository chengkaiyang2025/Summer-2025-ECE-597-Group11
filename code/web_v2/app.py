import os.path
import uuid

import streamlit as st
import random
import time
from dataset.output import kaggle_spam_sample
from response_generator import MODEL_CHOICES, MODEL_LR, MODEL_NB, ResponseService, ResponseMessage

st.set_page_config(
    page_title="UVic Spam Detector",     # 标签页标题
    page_icon="📧",                      # 图标（可以是 emoji 或路径）
    # layout="wide"                        # 可选：'centered' or 'wide'
)
st.header("Got an email in your UVic inbox...")
st.subheader("... Worried it might be phishing or spam? 🤔")


@st.cache_resource(show_spinner="Loading models")
def get_response_service() -> ResponseService:
    return ResponseService()

service = get_response_service()

st.caption("😊Let [our model](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11) help you spot if your email is a phishing scam!!")
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,  #  DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Step 1: 初始随机样本
if "sample" not in st.session_state:
    st.session_state.sample = random.choice(kaggle_spam_sample)


# Step 3: 使用当前样本内容
sample = st.session_state.sample
email_subject = st.text_input("Email Subject", value=sample["subject"])
email_body = st.text_area("Email Body:", height=250, value=sample["body"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
#
# Accept user input
model_selected = st.selectbox(
    'Choose a model',
    MODEL_CHOICES
)
BASE = "💡Any feedback on the webpage? Feel free to create a [Github Issue](https://github.com/chengkaiyang2025/Summer-2025-ECE-597-Group11/issues)"


def output_answer_with_funny_emoji(lines:list):
    for line in lines:
        message_placeholder = st.empty()
        full_response = ""

        for chunk in line.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            # TODO houmian
            emoji_r = random.choice([
                "1😄",
                "^",
                "^$",
                "🎉",
                "🎢"
            ])
            message_placeholder.markdown(full_response + emoji_r)
            message_placeholder.markdown(full_response)


col1, col2 = st.columns([1, 1])  # 左列 1x，右列 3x 更突出 Detect


with col1:
    st.button("🎲 Generate Sample", help="Click to load a new random email",
              on_click=lambda: st.session_state.update(sample=random.choice(kaggle_spam_sample)),
              use_container_width=True)
with col2:
    detect_clicked = st.button("🚨 Detect", type="primary", use_container_width=True)

if detect_clicked:

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resp:ResponseMessage = service.response(model_selected, email_subject, email_body)
    with st.chat_message("assistant"):

        output_answer_with_funny_emoji(resp.md_content_list)
        if resp.image_path and len(resp.image_path)>0 and os.path.exists(resp.image_path):
            st.image(resp.image_path)
        st.caption(BASE)

    st.session_state.messages.append({"role": "assistant",
                                      "md_content_list": resp.md_content_list,
                                      "image_path":resp.image_path,
                                      "timestamp": ts})
    st.session_state.messages.append({"role": "user",
                                      "content": {
                                          "email_subject":email_subject,
                                          "email_body":email_body
                                      }
                                     ,"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})



if len(st.session_state.messages)>0:
    st.markdown("----------------------------")

    st.subheader("💬 Check History")
    for message in reversed(st.session_state.messages):  #
        with st.chat_message(message["role"]):

            # st.markdown("----------------------------")
            timestamp = message.get("timestamp", "")
            if timestamp:
                st.caption(f"🕒 {timestamp}")
            if message.get("role") == "assistant":
                st.caption(f"{model_selected}")
                for x in message["md_content_list"]:
                    st.markdown(x)
                if message['image_path'] and len(message['image_path'])>0 and os.path.exists(message['image_path']):
                    st.image(message['image_path'])
                st.markdown("****************")

            elif message["role"] == "user":
                st.text_area("Email Subject", value=message["content"]["email_subject"], disabled=True, key=str(uuid.uuid4()))

                st.text_area("Email Body", value=message["content"]["email_body"], height=250, disabled=True, key=str(uuid.uuid4()))


