import streamlit as st
import pandas as pd
from fpdf import FPDF
import tempfile
import os
import logging
from datetime import datetime

# ==========================================
# 1. CONFIGURATION & CONSTANTS
# ==========================================

REQUIRED_COLUMNS = ['calling_number', 'called_number', 'start_time', 'call_direction']

CDR_COLUMN_MAP = {
    "calling_number": ["calling_number", "caller", "source_number", "a_party"],
    "called_number": ["called_number", "callee", "dest_number", "b_party"],
    "start_time": ["start_time", "timestamp", "date_time", "call_time"],
    "call_direction": ["call_direction", "direction", "type", "call_type"]
}

# ==========================================
# 2. DATA NORMALIZATION & VALIDATION
# ==========================================

def normalize_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """Standardizes column names based on a mapping dictionary."""
    col_rename = {}
    df_cols = {col.lower().replace(" ", "").replace("_", ""): col for col in df.columns}
    for std_col, variants in column_map.items():
        for variant in variants:
            key = variant.lower().replace(" ", "").replace("_", "")
            if key in df_cols:
                col_rename[df_cols[key]] = std_col
                break
    return df.rename(columns=col_rename)

def validate_input(df: pd.DataFrame) -> pd.DataFrame:
    """Checks if the dataframe contains necessary columns."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        st.error(f"❌ Missing required columns: {missing}")
        st.stop()
    return df

def parse_cdr(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare CDR data for analysis."""
    df = normalize_columns(df, CDR_COLUMN_MAP)
    if 'start_time' in df.columns:
        df['start_time'] = pd.to_datetime(df['start_time'], errors='coerce')
    return df

# ==========================================
# 3. ANALYSIS LOGIC (CORE ENGINE)
# ==========================================

def analyze_logic(df: pd.DataFrame, intl_threshold: int, spike_threshold: int):
    """
    Core Logic: Separated from UI for easier testing and modularity.
    Returns: Tuple(intl_suspects, spike_suspects)
    """
    # Filter for outgoing calls (Mobile Originating)
    outgoing_df = df[df['call_direction'].astype(str).str.upper().isin(['MO', 'OUTGOING', '1'])].copy()
    
    if outgoing_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Logic A: International Calls (Not starting with 91)
    # Note: '91' is the assumed home country code.
    intl_calls = outgoing_df[~outgoing_df['called_number'].astype(str).str.startswith('91')]
    intl_counts = intl_calls.groupby('calling_number').size().reset_index(name='international_call_count')
    intl_suspects = intl_counts[intl_counts['international_call_count'] > intl_threshold]

    # Logic B: Call Spikes (Hourly)
    outgoing_df['hour_window'] = outgoing_df['start_time'].dt.floor('h')
    call_spikes = outgoing_df.groupby(['calling_number', 'hour_window']).size().reset_index(name='calls_in_hour')
    spike_suspects = call_spikes[call_spikes['calls_in_hour'] > spike_threshold]
    
    return intl_suspects, spike_suspects

# ==========================================
# 4. REPORT GENERATION (PDF)
# ==========================================

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'CDR Analysis Report: Outgoing Anomalies', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(file_name, intl_suspects, spike_suspects, settings):
    """
    Generates a structured PDF report with tables and analysis summary.
    """
    pdf = PDFReport()
    pdf.add_page()
    
    # -- Introduction & Meta Data --
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Source File: {file_name}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Executive Summary", ln=True)
    pdf.set_font("Arial", size=10)
    summary_text = (
        f"This report analyzes outgoing call patterns to detect suspicious activity. "
        f"The analysis applied a threshold of >{settings['intl']} for international calls "
        f"and >{settings['spike']} calls per hour for spike detection."
    )
    pdf.multi_cell(0, 5, summary_text)
    pdf.ln(10)

    # -- Part 1 Table --
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Excessive International Calls", ln=True)
    
    if intl_suspects.empty:
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "No anomalies detected based on current thresholds.", ln=True)
    else:
        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(95, 10, "Calling Number", 1, 0, 'C', 1)
        pdf.cell(95, 10, "Total Int'l Calls", 1, 1, 'C', 1)
        
        # Table Rows
        pdf.set_font("Arial", size=10)
        for _, row in intl_suspects.iterrows():
            pdf.cell(95, 10, str(row['calling_number']), 1)
            pdf.cell(95, 10, str(row['international_call_count']), 1, 1, 'C')
            
    pdf.ln(10)

    # -- Part 2 Table --
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "3. Hourly Call Spikes", ln=True)
    
    if spike_suspects.empty:
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(0, 10, "No sudden spikes detected.", ln=True)
    else:
        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(70, 10, "Calling Number", 1, 0, 'C', 1)
        pdf.cell(70, 10, "Time Window", 1, 0, 'C', 1)
        pdf.cell(50, 10, "Call Volume", 1, 1, 'C', 1)
        
        # Table Rows
        pdf.set_font("Arial", size=10)
        for _, row in spike_suspects.iterrows():
            pdf.cell(70, 10, str(row['calling_number']), 1)
            pdf.cell(70, 10, str(row['hour_window']), 1)
            pdf.cell(50, 10, str(row['calls_in_hour']), 1, 1, 'C')

    # Output
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(tmp_file.name)
    return tmp_file.name

