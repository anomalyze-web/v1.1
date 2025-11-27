import streamlit as st
import base64
from streamlit_extras.stylable_container import stylable_container

# Placeholder functions for analysis modules (simulate external imports)
# In a real application, you would ensure 'CDR_analysis.py', etc., contain these functions.
def show_cdr_analysis(case_number, investigator_name, case_name, remarks):
    st.header("CDR Analysis Page 📞")
    st.write(f"**Case No:** {case_number}, **Case Name:** {case_name}, **Investigator:** {investigator_name}")
    st.markdown("---")
    if st.button("⬅ Back to New Case Selection", key="back_from_cdr_analysis"):
        st.session_state.page = "new_case_selector"
        st.rerun()

def show_ipdr_analysis(case_number, investigator_name, case_name, remarks):
    st.header("IPDR Analysis Page 🌐")
    st.write(f"**Case No:** {case_number}, **Case Name:** {case_name}, **Investigator:** {investigator_name}")
    st.markdown("---")
    if st.button("⬅ Back to New Case Selection", key="back_from_ipdr_analysis"):
        st.session_state.page = "new_case_selector"
        st.rerun()

def show_firewall_analysis(case_number, investigator_name, case_name, remarks):
    st.header("FIREWALL Analysis Page 🔥")
    st.write(f"**Case No:** {case_number}, **Case Name:** {case_name}, **Investigator:** {investigator_name}")
    st.markdown("---")
    if st.button("⬅ Back to New Case Selection", key="back_from_firewall_analysis"):
        st.session_state.page = "new_case_selector"
        st.rerun()

def show_correlation_analysis(case_number, investigator_name, case_name, remarks):
    st.header("CO-RELATION Analysis Page 🔗")
    st.write(f"**Case No:** {case_number}, **Case Name:** {case_name}, **Investigator:** {investigator_name}")
    st.markdown("---")
    if st.button("⬅ Back to New Case Selection", key="back_from_correlation_analysis"):
        st.session_state.page = "new_case_selector"
        st.rerun()

# --- Helper Functions (Page Views) ---

def show_evidence_library():
    st.title("Evidence Library 🗃️")
    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "main"
        st.rerun()

    st.text_input("Search Evidence Library", placeholder="Enter keywords, hash values, or file names...")
    st.markdown('<div style="margin-top: 50px; padding: 30px; border: 1px dashed #555; border-radius: 10px; color: #aaa; text-align: center;">\
    <h3>No Evidence Uploaded Yet</h3>\
    <p>Start a new case to upload and categorize digital evidence.</p>\
    </div>', unsafe_allow_html=True)

def show_search_cases():
    st.title("Search Historical Cases 🔎")
    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "main"
        st.rerun()

    st.text_input("Search Cases", placeholder="Enter case number, investigator name, or keywords...")
    st.markdown('<div style="margin-top: 50px; padding: 30px; border: 1px dashed #555; border-radius: 10px; color: #aaa; text-align: center;">\
    <h3>No Cases Archived</h3>\
    <p>Completed case analyses will appear here for future reference and searching.</p>\
    </div>', unsafe_allow_html=True)

def show_legal_reference():
    st.title("Legal Reference and Standards ⚖️")
    st.markdown("---")
    if st.button("⬅ Back to Dashboard"):
        st.session_state.page = "main"
        st.rerun()

    st.markdown('<div style="padding: 30px; border: 1px dashed #555; border-radius: 10px; color: #aaa;">\
    <p>This section is reserved for relevant legal statutes, compliance documentation, and digital forensics standards.</p>\
    <p>Content to be integrated...</p>\
    </div>', unsafe_allow_html=True)

def show_new_case_selector():
    st.markdown(f"### Select Data Type for New Case: 💾")

    if st.button("⬅ Back to Dashboard", key="back_to_dash_new_case_sel"):
        st.session_state.page = "main"
        st.rerun()
    
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)

    selector_button_style = """
    button {
    background-color: #1c4868 !important;
    color: #fff !important;
    border: 2px solid #61a3cd !important;
    border-radius: 12px;
    height: 60px;
    font-size: 1.1rem;
    width: 100%;
    margin-bottom: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.2s, border-color 0.2s;
    }
    button:hover {
    background-color: #367588 !important;
    border: 2px solid #fff !important;
    }
    """

    with col1:
        with stylable_container("cdr_button", css_styles=selector_button_style):
            if st.button("CDR Analysis", key="select_cdr"):
                st.session_state.page = "cdr"
                st.session_state.form_submitted = False
                st.rerun()

    with col2:
        with stylable_container("ipdr_button", css_styles=selector_button_style):
            if st.button("IPDR Analysis", key="select_ipdr"):
                st.session_state.page = "ipdr"
                st.session_state.form_submitted = False
                st.rerun()

    with col3:
        with stylable_container("firewall_button", css_styles=selector_button_style):
            if st.button("Firewall Logs", key="select_firewall"):
                st.session_state.page = "firewall"
                st.session_state.form_submitted = False
                st.rerun()

    with col4:
        with stylable_container("correlation_button", css_styles=selector_button_style):
            if st.button("Correlation", key="select_correlation"):
                st.session_state.page = "correlation"
                st.session_state.form_submitted = False
                st.rerun()

