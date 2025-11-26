import streamlit as st

# Dummy functions to satisfy the import requirements from the login page
def show_evidence_library(): pass
def show_search_cases(): pass
def show_legal_reference(): pass
def show_new_case_selector(): pass
def show_cdr_analysis(a, b, c, d): pass
def show_ipdr_analysis(a, b, c, d): pass
def show_firewall_analysis(a, b, c, d): pass
def show_correlation_analysis(a, b, c, d): pass

# --- CSS and Core Function ---

def dashboard_css():
    st.markdown("""
    <style>
    /* Global Background and Padding */
    .main .block-container {
        padding-top: 80px !important; 
        padding-left: 40px;
        padding-right: 40px;
        padding-bottom: 40px;
        max-width: 100% !important;
    }
    body, [data-testid="stAppViewContainer"] {
        background: #001928 !important; /* Dark Background */
    }

    /* Fixed Header Container */
    #fixed-header-container {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 60px;
        z-index: 10;
        background: #15425b; /* Requested Title Bar Color */
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        padding: 0 20px; /* Add padding inside the bar */
    }
    
    /* Layout for columns inside the header */
    #header-content-wrapper {
        display: flex;
        align-items: center;
        height: 60px;
    }

    /* Dashboard Title Styling (centered text) */
    .dashboard-title-text {
        font-size: 2rem;
        font-weight: 700;
        color: #fff;
        text-align: center;
        width: 100%; /* Take full width of its column */
    }

    /* User/Logout Action Styling (on the right) */
    .user-actions {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-box {
        display: flex;
        align-items: center;
        color: #fff;
        font-size: 1rem;
        font-weight: 500;
        gap: 6px;
    }
    .user-avatar {
        width: 30px;
        height: 30px;
        background: #367588; 
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
        color: #fff;
    }
    
    /* Style for the Logout Button in the header */
    [data-testid="stButton"][key="header_logout"] button {
        background-color: #367588; 
        color: white;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        width: auto;
        padding: 5px 10px;
        height: 30px;
        margin: 0;
        transition: background-color 0.2s;
        border: none;
    }
    [data-testid="stButton"][key="header_logout"] button:hover {
        background-color: #e57373; /* Light red hover for danger/logout */
    }
    
    /* Remove Sidebar */
    [data-testid="stSidebar"], [data-testid="stSidebarContent"] { display: none !important; }

    /* Remove extra margin/padding from inner markdown elements */
    #fixed-header-container p {
        margin: 0;
        padding: 0;
    }
    </style>
    """, unsafe_allow_html=True)

def dashboard(username):
    st.set_page_config(page_title="Anomalyze Dashboard", layout="wide")
    dashboard_css()

    # --- Session State Initialization (Required for login page logic) ---
    if "page" not in st.session_state:
        st.session_state.page = "main"
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # --- Fixed Header (Title Bar with User/Logout) ---
    st.markdown('<div id="fixed-header-container">', unsafe_allow_html=True)
    st.markdown('<div id="header-content-wrapper">', unsafe_allow_html=True)
    
    # Define columns: User Actions (3 units) | Title (6 units) | Logout/User Info (3 units)
    # Note: Using Streamlit columns *inside* a custom fixed div is tricky, but we use it for placement.
    left_spacer, title_col, actions_col = st.columns([1, 4, 3])
    
    # 1. User Actions (Left side - icon + username)
    with left_spacer:
        st.markdown(f'''
            <div class="user-actions">
                <div class="user-box">
                    <div class="user-avatar">👤</div>
                    {username.upper()}
                </div>
            </div>
        ''', unsafe_allow_html=True)

    # 2. Title (Center)
    with title_col:
        st.markdown('<div class="dashboard-title-text">Dashboard</div>', unsafe_allow_html=True)
        
    # 3. Logout (Right side - button)
    with actions_col:
        st.markdown('<div style="display: flex; justify-content: flex-end;">', unsafe_allow_html=True)
        if st.button("Logout", key="header_logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.page = "main"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True) # Close header-content-wrapper
    st.markdown('</div>', unsafe_allow_html=True) # Close fixed-header-container

    # Main content area (intentionally blank)
    st.markdown('<div style="height: 500px;"></div>', unsafe_allow_html=True)
