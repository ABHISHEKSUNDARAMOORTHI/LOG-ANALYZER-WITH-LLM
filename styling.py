import streamlit as st

def apply_custom_styles():
    """
    Applies comprehensive custom CSS styles to the Streamlit application
    for a modern, professional, dark-themed look tailored for data engineering
    and analysis tools.
    """
    st.markdown("""
    <style>
        /* Import Inter font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
        /* Import Font Awesome for Icons (v5.15.4 is stable and widely used) */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

        /* --- Color Variables for a Professional Dark Palette --- */
        :root {
            --bg-primary: #1A1A2E; /* Deep Indigo / Very Dark Blue */
            --bg-secondary: #1E283A; /* Slightly lighter dark blue for cards/containers */
            --bg-tertiary: #27374D; /* Even lighter for hover/active states or subtle distinction */

            --text-light: #E0E0E0; /* Off-white for main text */
            --text-medium: #A0A0A0; /* Medium gray for secondary text/labels */
            --text-dark: #606060; /* Darker gray for subtle elements */

            --accent-blue-light: #4A90E2; /* Bright, professional blue for highlights */
            --accent-blue-dark: #2F6DA4; /* Deeper blue for accents */
            --accent-green: #5CB85C; /* Success/positive green */
            --accent-red: #D9534F; /* Danger/error red */
            --accent-orange: #F0AD4E; /* Warning/attention orange */

            --border-color: #3B4A60; /* Darker, subtle border */
            --shadow-light: rgba(0, 0, 0, 0.3);
            --shadow-medium: rgba(0, 0, 0, 0.5);

            --border-radius-lg: 12px;
            --border-radius-md: 8px;
            --border-radius-sm: 4px;

            --spacing-md: 1.5rem; /* Medium spacing for gaps */
            --spacing-lg: 2.5rem; /* Larger spacing for sections */
        }

        /* --- General Body & Streamlit App Overrides --- */
        html, body {
            font-family: 'Inter', sans-serif;
            line-height: 1.7; /* Improved readability for long text */
            margin: 0;
            padding: 0;
            color: var(--text-light);
            background-color: var(--bg-primary);
        }

        .stApp {
            background-color: var(--bg-primary);
            color: var(--text-light);
        }

        /* Global app padding adjustment (to avoid content sticking to edges) */
        .stApp > header {
            background-color: transparent; /* Makes Streamlit header transparent */
        }
        .css-1dp5vir { /* Targets the main content wrapper padding - might need adjustment for newer Streamlit versions */
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Custom Scrollbar Styling */
        ::-webkit-scrollbar {
            width: 12px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
            border-radius: var(--border-radius-lg);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--accent-blue-dark);
            border-radius: var(--border-radius-lg);
            border: 3px solid var(--bg-secondary); /* Creates a border effect */
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-blue-light);
        }

        /* --- Main Content Container --- */
        .main .block-container {
            max-width: 1300px; /* Slightly wider for data-heavy apps */
            padding: var(--spacing-lg) 3.5rem; /* Generous padding */
            background-color: var(--bg-secondary);
            border-radius: var(--border-radius-lg);
            box-shadow: 0 15px 35px var(--shadow-medium); /* More prominent shadow */
            margin: var(--spacing-lg) auto;
            border: 1px solid var(--border-color);
        }

        /* --- Section Headers --- */
        .stMarkdown h1, .stMarkdown h2 {
            font-size: 2.5rem; /* Larger for impact */
            color: var(--accent-blue-light);
            margin-top: var(--spacing-lg);
            margin-bottom: var(--spacing-md);
            border-bottom: 2px solid var(--accent-blue-dark);
            padding-bottom: 0.8rem;
            font-weight: 700;
            position: relative;
            letter-spacing: -0.02em; /* Tighter for modern look */
        }
        /* Animated underline for main headers */
        .stMarkdown h1::after, .stMarkdown h2::after {
            content: '';
            display: block;
            width: 80px; /* Longer line */
            height: 6px; /* Thicker line */
            background: linear-gradient(90deg, var(--accent-blue-light) 0%, var(--accent-blue-dark) 100%);
            position: absolute;
            bottom: -3px; /* Slightly below the border */
            left: 0;
            border-radius: var(--border-radius-sm);
        }

        .stMarkdown h3 {
            font-size: 2rem;
            color: var(--text-light);
            margin-top: 2rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            font-weight: 600;
            letter-spacing: -0.01em;
        }
        .stMarkdown h4 {
            font-size: 1.5rem;
            color: var(--text-light);
            margin-top: var(--spacing-md);
            margin-bottom: 0.8rem;
            font-weight: 600;
        }

        /* --- Textareas and Input Fields --- */
        textarea, .stTextInput > div > div > input, .stCodeEditor, .stSelectbox > div > div, .stFileUploader > div > div {
            background-color: var(--bg-primary); /* Darker background for inputs */
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            color: var(--text-light);
            font-size: 1.05rem;
            padding: 0.8rem 1.2rem; /* Slightly more padding */
            box-shadow: inset 0 2px 8px var(--shadow-light); /* Deeper inset shadow */
            transition: all 0.3s ease-in-out;
            outline: none; /* Remove default outline */
        }
        textarea:focus, .stTextInput > div > div > input:focus, .stCodeEditor:focus-within, .stSelectbox > div > div:focus-within, .stFileUploader > div > div:focus-within {
            border-color: var(--accent-blue-light);
            box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.3), inset 0 2px 8px var(--shadow-light); /* Brighter, wider focus shadow */
        }
        textarea::placeholder {
            color: var(--text-medium);
            opacity: 0.7;
        }
        /* Style for file uploader drag area */
        .stFileUploader > label > div > div {
            border: 2px dashed var(--border-color); /* Dashed border for drop zone */
            border-radius: var(--border-radius-md);
            background-color: var(--bg-primary);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        .stFileUploader > label > div > div:hover {
            border-color: var(--accent-blue-light);
            background-color: var(--bg-tertiary);
        }
        /* File uploader "Browse files" button styling */
        .stFileUploader button {
            background-color: var(--accent-blue-dark) !important;
            color: white !important;
            border-radius: var(--border-radius-md) !important;
            padding: 0.7rem 1.5rem !important;
            font-size: 1em !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 4px 10px var(--shadow-light) !important;
            transition: all 0.3s ease !important;
        }
        .stFileUploader button:hover {
            background-color: var(--accent-blue-light) !important;
            transform: translateY(-2px);
        }


        /* --- Buttons --- */
        .stButton > button {
            padding: 1rem 2.2rem;
            border: none;
            border-radius: var(--border-radius-md);
            font-size: 1.15rem; /* Slightly larger text */
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
            margin-top: var(--spacing-md);
            box-shadow: 0 8px 20px var(--shadow-medium);
            letter-spacing: 0.04em;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem; /* Space between text and icon */
        }
        .stButton > button:hover {
            transform: translateY(-5px); /* More pronounced lift */
            box-shadow: 0 12px 25px var(--shadow-medium);
        }
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 4px 10px var(--shadow-light);
        }

        /* Primary button with gradient */
        .stButton > button[kind="primary"] {
            background: linear-gradient(45deg, var(--accent-blue-dark), var(--accent-blue-light));
            color: #ffffff;
            border: 1px solid var(--accent-blue-light);
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(45deg, #3182ce, var(--accent-blue-light));
        }

        /* Secondary button styling (e.g., for download) */
        .stButton > button[kind="secondary"] {
            background-color: var(--bg-tertiary);
            color: var(--accent-blue-light);
            border: 2px solid var(--accent-blue-dark);
            box-shadow: none;
        }
        .stButton > button[kind="secondary"]:hover {
            background-color: var(--accent-blue-dark);
            color: #ffffff;
            border-color: var(--accent-blue-dark);
            box-shadow: 0 4px 10px var(--shadow-light);
        }

        /* --- Markdown Output Styling (for AI explanations) --- */
        .stMarkdown p, .stMarkdown ul, .stMarkdown ol, .stMarkdown li {
            color: var(--text-light);
            margin-bottom: 1.2rem;
            font-size: 1.1rem;
            line-height: 1.8;
        }
        .stMarkdown ul {
            list-style-type: '👉 '; /* Custom bullet point */
            margin-left: 20px;
            padding-left: 10px;
        }
        .stMarkdown ol {
            margin-left: 20px;
            padding-left: 10px;
        }
        .stMarkdown strong {
            color: var(--accent-blue-light);
            font-weight: 700;
        }
        .stMarkdown em {
            color: var(--text-medium);
            font-style: italic;
        }
        .stMarkdown code {
            background-color: var(--bg-tertiary); /* Inline code background */
            padding: 0.3em 0.5em;
            border-radius: var(--border-radius-sm);
            font-family: 'Fira Code', 'Cascadia Code', monospace; /* Professional coding fonts */
            font-size: 0.95em;
            color: #FFD700; /* Gold-like color for inline code */
        }
        .stMarkdown pre code {
            background-color: #0F121C; /* Even darker for code blocks */
            border: 1px solid var(--border-color);
            border-radius: var(--border-radius-md);
            padding: 1.8em; /* More padding */
            overflow-x: auto;
            margin-bottom: var(--spacing-lg);
            display: block;
            box-shadow: inset 0 0 15px var(--shadow-light); /* Deeper inset shadow */
            color: #E0E0E0; /* Lighter text in code block */
            font-size: 0.95em;
            line-height: 1.6;
        }

        /* --- Alerts and Info Boxes --- */
        .stAlert {
            border-radius: var(--border-radius-md);
            margin-top: var(--spacing-md);
            padding: 1.5rem 2rem; /* More padding */
            font-weight: 600;
            font-size: 1.05rem;
            box-shadow: 0 4px 15px var(--shadow-light);
            display: flex;
            align-items: center;
        }
        .stAlert div[data-testid="stMarkdownContainer"] {
            margin-left: 15px; /* Space for icon if Streamlit adds one */
        }
        /* Specific alert types (classes are Streamlit internal and may change) */
        /* You might need to inspect your deployed app to confirm these class names */
        .stAlert.st-emotion-cache-1fcpknu { /* Success */
            border-left: 8px solid var(--accent-green) !important;
            background-color: rgba(92, 184, 92, 0.15) !important; /* Slightly more opaque */
            color: var(--accent-green) !important;
        }
        .stAlert.st-emotion-cache-1wdd6qg { /* Warning */
            border-left: 8px solid var(--accent-orange) !important;
            background-color: rgba(240, 173, 78, 0.15) !important;
            color: var(--accent-orange) !important;
        }
        .stAlert.st-emotion-cache-1215i5j { /* Error */
            border-left: 8px solid var(--accent-red) !important;
            background-color: rgba(217, 83, 79, 0.15) !important;
            color: var(--accent-red) !important;
        }
        .stAlert.st-emotion-cache-19t5331 { /* Info (Streamlit's info component) */
             border-left: 8px solid var(--accent-blue-light) !important;
             background-color: rgba(74, 144, 226, 0.15) !important;
             color: var(--accent-blue-light) !important;
        }

        /* --- Expander Styling --- */
        .streamlit-expanderHeader {
            background-color: var(--bg-tertiary);
            color: var(--text-light);
            font-weight: 600;
            border-radius: var(--border-radius-md);
            padding: 1.2rem 1.8rem;
            margin-bottom: 1rem;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 5px 12px var(--shadow-light);
            font-size: 1.1rem;
            display: flex;
            align-items: center;
        }
        .streamlit-expanderHeader:hover {
            background-color: #37475E; /* Slightly lighter on hover */
            box-shadow: 0 8px 18px var(--shadow-medium);
        }
        .streamlit-expanderContent {
            background-color: var(--bg-primary); /* Inner content background */
            border: 1px solid var(--border-color);
            border-top: none; /* Connects to header */
            border-radius: 0 0 var(--border-radius-md) var(--border-radius-md);
            padding: var(--spacing-md);
            box-shadow: inset 0 0 15px var(--shadow-light); /* Deeper inset shadow */
        }

        /* --- Horizontal Rule --- */
        hr {
            border-top: 1px solid var(--border-color);
            margin: var(--spacing-lg) 0;
            opacity: 0.7;
        }

        /* --- Sidebar Specific Styling --- */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-secondary); /* Matches main content card background for cohesion */
            border-right: 1px solid var(--border-color);
            box-shadow: 2px 0px 10px var(--shadow-medium); /* Stronger shadow for sidebar */
            padding-top: var(--spacing-md);
            color: var(--text-light);
        }
        section[data-testid="stSidebar"] .st-emotion-cache-vk33gh { /* Targets inner sidebar content */
            padding-top: 0rem; /* Reset default padding if any */
        }
        section[data-testid="stSidebar"] h2 {
            color: var(--accent-blue-light);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 10px;
            margin-bottom: 20px;
            margin-top: 0; /* Align to top of sidebar */
            font-size: 1.8rem;
        }
        section[data-testid="stSidebar"] label {
            color: var(--text-light);
            font-weight: 600;
            font-size: 1.05rem;
            margin-bottom: 0.5rem;
        }

        /* --- Custom Metric Card (Example - if you implement KPI metrics later) --- */
        .custom-metric-card {
            background-color: var(--bg-tertiary);
            border-radius: var(--border-radius-md);
            padding: 1.5rem;
            box-shadow: 0 6px 15px var(--shadow-medium);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            min-height: 140px;
            border: 1px solid var(--border-color);
            height: 100%;
        }
        .custom-metric-card:hover {
            transform: translateY(-7px);
            box-shadow: 0 10px 25px var(--shadow-medium);
        }
        .custom-metric-value {
            font-size: 3.5em; /* Larger value font */
            font-weight: 800;
            line-height: 1;
            margin-bottom: 0.2rem;
            color: var(--accent-blue-light);
            text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        }
        .custom-metric-label {
            font-size: 1.15em;
            color: var(--text-medium);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.5rem;
        }
        .custom-metric-label i {
            margin-right: 0.8rem;
            color: var(--accent-blue-dark);
        }
        /* --- General Spacing for Streamlit blocks --- */
        .stVerticalBlock {
            gap: 2rem; /* Increased vertical spacing */
        }

        /* --- Responsive Design (Adjustments for smaller screens) --- */
        @media (max-width: 1200px) {
            .main .block-container {
                padding: 2.2rem 3rem;
            }
        }
        @media (max-width: 1024px) {
            .main .block-container {
                padding: 2rem 2.5rem;
                margin: 2rem auto;
            }
            .stMarkdown h1, .stMarkdown h2 {
                font-size: 2.2rem;
            }
            .stMarkdown h3 {
                font-size: 1.7rem;
            }
            .stButton > button {
                padding: 0.9rem 1.8rem;
                font-size: 1.05rem;
            }
        }
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1.5rem;
                margin: 1.5rem auto;
                width: 95%; /* Adjust width for better mobile fit */
            }
            .stButton > button {
                display: block;
                width: 100%;
                margin: 0.8rem 0;
            }
            .stMarkdown h1, .stMarkdown h2 {
                font-size: 2rem;
            }
            .stMarkdown h3 {
                font-size: 1.5rem;
            }
            .stMarkdown h4 {
                font-size: 1.2rem;
            }
            textarea, .stTextInput > div > div > input, .stSelectbox > div > div {
                padding: 0.7rem 1.1rem;
                font-size: 0.95rem;
            }
            .stTabs [data-baseweb="tab-list"] button {
                padding: 0.7rem 0.9rem;
                font-size: 0.95rem;
            }
            .stMarkdown ul {
                margin-left: 15px;
            }
            /* Adjust sidebar for smaller screens */
            section[data-testid="stSidebar"] {
                padding: 1rem;
            }
            section[data-testid="stSidebar"] h2 {
                font-size: 1.6rem;
            }
        }
        @media (max-width: 480px) {
            .main .block-container {
                padding: 1rem;
                margin: 1rem auto;
            }
            .stMarkdown h1, .stMarkdown h2 {
                font-size: 1.8rem;
                padding-bottom: 0.5rem;
            }
            .stMarkdown h1::after, .stMarkdown h2::after {
                width: 50px;
                height: 4px;
            }
            .stMarkdown h3 {
                font-size: 1.3rem;
            }
            .stButton > button {
                padding: 0.7rem 1.2rem;
                font-size: 1em;
            }
            .stMarkdown pre code {
                padding: 1em;
                font-size: 0.85em;
            }
            .stAlert {
                padding: 1rem 1.2rem;
                font-size: 0.95rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Example of how this styling function would be called in main.py for testing:
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Log Analyzer Styling Showcase")
    
    apply_custom_styles() # Apply the new dark-themed styles

    st.title("Log Analyzer: Professional Dark Theme Demo 📊")
    st.markdown("""
    Welcome to the enhanced styling for data engineers and analysts! This theme aims for a
    **professional, modern, and dark aesthetic**, prioritizing readability and a clean interface.
    """)

    st.sidebar.header("Navigation & Upload")
    st.sidebar.markdown("Upload your log files here. 👇")
    st.sidebar.file_uploader("Upload Log File", type=["txt", "log"])
    st.sidebar.radio("Analysis Type", ["Summary", "Performance", "Errors"])
    st.sidebar.button("Analyze Logs")

    st.header("Key Insights & Summary")
    st.write("""
    This section will display the summarized insights from your log files.
    The goal is to provide **actionable intelligence** from vast log data.
    """)

    st.subheader("Example Log Explanation")
    st.markdown("""
    Here's a breakdown of a critical event:
    * **Timestamp:** `2024-06-25 14:30:15`
    * **Level:** `ERROR`
    * **Message:** `Database connection pool exhausted. Max connections reached (100).`
    * **Recommendation:** `Increase database connection limit or optimize query patterns.`

    This demonstrates how the system identifies key issues like:
    1.  **Errors:** `Connection refused`
    2.  **Warnings:** `High memory usage`
    3.  **Performance Bottlenecks:** `Long query execution`
    """)

    st.code("""
# Sample Python Log Snippet
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_task(task_id):
    logging.info(f"Task {task_id}: Starting process.")
    try:
        if task_id % 2 == 0:
            time.sleep(0.1) # Simulate some work
            logging.warning(f"Task {task_id}: High CPU usage detected during processing.")
        else:
            time.sleep(0.05)
            raise ValueError("Simulated critical error in task processing.")
    except ValueError as e:
        logging.error(f"Task {task_id}: Critical error occurred: {e}")
    logging.info(f"Task {task_id}: Process completed.")

for i in range(5):
    simulate_task(i)
    """, language="python")

    st.subheader("System Alerts and Notifications")
    st.success("Analysis complete! No critical errors detected in the provided logs.")
    st.warning("Warning: A few 'ResourceNotFound' errors were observed, but the system recovered.")
    st.error("Fatal Error: Unhandled exception detected. Please review logs immediately for 'NullPointerException'.")
    st.info("Info: Log analysis initiated successfully. Processing 1.2M log entries.")

    with st.expander("Click here for raw log details (for advanced debugging)"):
        st.write("""
        `2024-06-25 14:35:01 INFO MainThread: Starting application server.`
        `2024-06-25 14:35:05 WARN ConnectionPool: Max connections (50) reached for database 'metrics_db'.`
        `2024-06-25 14:35:10 ERROR DatabaseError: Could not connect to primary replica.`
        `2024-06-25 14:35:12 INFO Scheduler: Background job 'report_gen' finished in 1200ms.`
        """)

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-size: small; color: var(--text-medium); padding-top: 1rem;">
            Designed with <i class="fas fa-heart" style="color: var(--accent-red);"></i> by Your Team. Powered by Google Gemini & Streamlit.
        </div>
        """,
        unsafe_allow_html=True
    )