import streamlit as st
import os
from extraction.pdf_parser import PDFParser
from processing.financial_data_processor import FinancialDataProcessor
from processing.json_formatter import JSONFormatter

# Configure page
st.set_page_config(page_title="Financial Extractor", layout="wide")
st.title("Financial Statement Processor")

uploaded_files = st.file_uploader(
    "Upload financial statements (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        with st.expander(f"Processing: {file.name}", expanded=True):
            try:
                # 1. Parse the PDF
                parser = PDFParser(file)
                
                # 2. Extract financial data
                raw_data = parser.find_financial_tables()
                st.write("Raw extracted data preview:", raw_data)  # Debug preview
                
                # 3. Process the data
                processor = FinancialDataProcessor(raw_data)
                processed_data = processor.process()
                
                # 4. Display JSON
                # In your app.py, modify the display section:
json_str = json_formatter.format()

# Validate JSON first
try:
    json.loads(json_str)  # This will raise an error if invalid
    st.subheader("Processed Financial Data")
    st.json(processed_data)  # Display the parsed data
    
    # Download button
    st.download_button(
        label="Download as JSON",
        data=json_str,
        file_name=f"{os.path.splitext(file.name)[0]}.json",
        mime="application/json"
    )
except json.JSONDecodeError as e:
    st.error(f"Invalid JSON generated: {str(e)}")
    st.text_area("Raw Problematic Data", json_str, height=300)
                
                # 5. Download option
                json_formatter = JSONFormatter(processed_data)
                st.download_button(
                    label="Download as JSON",
                    data=json_formatter.format(),
                    file_name=f"{os.path.splitext(file.name)[0]}.json",
                    mime="application/json"
                )
                
            except Exception as e:
                st.error(f"Failed to process {file.name}: {str(e)}")
            finally:
                parser.close()  # Ensure PDF is properly closed
else:
    st.info("Please upload PDF files to begin")
    