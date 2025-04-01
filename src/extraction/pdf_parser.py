import pdfplumber
import pandas as pd
from typing import Dict, List
import re

class PDFParser:
    def __init__(self, file):
        self.file = file
        self.pdf = pdfplumber.open(file)
        
    def extract_text(self) -> str:
        """Extract all text from PDF"""
        full_text = ""
        for page in self.pdf.pages:
            full_text += page.extract_text() + "\n"
        return full_text
    
    def find_financial_tables(self) -> Dict:
        """Extract financial tables from PDF"""
        financial_data = {
            "Standalone_financial_results_for_all_months": {},
            "Statement_Consolidated_finanacial_results_for_all_months": {}
        }
        
        # Extract all tables
        for i, page in enumerate(self.pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                if len(table) > 3:  # Basic check for data tables
                    df = pd.DataFrame(table[1:], columns=table[0])
                    period = self._detect_period(page.extract_text())
                    
                    # Check if table contains financial data
                    if "Revenue" in str(df.columns):
                        if "Consolidated" in page.extract_text():
                            key = "Statement_Consolidated_finanacial_results_for_all_months"
                        else:
                            key = "Standalone_financial_results_for_all_months"
                        
                        financial_data[key][period] = df.to_dict('records')
        
        return financial_data
    
    def _detect_period(self, text: str) -> str:
        """Detect reporting period from text"""
        quarter_match = re.search(r"Quarter (ended|ending) (\d{1,2} \w+ \d{4})", text)
        year_match = re.search(r"Year (ended|ending) (\d{1,2} \w+ \d{4})", text)
        
        if quarter_match:
            return f"Quarter ended {quarter_match.group(2)}"
        elif year_match:
            return f"Year ended {year_match.group(2)}"
        return "Unknown Period"
    
    def close(self):
        """Close the PDF file"""
        self.pdf.close()