# --- CSS Injection ---

def inject_css():
    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">', unsafe_allow_html=True)
    
    css_code_compressed = """
<style>
/* Aggressive reset for browser/Streamlit default margins */
html, body { margin: 0 !important; padding: 0 !important; }
/* IMPORTANT: We are explicitly unsetting Streamlit's default padding */
[data-testid="stAppViewContainer"]{margin-top:0!important;padding-top:0!important;}
body,[data-testid="stAppViewContainer"]{background:#001928!important;}
[data-testid="stSidebar"],[data-testid="stSidebarContent"]{display:none!important;}

/* HEADER HEIGHT 120px, NO USER/LOGOUT BUTTONS */
#fixed-header-container{
    position:fixed;
    left:0;
    top:0;
    width:100%;
    z-index:10; /* BASE Z-INDEX for the background */
    padding:0 40px;
    background:rgba(21, 66, 91, 0.95); 
    box-shadow:0 4px 12px rgba(0,0,0,0.3);
    height:120px; /* RESTORED 120px HEIGHT */
    display:flex;
    flex-direction:column;
    justify-content:flex-start; 
}

/* Top row (Title Only) - Centered in top half of 120px header */
.fixed-header-content{
    width:100%;
    display:flex;
    justify-content:center; /* Center title horizontally */
    align-items:center; 
    z-index: 100; /* HIGH Z-INDEX to show above header background */
    position: absolute;
    top: 0px; /* PINNED to the top of the container */
    padding-top: 15px; /* Padded for vertical center in the top half */
    padding-bottom: 5px;
}

/* Removed User Box and Logout Link/Button CSS */
.user-box, .user-avatar, .logout-link, [data-testid="stButton"][key="header_logout"] {
    display: none !important; 
}

/* Navigation Buttons (Second Row, starts at 60px down) */
.fixed-nav-row{
    width:100%;
    display:flex;
    align-items:center;
    height: 60px;
    padding-bottom: 5px;
    padding-top: 5px; 
    z-index: 50; 
    background: #001928; /* Same background as main body */
    position: absolute;
    top: 60px; /* Starts exactly where the top 60px section ends */
}

.dashboard-title{
    font-size:1.8rem;
    font-weight:700;
    color:#fff;
    text-align:center;
    margin:0;
    line-height:1.2; 
    padding-top: 0px; 
}

.main-nav-button button{
    background-color:#1c4868!important;
    color:white!important;
    border:2px solid #61a3cd!important;
    border-radius:8px!important;
    font-size:1.05rem!important;
    font-weight:600!important;
    width:100%; 
    height:40px;
    margin:0;
    transition:all 0.2s;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
.main-nav-button button:hover{background-color:#367588!important;border-color:#fff!important;}

/* Adjust content padding to accommodate the 120px header + small top margin */
.main .block-container{padding-top:130px!important;padding-left:40px;padding-right:40px;padding-bottom:40px;max-width:100%!important;}
.section-header{font-size:1.8rem;font-weight:700;color:#3a7ba4!important;margin-top:30px;margin-bottom:15px;border-bottom:2px solid #367588;padding-bottom:5px;}
.placeholder-box{background:#15425b;color:#99aab5;padding:20px;border-radius:12px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.15);}
.placeholder-box h4{margin-top:0;color:#fff;}
</style>
"""
    st.markdown(css_code_compressed, unsafe_allow_html=True)

# --- Core Function ---

