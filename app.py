import streamlit as st

from resume_parser import extract_resume_text
from jd_parser import extract_jd_text
from analyzer import analyze_match


st.set_page_config(
    page_title="Smart Resume Screening",
    page_icon="📄",
    layout="wide",
)


def main():
    st.title("📄 Smart Resume Screening – AI-Assisted ATS Match")
    st.write(
        "Upload your **resume** and a **job description** to get a rough ATS-style match score, "
        "missing keywords, and improvement hints. This is a learning project – not a real ATS."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1️⃣ Upload Resume")
        resume_file = st.file_uploader(
            "Upload your resume (PDF or DOCX)",
            type=["pdf", "docx"],
            key="resume_file",
        )

    with col2:
        st.subheader("2️⃣ Job Description")
        jd_text_manual = st.text_area(
            "Paste Job Description (recommended)",
            height=180,
            placeholder="Paste the JD here...",
        )
        jd_file = st.file_uploader(
            "Or upload JD file (PDF/TXT)",
            type=["pdf", "txt"],
            key="jd_file",
        )

    if st.button("🔍 Analyze Match", type="primary"):
        if resume_file is None:
            st.error("Please upload a resume.")
            return

        resume_text = extract_resume_text(resume_file)
        jd_text = extract_jd_text(jd_file, jd_text_manual)

        if resume_text is None:
            st.error("Unsupported resume format. Use PDF or DOCX.")
            return
        if jd_text is None:
            st.error("Please provide a job description (paste text or upload file).")
            return

        result = analyze_match(resume_text, jd_text)

        st.success(f"Estimated Match Score: **{result['score']}%**")

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("✅ Matched Keywords")
            if result["matched_keywords"]:
                st.write(", ".join(result["matched_keywords"]))
            else:
                st.write("No strong keyword matches detected yet.")

        with col_b:
            st.subheader("⚠️ Missing Keywords (Consider adding if relevant)")
            if result["missing_keywords"]:
                st.write(", ".join(result["missing_keywords"][:50]))
            else:
                st.write("Great! No major missing keywords found.")

        st.subheader("📊 Top Keywords in Your Resume")
        freq_data = result["resume_keyword_frequency"]
        if freq_data:
            st.table(freq_data)
        else:
            st.write("Could not extract enough text from the resume.")


if __name__ == "__main__":
    main()
