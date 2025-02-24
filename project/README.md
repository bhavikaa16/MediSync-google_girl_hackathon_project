# MEDISYNC - Medical Diagnostic Unified System Assistant 🏥

Welcome to **MEDISYNC**, a comprehensive medical diagnostic assistant designed for the GOOGLE GIRLS' HACKATHON, to simplify and enhance the workflow of healthcare professionals.This innovative system combines various diagnostic tools into a cohesive, user-friendly interface, making advanced medical analysis accessible to healthcare professionals worldwide. This README will guide you through the features and functionalities of this application, providing you with everything you need to start using MEDISYNC  effectively.





## Vision

Our vision is to democratize access to advanced medical diagnostics by creating an integrated platform that merges imaging analysis, pathology diagnostics, and risk assessment tools. This initiative aims to enhance patient care and improve medical decision-making processes.

## 🔍 Key Features Unveiled
MEDISYNC provides a range of modules to support various aspects of medical diagnostics:

1.**Advanced Medical Imaging Analysis**
2.**Comprehensive Pathology Diagnostics**
3.**AI-Powered Insurance Risk Assessment**

## Google Gemini Pro Vision Model:

-Multimodal Analysis: The model can simultaneously analyze text and images, allowing for comprehensive evaluations of medical data.
-Extended Context Window: With a context window of up to 1 million tokens, the model can maintain coherent conversations and handle complex queries effectively.
-Request Rate Limit : 2,000 requests per minute.

## Intelligent Medical Image Analysis

Automated analysis of X-rays, MRIs, and CT scans

-AI Analysis Capabilities:
     -Medical image interpretation
     -Abnormality detection
     -Diagnostic suggestions
     -Natural language report generation

-Research Integration:
     -Uses web scraping to find relevant medical research
     -Connects diagnosis with academic literature

-AI Workflow: Image Upload & Preprocessing:
     - Accepts multiple image formats (jpg, jpeg, png)
     - Processes images before AI analysis

Upload medical images and receive detailed analyses. The tool supports multiple image formats (JPG, JPEG, PNG).
![alt text](image.png)



### 2. Medical Pathology Diagnostics
-->User Interface Features: 
     - Two-column layout
     - Progress indicators
     - Error handling messages
     - Interactive buttons
-->Accuracy Metrics:     
     -Text Extraction: 90-92%
     -Information Categorization: 90-95%
     -Patient Info Extraction: 91-93%
     -Clinical Analysis: 85-90%
-->Report Generation Performance:
      -File Size: 100-200KB
      -Resolution: 300 DPI
      -Quality Score: 95%
Analyze medical reports to generate comprehensive pathology reports.

![alt text](image-1.png)






### 5. Insurance Risk Analysis

Upload user data images and calculate insurance risk percentages with detailed justifications.

![Screenshot (163)](https://github.com/user-attachments/assets/635d753f-e61d-4d3c-872a-e5cbb9464b26)




    ```

2. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**
    - Create a `.env` file in the root directory and add your Google API key.
    ```env
    GOOGLE_API_KEY=your_google_api_key
    ```

4. **Run the application:**
    ```sh
    streamlit run MEDUSA_AI.py
    ```

## Usage

### Navigation Menu

Select the desired module from the navigation menu at the top of the page.

### Medical Imaging Diagnostics

1. **Upload Image:** Choose one or more medical images to upload.
2. **Enter Prompt:** Use the default prompt or enter a custom prompt.
3. **Analyze Image:** Click to analyze the image and get a detailed report.
4. **Download Report:** Save the analysis as a PDF report.
5. **Related Research Papers:** View related research papers based on the analysis.



### Medical Pathology Diagnostics

1. **Upload Report:** Choose a medical report image to upload.
2. **Enter Prompt:** Use the default prompt or enter a custom prompt.
3. **Analyze Report:** Click to generate a comprehensive pathology report.



### Insurance Risk Analysis

1. **Upload User Data Image:** Choose an image containing user data to upload.
2. **Enter Prompt:** Use the default prompt or enter a custom prompt.
3. **Analyze Risk:** Click to calculate the insurance risk percentage and get a detailed justification.



## Additional Features

- **Latest Medical News:** View the latest medical news directly from the sidebar.
- **Customizable Reports:** Select from various report formats for personalized outputs.

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/swayam-the-coder/medusa-ai/issues).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

 
