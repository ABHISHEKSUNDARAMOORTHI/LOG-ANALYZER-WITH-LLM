import streamlit as st
import os
from dotenv import load_dotenv
from styling import apply_custom_styles
from features import process_logs_and_summarize
import pandas as pd # New import for DataFrame
import plotly.express as px # New import for plotting

def main():
    """
    Main function to run the Streamlit application for the Log Analyzer with LLM.
    """
    st.set_page_config(
        page_title="LLM-Powered Log Analyzer",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    apply_custom_styles()

    st.title("Log Analyzer with LLM 🔍")
    st.markdown("""
        Upload your server or application log files here to get **AI-powered summaries**
        of errors, warnings, and performance bottlenecks. Get actionable insights in
        plain English, making debugging and monitoring faster and more efficient.
        
        **Simply upload a log file (.txt, .log) and click 'Analyze Logs'!**
    """)

    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("🚨 Google Gemini API Key is not set! Please add `GOOGLE_API_KEY=\"YOUR_API_KEY\"` to your `.env` file.")
        st.stop()

    st.sidebar.header("Upload Your Log File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a `.log` or `.txt` file",
        type=["log", "txt"],
        help="Upload your server or application log file here."
    )

    st.sidebar.header("Output Options")
    output_format = st.sidebar.radio(
        "Select Output Format:",
        ("Markdown", "HTML"),
        help="Choose the format for the downloadable log analysis report."
    ).lower()

    process_button = st.sidebar.button("Analyze Logs", use_container_width=True, type="primary")

    st.markdown("---")

    if uploaded_file is not None and process_button:
        with st.spinner("Analyzing logs and generating insights... This might take a moment."):
            # Updated call: now expects a 5th return value (df_logs)
            summary_text, download_link, success, error_message, df_logs = process_logs_and_summarize(uploaded_file, output_format)

            if success:
                st.success("Log Analysis Complete!")
                
                st.subheader("💡 Log Analysis Summary")
                st.markdown(summary_text) # This renders the structured Markdown output from AI

                # --- NEW GRAPH SECTION ---
                # Check if a valid DataFrame exists and has timestamps for plotting
                if df_logs is not None and not df_logs.empty and 'timestamp' in df_logs.columns and df_logs['timestamp'].notna().any():
                    st.markdown("---")
                    st.subheader("📊 Log Events Timeline")

                    # Define a consistent order for severity levels for plotting
                    severity_order = ['CRITICAL', 'FATAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG']
                    
                    # Define a color map for better visual distinction of severity
                    color_map = {
                        'CRITICAL': '#DC143C', # Crimson
                        'FATAL': '#8B0000',    # DarkRed
                        'ERROR': '#FF4500',    # OrangeRed
                        'WARN': '#FFD700',     # Gold
                        'WARNING': '#FFA500',  # Orange (used for WARN/WARNING interchangeably)
                        'INFO': '#1E90FF',     # DodgerBlue
                        'DEBUG': '#808080'     # Gray
                    }
                    
                    # Filter out rows with missing/NaT timestamps as they cannot be plotted on a timeline
                    df_plot = df_logs.dropna(subset=['timestamp']).copy()
                    
                    # Ensure 'level' column is categorical with the desired order for consistent Y-axis and legend
                    df_plot['level'] = pd.Categorical(df_plot['level'], categories=severity_order, ordered=True)
                    
                    # Sort by timestamp for proper timeline display
                    df_plot = df_plot.sort_values(by='timestamp')

                    # Create a scatter plot for events over time
                    fig = px.scatter(
                        df_plot,
                        x='timestamp',
                        y='level', # Y-axis represents the severity level, showing distinct bands for each
                        color='level',
                        color_discrete_map=color_map,
                        hover_data={'message': True, 'raw_line': True, 'timestamp': '|%Y-%m-%d %H:%M:%S,%f'}, # Show message and raw line in hover
                        title='Log Events by Severity Over Time',
                        labels={'timestamp': 'Time of Event', 'level': 'Severity Level'},
                        height=550 # Adjust height as needed
                    )

                    # Customize layout for better readability
                    fig.update_layout(
                        yaxis_title='Severity Level',
                        xaxis_title='Time',
                        hovermode="x unified", # Shows all hover info for points near the cursor's x-value
                        yaxis=dict(categoryorder='array', categoryarray=severity_order), # Ensure Y-axis order matches severity_order
                        legend_title_text='Log Level',
                        font=dict(family="Inter, sans-serif"),
                        title_font_size=20
                    )
                    
                    # Add a range slider to the x-axis for easier navigation of time series data
                    fig.update_xaxes(rangeslider_visible=True, rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1h", step="hour", stepmode="backward"),
                            dict(count=6, label="6h", step="hour", stepmode="backward"),
                            dict(count=1, label="1d", step="day", stepmode="backward"),
                            dict(step="all")
                        ])
                    ))

                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No sufficient log events with timestamps found to generate a timeline graph.")

                # --- END NEW GRAPH SECTION ---

                st.markdown("---")
                st.subheader("⬇️ Download Analysis Report")
                st.download_button(
                    label=f"Download {output_format.upper()} Report",
                    data=download_link,
                    file_name=uploaded_file.name.replace(".log", "").replace(".txt", "") + f"_log_summary.{output_format}",
                    mime=f"text/{output_format}",
                    key="download_log_report_button",
                    help=f"Click to download the log analysis report as a .{output_format} file."
                )
                
            else:
                st.error(f"Failed to analyze logs: {error_message}")
                if "API key" in error_message or "authentication" in error_message or "configure" in error_message:
                    st.warning("Ensure your Google Gemini API key is correctly set in the `.env` file and has sufficient permissions.")
                elif "UnicodeDecodeError" in error_message:
                    st.info("The log file might be in a different encoding. Try converting it to UTF-8 or ensure it's plain text.")
                st.info("If the issue persists, check your internet connection or try a different log file.")


    elif uploaded_file is None and process_button:
        st.warning("Please upload a `.log` or `.txt` file first before clicking 'Analyze Logs'.")
        
    elif uploaded_file is None:
        st.info("Upload your log file on the left sidebar and click 'Analyze Logs' to get started.")
        st.image("https://images.unsplash.com/photo-1551288259-f2ef4847e06a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w1NjY1OTR8MHwxfHNlYXJjaHw3MXx8bG9nfHxlbnwwfHx8fDE3MTk3NDgwODV8MA&ixlib=rb-4.0.3&q=80&w=1080",
                 caption="AI-Powered Log Analysis for System Reliability",
                 use_column_width=True)

    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; font-size: small; color: var(--text-medium);">
            Developed with ❤️ for Data Engineers & Analysts. Powered by Google Gemini and Streamlit.
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()