# ==========================================
# 5. STREAMLIT INTERFACE (MAIN EXECUTION)
# ==========================================

def run_analysis():
    st.title("📞 Outgoing Call Analysis")
    st.markdown("---")

    # Initialize Session State
    if 'uploaded_file' not in st.session_state: st.session_state.uploaded_file = None
    if 'intl_suspects' not in st.session_state: st.session_state.intl_suspects = None
    if 'spike_suspects' not in st.session_state: st.session_state.spike_suspects = None
    if 'pdf_path' not in st.session_state: st.session_state.pdf_path = None

    # -- File Upload --
    uploaded_file = st.file_uploader("Upload CDR File (CSV/Excel)", type=["csv", "xlsx"], key='file_uploader')

    # -- Threshold Settings (Displayed only after/with file upload option) --
    with st.expander("⚙️ Analysis Settings (Thresholds)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            intl_thresh = st.number_input("Max Allowed Int'l Calls", min_value=1, value=5, step=1)
        with col2:
            spike_thresh = st.number_input("Max Allowed Hourly Calls", min_value=5, value=10, step=5)

    # -- Execution Logic --
    if uploaded_file is not None:
        # Trigger analysis if file changes OR if thresholds change
        # (Note: In Streamlit, a button is often safer to prevent constant re-running, 
        # but here we follow the existing pattern of auto-running on interaction)
        st.session_state.uploaded_file = uploaded_file
        
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            df = parse_cdr(df)
            df = validate_input(df)
            
            # Run Analysis
            intl_suspects, spike_suspects = analyze_logic(df, intl_thresh, spike_thresh)
            
            # Store Results
            st.session_state.intl_suspects = intl_suspects
            st.session_state.spike_suspects = spike_suspects
            st.session_state.pdf_path = generate_pdf_report(
                uploaded_file.name, intl_suspects, spike_suspects, 
                {"intl": intl_thresh, "spike": spike_thresh}
            )
            
            st.success("Analysis Completed Successfully")

        except Exception as e:
            st.error(f"Error processing file: {e}")
            logging.error(f"Analysis failed: {e}")

    # -- Display Results --
    if st.session_state.uploaded_file is not None and st.session_state.intl_suspects is not None:
        st.write("----")
        
        # Part 1: International
        st.subheader("🌍 Excessive International Calls")
        if st.session_state.intl_suspects.empty:
            st.info("No suspects found matching criteria.")
        else:
            st.dataframe(st.session_state.intl_suspects, use_container_width=True)

        # Part 2: Spikes
        st.subheader("📈 Hourly Call Spikes")
        if st.session_state.spike_suspects.empty:
            st.info("No call spikes detected.")
        else:
            # Format datetime for cleaner display
            display_spikes = st.session_state.spike_suspects.copy()
            if not display_spikes.empty:
                display_spikes['hour_window'] = display_spikes['hour_window'].dt.strftime('%Y-%m-%d %H:00')
            st.dataframe(display_spikes, use_container_width=True)

        # PDF Download
        if st.session_state.pdf_path and os.path.exists(st.session_state.pdf_path):
            with open(st.session_state.pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Detailed PDF Report",
                    data=f,
                    file_name="CDR_Outgoing_Analysis_Report.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    run_analysis()
