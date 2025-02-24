import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from PIL import Image as PILImage
import io
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import feedparser
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

load_dotenv()

st.set_page_config(
    page_title="MEDISYNC", 
    page_icon="⚕️", 
    layout="wide", 
    initial_sidebar_state="expanded", 
)

st.markdown(
    """
    <style>
    body {
        background-color: #eae7dc;
        background-size: 1200px 800px;
        background-position: center;
        font-family: 'Arial', sans-serif;
    }
    .stApp {
        padding: 15px;
        border-radius: 5px;
        background-color: #eae7dc;
        background-position: center;
    }
    .stButton>button {
        background-color: #116466;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #d1e8e2
        color: #5c2018;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 1px solid #ccc;
        padding: 10px;
        font-size: 18px;
    }
    .stTextInput>div {
        display: flex;
        justify-content: center;
        margin-top: 80px; /* Adjust the value to move the input box downwards */
    }
    .stSidebar > div {
        background-color: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 5px;
    }
    .sidebar-emoji {
        text-align: center;
    }
    .sidebar-emoji img {
        width: 2in;
        height: 2in;
    }
    .chat-message {
        font-size: 18px;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)





@st.cache_resource
def load_model():
    """Loads the Gemini Pro Vision model using the API key from the environment."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Google API Key not found. Please set it in the .env file.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def analyze_image(image, prompt):
    """Analyzes the provided image using the Gemini model and returns the generated response."""
    try:
        model = load_model()
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        st.error(f"Error analyzing image: {e}")
        return None

def search_research_papers(query):
    """Searches Google Scholar for research papers related to the given query."""
    try:
        search_url = f"https://scholar.google.com/scholar?q={query}"
        response = requests.get(search_url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')
        papers = [
            {'title': item.select_one('.gs_rt').text, 'link': item.select_one('.gs_rt a')['href']}
            for item in soup.select('[data-lid]') if item.select_one('.gs_rt a')
        ]
        return papers
    except Exception as e:
        st.error(f"Error fetching research papers: {e}")
        return []

def fetch_rss_feed(feed_url):
    """Fetches and parses an RSS feed, returning a list of articles."""
    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo:
            st.error("Failed to fetch RSS feed. Invalid or unreachable URL.")
            return []

        articles = [
            {'title': entry.title, 'link': entry.link, 'published': entry.get('published', 'No publication date')}
            for entry in feed.entries
        ]
        return articles
    except Exception as e:
        st.error(f"Error fetching RSS feed: {e}")
        return []


def create_pathology_report(patient_info, service_info, specimens, theranostic_report):
    fig, ax = plt.subplots(figsize=(10, 12))

    def add_textbox(ax, x, y, width, height, header, text, wrap_text=True, fontsize=9, fontweight='normal', ha='left', va='top', line_height=0.02, color='white'):
        rect = patches.Rectangle((x, y), width, height, linewidth=1.5, edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        plt.text(x + 0.01, y + height - 0.01, header, ha=ha, va=va, fontsize=fontsize, fontweight='bold', family='DejaVu Sans')
        
        if wrap_text:
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + word) * 0.01 > width:
                    lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line += word + " "

            if current_line:
                lines.append(current_line)

            for i, line in enumerate(lines):
                if i * line_height < height - line_height:
                    plt.text(x + 0.01, y + height - 0.03 - i * line_height, line, ha=ha, va=va, fontsize=fontsize, fontweight=fontweight, family='DejaVu Sans', clip_on=True)
        else:
            plt.text(x + 0.01, y + height - 0.03, text, ha=ha, va=va, fontsize=fontsize, fontweight=fontweight, family='DejaVu Sans', clip_on=True)

    plt.text(0.5, 0.96, 'LABORATORY MEDICINE PROGRAM', ha='center', va='center', fontsize=15, family='DejaVu Sans', fontweight='bold')

    plt.text(0.5, 0.93, 'Surgical Pathology Consultation Report', ha='center', va='center', fontsize=13, family='DejaVu Sans', fontweight='bold')

    section_height = 0.8 / 4 

    add_textbox(ax, 0.05, 0.88 - section_height, 0.9, section_height, 'Patient Information', patient_info, wrap_text=False, fontsize=10, line_height=0.025, color='#E6F2FF')

    add_textbox(ax, 0.05, 0.88 - 2*section_height, 0.9, section_height, 'Observation', service_info, wrap_text=True, fontsize=10, line_height=0.025, color='#F5F5F5')

    add_textbox(ax, 0.05, 0.88 - 3*section_height, 0.9, section_height, 'Inferences', specimens, wrap_text=True, fontsize=10, line_height=0.025, color='#E6F2FF')

    add_textbox(ax, 0.05, 0.88 - 4*section_height, 0.9, section_height, 'Conclusion', theranostic_report, wrap_text=True, fontsize=10, line_height=0.025, color='#F5F5F5')

    plt.text(0.95, 0.01, 'Page 1 of 5', ha='right', va='center', fontsize=10, family='DejaVu Sans')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf_report(patient_info, service_info, specimens, theranostic_report, diagnosis, detailed_diagnosis, image_buffer, report_format):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle('Normal', fontName='Arial', fontSize=10, leading=12)
    styleH = ParagraphStyle('Heading1', fontName='Arial', fontSize=20, leading=20, alignment=1, spaceAfter=12, underline=True)
    styleH2 = ParagraphStyle('Heading2', fontName='Arial', fontSize=14, leading=14, spaceAfter=8)

    def add_background_and_border(canvas, doc, background_color):
        canvas.saveState()
        margin = 36
        canvas.setFillColor(background_color)
        canvas.rect(margin, margin, doc.pagesize[0] - 2 * margin, doc.pagesize[1] - 2 * margin, fill=1)
        canvas.setStrokeColor(colors.black)
        canvas.setLineWidth(2)
        canvas.rect(margin, margin, doc.pagesize[0] - 2 * margin, doc.pagesize[1] - 2 * margin)
        canvas.restoreState()

    format_details = {
        "Format 1": {"color": colors.lightblue, "header": "SWAYAM IMAGING CENTER"},
        "Format 2": {"color": colors.lightgreen, "header": "SWAYAM IMAGING CENTER"},
        "Format 3": {"color": colors.lightyellow, "header": "Medical Imaging Report"},
        "Format 4": {"color": colors.lightpink, "header": "IMAGING DIAGNOSTIC CENTER"},
        "Format 5": {"color": colors.lightgrey, "header": "RADIOLOGY REPORT"}
    }

    format_detail = format_details[report_format]
    elements.append(Paragraph(format_detail["header"], styleH))
    elements.append(Spacer(1, 12))
    elements.extend([
        Paragraph(f"Patient Information: {patient_info}", styleN),
        Paragraph(f"Observation: {service_info}", styleN),
        Paragraph(f"Inferences: {specimens}", styleN),
        Spacer(1, 12),
        Paragraph("DIAGNOSIS", styleH2),
        Paragraph(detailed_diagnosis, styleN),
        Spacer(1, 12),
        Paragraph("Conclusion:", styleH2),
        Paragraph(theranostic_report, styleN),
        Spacer(1, 12),
        Paragraph("X-Ray Image:", styleH2),
        Image(image_buffer, width=5 * inch, height=3.5 * inch),
        Spacer(1, 12),
        Paragraph("IMPRESSION", styleH2),
        Paragraph(diagnosis, styleN),
        Spacer(1, 12),
        Paragraph("ADVICE", styleH2),
        Paragraph("Clinical correlation.", styleN),
        Spacer(1, 12),
        Paragraph("Radiologic Technologists: MSC, PGDM", styleN),
        Paragraph("Dr. Payal Shah (MD, Radiologist)", styleN),
        Paragraph("Dr. Vimal Shah (MD, Radiologist)", styleN)
    ])

    doc.build(elements, onFirstPage=lambda canvas, doc: add_background_and_border(canvas, doc, format_detail["color"]), onLaterPages=lambda canvas, doc: add_background_and_border(canvas, doc, format_detail["color"]))
    buffer.seek(0)
    return buffer
def display_instructions(page):
    st.sidebar.header("Instructions")

    instructions = {
        "Medical Imaging Diagnostics": """
            1. **Upload Images**: Use the file uploader to upload one or more medical images.
            2. **Enter Prompt**: Enter your prompt or use the default one provided.
            3. **Analyze Image**: Click 'Analyze Image' to get the analysis.
            4. **Regenerate Analysis**: If not satisfied, click 'Regenerate Analysis'.
            5. **View Research Papers**: View related research papers based on the analysis.
        """,
        
        "Medical Pathology Diagnostics": """
            1. **Upload Report Image**: Upload a medical report image using the file uploader.
            2. **Enter Prompt**: Enter your prompt or use the default one provided.
            3. **Analyze Report**: Click 'Analyze Report' to get the analysis and generate the pathology report.
        """,
        
        "Insurance Risk Analysis": """
            1. **Upload User Data Image**: Upload an image containing user data using the file uploader.
            2. **Enter Prompt**: Enter your prompt or use the default one provided.
            3. **Analyze Risk**: Click 'Analyze Risk' to get the percentage risk and detailed justification.
        """,
    }

    st.sidebar.markdown(instructions.get(page, ""))


def display_medical_news():
    st.sidebar.header("📰 Latest Medical News")
    show_news_button = st.sidebar.button("Show Medical News")
    if show_news_button:
        feed_url = "https://health.economictimes.indiatimes.com/rss/topstories"
        articles = fetch_rss_feed(feed_url)
        if articles:
            for article in articles:
                st.sidebar.markdown(
                    f"<div style='font-size: 0.9rem;'><b>Title:</b> <a href='{article['link']}'>{article['title']}</a><br><b>Published:</b> {article['published']}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.sidebar.info("No articles available at the moment.")

def medical_imaging_diagnostics():
    st.header("Medical Imaging Diagnostics")

    st.header("Upload Image")
    uploaded_files = st.file_uploader(
        "Choose medical images...", 
        type=["jpg", "jpeg", "png"], 
        accept_multiple_files=True
    )

    st.header("Analysis Options")
    default_prompt = "Analyze this medical image. Describe what you see, identify any abnormalities, and suggest potential diagnoses."
    prompt = st.text_area(
        "Enter your prompt:", 
        value=default_prompt, 
        height=100
    )

    analyze_button = st.button("Analyze Image")
    regenerate_button = st.button("Regenerate Analysis")

    st.header("Report Format")
    report_format = st.selectbox(
        "Choose Report Format:", 
        ["Format 1", "Format 2", "Format 3", "Format 4", "Format 5"]
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            col1, col2 = st.columns(2)

            with col1:
                st.header("Uploaded Image")
                image = PILImage.open(uploaded_file)
                st.image(
                    image, 
                    caption="Uploaded Medical Image", 
                    use_column_width=True
                )

            with col2:
                st.header("Image Analysis")
                if analyze_button or regenerate_button:
                    with st.spinner("Analyzing the image..."):
                        try:
                            analysis = analyze_image(image, prompt)
                            st.markdown(analysis)

                            detailed_diagnosis = analysis
                            diagnosis = analysis.split('.')[0]

                            img_buffer = io.BytesIO()
                            image.save(img_buffer, format='PNG')
                            img_buffer.seek(0)

                            pdf_buffer = create_pdf_report(
                                "Yashvi M. Patel", 
                                21, 
                                "Female", 
                                diagnosis, 
                                detailed_diagnosis, 
                                "", 
                                img_buffer, 
                                report_format
                            )
                            st.download_button(
                                label="Download Report", 
                                data=pdf_buffer, 
                                file_name="medical_report.pdf", 
                                mime="application/pdf"
                            )

                            st.header("Related Research Papers")
                            papers = search_research_papers(diagnosis)
                            for paper in papers:
                                st.markdown(f"[{paper['title']}]({paper['link']})")

                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                else:
                    st.info("Click 'Analyze Image' to start the analysis.")





def extract_info_from_analysis(analysis):
    theranostic_report = """lorem ipsum
    lorem ipsum
    lorem ipsum"""
    patient_info = "Patient Name:         N.A.\n" \
                   "MRN:                          N.A.\n" \
                   "DOB:                          N.A. (Age: N.A.)\n" \
                   "Gender:                      N.A.\n" \
                   "HCN:                          N.A.\n" \
                   "Ordering MD:            N.A.\n" \
                   "Copy To:                   N.A.\n" \
                   "                                      N.A."

    service_info = """lorem ipsum
    lorem ipsum
    lorem ipsum"""

    specimens = """lorem ipsum
    lorem ipsum
    lorem ipsum"""

    if "Patient Name:" in analysis:
        patient_info = analysis.split("Patient Name:")[1].split("Observation:")[0].strip()
    if "Observation:" in analysis:
        service_info = analysis.split("Observation:")[1].split("Inferences:")[0].strip()
    if "Inferences:" in analysis:
        specimens= analysis.split("Inferences:")[1].split("Conclusion:")[0].strip()    
    if "Conclusion:" in analysis:
        theranostic_report = analysis.split("Conclusion:")[1].strip()     

    return patient_info, service_info, specimens, theranostic_report

def medical_pathology_diagnostics():
    st.header("Medical Pathology Diagnostics")

    st.header("Upload Report")
    uploaded_file = st.file_uploader("Choose a medical report image...", type=["jpg", "jpeg", "png"])
    
    st.header("Analysis Options")
    default_prompt = """You are a highly skilled medical professional specializing in pathology. Analyze the uploaded medical pathology report and extract the following details accurately:

1. **Patient Information:**
   - Patient Name
   - Medical Record Number (MRN)
   - Date of Birth (DOB) with Age
   - Gender
   - Health Card Number (HCN)
   - Ordering Physician
   - Copy To (if any)

2. **Observation:** Summarize key observations.

3. **Inferences:** Provide main inferences derived from observations.

4. **Conclusion:** State the final conclusion or diagnosis.

**Format for Output:**

- **Patient Information:**
  - Patient Name: [Extracted Name]
  - MRN: [Extracted MRN]
  - DOB: [Extracted DOB] (Age: [Extracted Age])
  - Gender: [Extracted Gender]
  - HCN: [Extracted HCN]
  - Ordering Physician: [Extracted Physician]
  - Copy To: [Extracted Copy To (if any)]

- **Observation:** [Summarized Observations]

- **Inferences:** [Summarized Inferences]

- **Conclusion:** [Final Conclusion or Diagnosis]

Ensure that the extracted information is precise and well-structured.
"""

    prompt = st.text_area("Enter your prompt:", value=default_prompt, height=100)
    analyze_button = st.button("Analyze Report")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Uploaded Report")
        if uploaded_file:
            image = PILImage.open(uploaded_file)
            st.image(image, caption="Uploaded Medical Report", use_column_width=True)
        else:
            st.info("Please upload an image.")

    with col2:
        st.header("Report Analysis")
        if uploaded_file and analyze_button:
            with st.spinner("Analyzing the image..."):
                try:
                    image = PILImage.open(uploaded_file)
                    analysis = analyze_image(image, prompt)
                    patient_info, service_info, specimens, theranostic_report = extract_info_from_analysis(analysis)
                    
                    report_buf = create_pathology_report(patient_info, service_info, specimens, theranostic_report)
                    st.image(report_buf, caption="Pathology Report", use_column_width=True)
                    st.download_button(label="Download Report Image", data=report_buf, file_name="pathology_report.png", mime="image/png")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif not uploaded_file:
            st.info("Upload an image and click 'Analyze Report' to proceed.")
        elif not analyze_button:
            st.info("Click 'Analyze Report' to begin the analysis.")


    
   

def insurance_risk_analysis():
    st.header("Insurance Risk Analysis")

    st.header("Upload User Data Image")
    uploaded_file = st.file_uploader(
        "Choose an image containing user data...", 
        type=["jpg", "jpeg", "png"]
    )

    st.header("Analysis Options")
    default_prompt = """You are a highly skilled insurance analyst. Please analyze the uploaded image containing user data and calculate the insurance risk percentage. Provide a detailed justification for the calculated risk percentage based on the data.

**Format for Output:**

- **Risk Percentage:** [Calculated Percentage]%
- **Justification:** [Detailed Justification]

Ensure that the calculated risk and justification are accurate and well-explained."""

    prompt = st.text_area(
        "Enter your prompt:", 
        value=default_prompt, 
        height=100
    )

    analyze_button = st.button("Analyze Risk")

    col1, col2 = st.columns(2)

    with col1:
        st.header("Uploaded User Data Image")
        if uploaded_file:
            image = PILImage.open(uploaded_file)
            st.image(
                image, 
                caption="Uploaded User Data Image", 
                use_column_width=True
            )
        else:
            st.info("Please upload an image using the uploader.")

    with col2:
        st.header("Risk Analysis")
        if uploaded_file and analyze_button:
            with st.spinner("Analyzing the image..."):
                try:
                    analysis = analyze_image(PILImage.open(uploaded_file), prompt)
                    st.markdown(analysis)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        elif not uploaded_file:
            st.info("Upload an image and click 'Analyze Risk' to see the results.")
        elif not analyze_button:
            st.info("Click 'Analyze Risk' to start the analysis.")



def main():
    st.sidebar.markdown(
        "<h3 style='text-align: center; color: #116466; font-family: comic sans ms;'>🔍 MEDUSA AI</h3>",
        unsafe_allow_html=True
    )
    
    display_instructions(selected)
    display_medical_news()

    diagnostic_tools = {
        "Medical Imaging Diagnostics": medical_imaging_diagnostics,
        "Medical Transcription": medical_transcription,
        "Medical Pathology Diagnostics": medical_pathology_diagnostics,
        "Medical Coding": medical_coding,
        "Insurance Risk Analysis": insurance_risk_analysis,
        "Treatment and Diet Plan Generator": treatment_diet_plan_generator,
    }

    diagnostic_tools.get(selected, lambda: st.info("Please select a diagnostic tool"))()

if __name__ == "__main__":
    main()
