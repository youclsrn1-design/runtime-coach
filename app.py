import streamlit as st
import os
import sys
from io import StringIO

st.set_page_config(page_title="AI 강의 자료 뷰어", layout="centered")

# --- 기존 파일 청소기 ---
def cleanup_files():
    for ext in ['png', 'jpg', 'mp3', 'mp4', 'pdf', 'pptx']:
        if os.path.exists(f"output.{ext}"):
            os.remove(f"output.{ext}")

# --- 메인 UI ---
st.markdown("## 🎓 AI 마스터 강의 생성기")
st.write("제미나이가 짜준 코드를 넣으면 이미지, 오디오, 영상이 한 번에 구워집니다.")

# 핵심: 오프라인/온라인 강의 모드 선택 토글
audio_mode = st.toggle("🔊 오디오 재생 켜기 (온라인 VOD 모드)", value=True)
if not audio_mode:
    st.info("🔇 현재 오프라인 모드입니다. (생성된 음성이 화면에 표시되지 않습니다)")

user_code = st.text_area(
    "여기에 코드를 붙여넣으세요:", 
    height=250, 
    placeholder="AI에게 output.png(슬라이드), output.mp3(음성), output.mp4(영상)로 저장해달라고 요청하세요."
)

if st.button("🚀 강의 자료 굽기", use_container_width=True):
    cleanup_files()
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    with st.spinner("서버가 강의 자료를 열심히 굽고 있습니다... ⏳"):
        try:
            # 코드 실행!
            exec(user_code)
            sys.stdout = old_stdout
            
            st.success("✅ 강의 자료가 성공적으로 완성되었습니다!")
            st.divider()
            
            st.markdown("### 👀 강의 미리보기 (PPT 스타일)")
            
            file_found = False
            
            # 1. 슬라이드 (이미지) 출력
            if os.path.exists("output.png"):
                file_found = True
                st.markdown("**[1] 슬라이드 자료**")
                st.image("output.png", use_container_width=True)
                with open("output.png", "rb") as file:
                    st.download_button("📥 이미지 다운로드", data=file, file_name="slide.png", mime="image/png")
            
            # 2. 오디오 (음성) 출력 - 토글이 ON일 때만 보임
            if os.path.exists("output.mp3"):
                file_found = True
                if audio_mode:
                    st.markdown("**[2] AI 강의 음성**")
                    st.audio("output.mp3")
                    with open("output.mp3", "rb") as file:
                        st.download_button("📥 음성 다운로드", data=file, file_name="voice.mp3", mime="audio/mp3")
            
            # 3. 비디오 (보충 영상) 출력
            if os.path.exists("output.mp4"):
                file_found = True
                st.markdown("**[3] 보충 설명 영상**")
                st.video("output.mp4")
                with open("output.mp4", "rb") as file:
                    st.download_button("📥 영상 다운로드", data=file, file_name="video.mp4", mime="video/mp4")
                    
            if not file_found:
                st.warning("⚠️ 코드는 실행되었지만 결과물(output.png, output.mp3, output.mp4)이 없습니다.")
                
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"❌ 에러 발생:\n{e}")
