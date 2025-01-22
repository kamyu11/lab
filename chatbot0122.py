import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# Streamlit UI 설정
st.title("나의 챗봇")

# 사이드바에 OpenAI API 키 입력 필드 생성
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# OpenAI API 클라이언트 초기화
if api_key:
    openai = OpenAI(api_key=api_key)
else:
    st.sidebar.warning("API 키를 입력하세요.")

# 대화 기록 저장
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 사용자 입력
user_input = st.text_input("질문을 입력하세요", label_visibility="collapsed")

# 사용자 입력 처리
if user_input and api_key:
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
