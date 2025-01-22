import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
api_key = "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"
openai = OpenAI(api_key=api_key)

# 챗봇 이름
st.title("나의 챗봇")

# 대화 기록 저장
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사용자 입력
user_input = st.text_input("질문을 입력하세요", label_visibility="collapsed")

# 사용자 입력 처리
if user_input:
    # 대화 기록에 사용자 입력 추가
    st.session_state['chat_history'].append({"role": "user", "content": user_input})

    try:
        # OpenAI API 호출
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state['chat_history']
        )

        # AI 응답 추가
        ai_response = response.choices[0].message['content']
        st.session_state['chat_history'].append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

# 대화 기록 출력
for chat in st.session_state['chat_history']:
    if chat['role'] == 'user':
        st.markdown(f"<div style='text-align: right;'>{chat['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left;'>{chat['content']}</div>", unsafe_allow_html=True)
