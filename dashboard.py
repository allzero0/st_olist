import streamlit as st
import pandas as pd
import os
from PIL import Image

# 페이지 설정
st.set_page_config(
    page_title="Olist 데이터 분석 대시보드",
    page_icon="📊",
    layout="wide"
)

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_PATH = os.path.join(BASE_DIR, "report", "integrated_analysis_report.md")
IMAGE_DIR = os.path.join(BASE_DIR, "images")
DATA_PATH = "/Users/dayoungoh/icd6/project1/output_data/transaction_level_table.csv"

def load_markdown(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    st.title("📊 Olist 이커머스 통합 분석 리포트")
    st.markdown("---")

    # 사이드바 설정
    st.sidebar.header("분석 메뉴")
    menu = st.sidebar.radio(
        "이동하기",
        ["분석 보고서 상보", "고객 여정 분석", "재구매/리텐션 상세", "데이터 원본 확인", "분석 인사이트 요약"]
    )

    if menu == "분석 보고서 상보":
        if os.path.exists(REPORT_PATH):
            content = load_markdown(REPORT_PATH)
            sections = content.split("---")
            
            for section in sections:
                if "![" in section:
                    lines = section.split("\n")
                    for line in lines:
                        if line.startswith("!["):
                            img_file_part = line.split("](")[1].split(")")[0]
                            # 경로가 sub-folder일 수 있음 (./images/reorder/... 또는 ./images/journey/...)
                            img_rel_path = img_file_part.replace("./images/", "")
                            img_path = os.path.join(IMAGE_DIR, img_rel_path)
                            
                            if os.path.exists(img_path):
                                img = Image.open(img_path)
                                st.image(img, use_container_width=True)
                            else:
                                st.warning(f"이미지를 찾을 수 없습니다: {img_rel_path}")
                        else:
                            st.markdown(line)
                else:
                    st.markdown(section)
        else:
            st.error("보고서 파일을 찾을 수 없습니다.")

    elif menu == "고객 여정 분석":
        JOURNEY_REPORT_PATH = os.path.join(BASE_DIR, "report", "customer_journey_report.md")
        if os.path.exists(JOURNEY_REPORT_PATH):
            content = load_markdown(JOURNEY_REPORT_PATH)
            st.markdown(content)
            
            st.subheader("📊 단계별 핵심 지표")
            col1, col2 = st.columns(2)
            with col1:
                st.image(os.path.join(IMAGE_DIR, "journey", "stage1_info_impact.png"), caption="정보 영향력")
                st.image(os.path.join(IMAGE_DIR, "journey", "stage2_shipping_sensitivity.png"), caption="배송비 민감도")
            with col2:
                st.image(os.path.join(IMAGE_DIR, "journey", "stage3_delivery_impact.png"), caption="배송 지연 여파")
                st.image(os.path.join(IMAGE_DIR, "journey", "stage4_satisfaction_corr.png"), caption="만족도 상관관계")
        else:
            st.error("고객 여정 분석 보고서를 찾을 수 없습니다.")

    elif menu == "재구매/리텐션 상세":
        REORDER_REPORT_PATH = os.path.join(BASE_DIR, "report", "reorder_analysis_report.md")
        if os.path.exists(REORDER_REPORT_PATH):
            content = load_markdown(REORDER_REPORT_PATH)
            st.markdown(content)
            
            # 이미지 수동 표시 (보고서 내 링크가 상대경로라 깨질 수 있음)
            st.subheader("📊 시각화 데이터")
            col1, col2 = st.columns(2)
            with col1:
                st.image(os.path.join(IMAGE_DIR, "reorder", "cohort_retention_heatmap.png"), caption="코호트 리텐션")
                st.image(os.path.join(IMAGE_DIR, "reorder", "interpurchase_interval_dist.png"), caption="구매 간격 분포")
            with col2:
                st.image(os.path.join(IMAGE_DIR, "reorder", "category_reorder_rate.png"), caption="카테고리별 재구매율")
        else:
            st.error("재구매 분석 보고서를 찾을 수 없습니다.")

    elif menu == "데이터 원본 확인":
        st.subheader("📁 트랜잭션 레벨 데이터 (상위 100행)")
        if os.path.exists(DATA_PATH):
            df = pd.read_csv(DATA_PATH, nrows=100)
            st.dataframe(df)
            
            st.download_button(
                label="CSV 데이터 다운로드",
                data=pd.read_csv(DATA_PATH).to_csv(index=False).encode('utf-8'),
                file_name='transaction_level_table.csv',
                mime='text/csv',
            )
        else:
            st.error("데이터 파일을 찾을 수 없습니다.")

    elif menu == "분석 인사이트 요약":
        st.subheader("💡 핵심 비즈니스 인사이트")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**상품 및 가격 최적화**\n\n- 명칭 50자, 사진 2~3장이 최적\n- 주력가는 100 BRL 전후 권장")
            st.success("**품질 및 만족도**\n\n- 취소율 0.48% (양호)\n- 1점 리뷰 대비 주문 관리 필수")
        with col2:
            st.warning("**리텐션 전략**\n\n- 재구매율: **3.05%** (매우 낮음)\n- 평균 구매 간격: **112일**\n- CRM 마케팅을 통한 충성도 강화 필요")

if __name__ == "__main__":
    main()