def dashboard(username):
    st.set_page_config(page_title="Anomalyze Dashboard", layout="wide")
    
    # 1. CSS INJECTION BLOCK
    inject_css()
    
    # 2. Session State Initialization
    if "page" not in st.session_state:
        st.session_state.page = "main"
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    # Ensure login state is initialized for the logic to work correctly
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
    if "current_user" not in st.session_state:
        st.session_state.current_user = username
    
    # 3. FIXED HEADER HTML STRUCTURE (120px tall)
    st.markdown('<div id="fixed-header-container">', unsafe_allow_html=True)

    # --- TOP ROW: Title Only ---
    st.markdown('<div class="fixed-header-content">', unsafe_allow_html=True)
    
    # Use columns to position the title
    empty_col_left, title_col, empty_col_right = st.columns([2, 6, 2])

    with title_col:
        # Title is centered by the CSS in fixed-header-content
        st.markdown('<div class="dashboard-title">Anomalyze Dashboard</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Closes fixed-header-content (Top Row)
    
    # --- BOTTOM ROW: Navigation Buttons ---
    st.markdown('<div class="fixed-nav-row">', unsafe_allow_html=True)
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

    def nav_button(label, key, target_page, col):
        with col:
            with stylable_container(f"nav_button_{key}", css_styles=".main-nav-button"):
                if st.button(label, key=key, help=f"Go to {label}"):
                    st.session_state.page = target_page
                    st.rerun()

    nav_button("New Case", "nav_new_case", "new_case_selector", nav_col1) 
    nav_button("Evidence Library", "nav_evidence", "evidence_library", nav_col2)
    nav_button("Search Cases", "nav_search", "search_cases", nav_col3)
    nav_button("Legal Reference", "nav_legal", "legal_reference", nav_col4)

    st.markdown('</div>', unsafe_allow_html=True) # Closes fixed-nav-row (Bottom Row)
    
    st.markdown('</div>', unsafe_allow_html=True) # Closes fixed-header-container

    # 4. MAIN CONTENT AREA
    st.markdown('<div class="dashboard-main">', unsafe_allow_html=True)

    if st.session_state.page == "main":
        
        st.markdown('<h2 class="section-header">Bookmarked Cases ⭐</h2>', unsafe_allow_html=True)
        st.markdown('<div class="placeholder-box"><h4>No bookmarked cases available.</h4><p>Use the bookmark feature on case analysis pages to quickly access important investigations.</p></div>', unsafe_allow_html=True)

        st.markdown('<h2 class="section-header">Recent Activity 🕓</h2>', unsafe_allow_html=True)
        st.markdown('<div class="placeholder-box"><h4>No recent cases analyzed.</h4><p>Start a new case using the "New Case" button above to begin your analysis.</p></div>', unsafe_allow_html=True)

    elif st.session_state.page == "new_case_selector":
        show_new_case_selector() 

    elif st.session_state.page == "evidence_library":
        show_evidence_library()
    elif st.session_state.page == "search_cases":
        show_search_cases()
    elif st.session_state.page == "legal_reference":
        show_legal_reference()

    # --- Analysis Case Submission Form ---
    elif st.session_state.page in ["cdr", "ipdr", "firewall", "correlation"]:
        st.markdown(f"### Uploading **{st.session_state.page.upper()}** Case 📁")

        # The Back button needs to check if the user is coming from the form or analysis page
        if st.button("⬅ Back to New Case Selection"):
            st.session_state.page = "new_case_selector"
            st.session_state.form_submitted = False
            st.rerun()

        with st.form(f"{st.session_state.page}_form"):
            # Preserve state if the user navigates back to the form
            case_number = st.text_input("Case Number", value=st.session_state.get('case_number', ''))
            investigator_name = st.text_input("Investigator Name", value=st.session_state.get('investigator_name', ''))
            case_name = st.text_input("Case Name", value=st.session_state.get('case_name', ''))
            remarks = st.text_area("Remarks", value=st.session_state.get('remarks', ''))
            submit = st.form_submit_button("Submit Case Data")
            
            if submit:
                # Store data in session state upon submission
                st.session_state.case_number = case_number
                st.session_state.investigator_name = investigator_name
                st.session_state.case_name = case_name
                st.session_state.remarks = remarks
                st.session_state.form_submitted = True
                
                st.success(
                    f"{st.session_state.page.upper()} Case '{case_name}' (Case No: {case_number}) uploaded by {investigator_name}."
                )

        # Analysis button only appears if the form was submitted successfully
        if st.session_state.form_submitted and st.session_state.get('case_name'):
            analysis_labels = {
                "cdr": "Start CDR Analysis",
                "ipdr": "Start IPDR Analysis",
                "firewall": "Start FIREWALL Analysis",
                "correlation": "Start CO-RELATION Analysis"
            }
            label = analysis_labels.get(st.session_state.page, "Start Analysis")
            if st.button(label):
                # Transition to the specific analysis page
                st.session_state.page = f"{st.session_state.page}_analysis"
                st.session_state.form_submitted = False
                st.rerun()

    # --- Analysis Page Router ---
    elif st.session_state.page == "cdr_analysis":
        show_cdr_analysis(
            st.session_state.case_number,
            st.session_state.investigator_name,
            st.session_state.case_name,
            st.session_state.remarks
        )
    elif st.session_state.page == "ipdr_analysis":
        show_ipdr_analysis(
            st.session_state.case_number,
            st.session_state.investigator_name,
            st.session_state.case_name,
            st.session_state.remarks
        )
    elif st.session_state.page == "firewall_analysis":
        show_firewall_analysis(
            st.session_state.case_number,
            st.session_state.investigator_name,
            st.session_state.case_name,
            st.session_state.remarks
        )
    elif st.session_state.page == "correlation_analysis":
        show_correlation_analysis(
            st.session_state.case_number,
            st.session_state.investigator_name,
            st.session_state.case_name,
            st.session_state.remarks
        )

    st.markdown('</div>', unsafe_allow_html=True)

# Example usage (assuming this is part of a larger app logic)
# if __name__ == "__main__":
#     if "logged_in" not in st.session_state or not st.session_state.logged_in:
#         # ... login page logic ...
#         pass # Assume a login function handles this
#     else:
#         dashboard(st.session_state.current_user)

# To run this in a simple environment for testing:
# dashboard("TEST_USER")
