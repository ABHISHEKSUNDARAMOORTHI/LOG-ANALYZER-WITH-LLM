import os
import re
import base64
import json
from io import StringIO, BytesIO
import markdown
import pandas as pd # New import for DataFrame
from datetime import datetime # New import for datetime parsing

from ai_logic import generate_log_summary

def parse_log_data(log_content: str, max_lines_for_llm: int = 200) -> dict:
    """
    Parses log content to extract detailed event information (timestamp, level, message)
    into a Pandas DataFrame, and also collects raw error/warning lines for the LLM.

    Args:
        log_content (str): The full content of the log file as a string.
        max_lines_for_llm (int): Maximum number of log lines to send to the LLM.

    Returns:
        dict: A dictionary containing:
            'df_logs': Pandas DataFrame with parsed log entries (timestamp, level, message, raw_line).
            'error_warning_raw_lines': List of raw error/warning strings for LLM.
    """
    log_lines = log_content.splitlines()
    parsed_entries = []
    raw_error_warning_lines = []

    # Regex for common log patterns: YYYY-MM-DD HH:MM:SS,ms [LEVEL] MESSAGE
    # This regex is made more flexible for cases where timestamp/level might be missing or vary
    log_pattern = re.compile(
        r"^(?P<timestamp_str>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d{3})?)?\s*" # Optional timestamp (YYYY-MM-DD HH:MM:SS,ms)
        r"(?:\[?(?P<level>INFO|WARN|WARNING|ERROR|DEBUG|CRITICAL|FATAL)\]?)?\s*" # Optional Level (e.g., [ERROR] or ERROR)
        r"(?P<message>.*)" # The rest is the message
    )

    for line in log_lines:
        line = line.strip()
        if not line:
            continue

        match = log_pattern.match(line)
        
        timestamp_str = None
        level = "INFO" # Default level if not explicitly found
        message = line # Default message is the whole line

        if match:
            # Extract named groups
            timestamp_str = match.group('timestamp_str')
            level_group = match.group('level')
            message = match.group('message').strip()

            if level_group:
                level = level_group.upper()
            
            # If a timestamp was matched but message is empty, the whole line might be the message
            if not message and timestamp_str and level_group:
                message = line[match.end('timestamp_str'):].strip() # Take everything after timestamp
                if level_group: # If level was also matched, take everything after level
                    message = line[match.end('level'):].strip()


        # Fallback for lines that don't fit regex but contain keywords
        # This ensures lines with "ERROR" or "WARN" are caught even without a perfect match
        if "ERROR" in line.upper() and level != "ERROR" and level != "CRITICAL" and level != "FATAL":
            level = "ERROR"
        elif ("WARN" in line.upper() or "WARNING" in line.upper()) and level != "WARN" and level != "WARNING":
            level = "WARN"

        # Create parsed entry for DataFrame
        parsed_entry = {
            "timestamp_str": timestamp_str,
            "level": level,
            "message": message,
            "raw_line": line
        }
        parsed_entries.append(parsed_entry)

        # Collect raw error/warning lines for LLM (including CRITICAL/FATAL)
        if level in ["ERROR", "WARN", "WARNING", "CRITICAL", "FATAL"]:
            if len(raw_error_warning_lines) < max_lines_for_llm:
                raw_error_warning_lines.append(line)

    df_logs = pd.DataFrame(parsed_entries)

    # Convert timestamp strings to datetime objects, handling potential missing timestamps
    if 'timestamp_str' in df_logs.columns and not df_logs['timestamp_str'].isnull().all():
        # Try parsing with milliseconds first, then without
        df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp_str'], errors='coerce', format='%Y-%m-%d %H:%M:%S,%f')
        # Fill NaT for timestamps that didn't match with milliseconds format
        if df_logs['timestamp'].isnull().any():
            df_logs['timestamp'] = df_logs['timestamp'].fillna(
                pd.to_datetime(df_logs['timestamp_str'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
            )
    else:
        df_logs['timestamp'] = pd.NaT # Add a NaT column if no timestamps found at all

    return {
        "df_logs": df_logs, # Return the full DataFrame for plotting
        "error_warning_raw_lines": raw_error_warning_lines, # For LLM summary
    }


def process_logs_and_summarize(uploaded_file, output_format: str = "markdown") -> tuple[str, str | None, bool, str | None, pd.DataFrame | None]:
    """
    Handles an uploaded log file, parses it, generates a summary using LLM,
    and returns the summary text along with a downloadable link, a success status,
    an error message, and a DataFrame of parsed logs.

    Args:
        uploaded_file (streamlit.runtime.uploaded_file_manager.UploadedFile):
            The file object uploaded via Streamlit's st.file_uploader.
        output_format (str): The desired output format ('markdown' or 'html').

    Returns:
        tuple[str, str | None, bool, str | None, pd.DataFrame | None]: A tuple containing:
            - The generated summary text (Markdown format) if successful, otherwise an empty string.
            - A base64 encoded download link for the generated summary file (str) or None.
            - A boolean indicating if the operation was successful (True/False).
            - An error message (str) if the operation failed, otherwise None.
            - A Pandas DataFrame of parsed log data, or None if parsing failed.
    """
    if uploaded_file is None:
        return "", None, False, "Please upload a log file to get started.", None

    log_content = None
    df_logs = None # Initialize df_logs
    try:
        log_content = uploaded_file.read().decode("utf-8")

        parsed_data = parse_log_data(log_content, max_lines_for_llm=200)
        df_logs = parsed_data["df_logs"] # Get the DataFrame
        logs_for_llm = "\n".join(parsed_data["error_warning_raw_lines"])
        
        # If no relevant errors/warnings found for LLM, return early with success
        if not logs_for_llm and not parsed_data["error_warning_raw_lines"]:
            return "No significant errors or warnings found in the provided log file.", None, True, None, df_logs

        summary_text = generate_log_summary(logs_for_llm)

        if not summary_text or summary_text.startswith("ERROR:"):
            return "", None, False, summary_text, df_logs # Pass df_logs even on LLM error

        download_filename_prefix = uploaded_file.name.replace(".log", "").replace(".txt", "")
        download_link = None
        mime_type = None
        output_content = summary_text

        if output_format == "markdown":
            download_filename = f"{download_filename_prefix}_log_summary.md"
            encoded_content = base64.b64encode(output_content.encode("utf-8")).decode()
            mime_type = "text/markdown"
            download_link = f'data:{mime_type};base64,{encoded_content}'
        elif output_format == "html":
            html_summary = markdown.markdown(output_content, extensions=['fenced_code', 'tables', 'nl2br'])
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Log Explanation - {download_filename_prefix}</title>
                <style>
                    body {{ font-family: 'Inter', sans-serif; line-height: 1.6; margin: 20px; color: #333; }}
                    h1, h2, h3, h4, h5, h6 {{ font-family: 'Inter', sans-serif; color: #2E86C1; }}
                    h2 {{ border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 30px; }}
                    pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                    code {{ background-color: #f9f9f9; padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
                    ul {{ list-style-type: disc; padding-left: 20px; }}
                    ol {{ padding-left: 20px; }}
                    ul li, ol li {{ margin-bottom: 5px; }}
                </style>
            </head>
            <body>
                {html_summary}
            </body>
            </html>
            """
            download_filename = f"{download_filename_prefix}_log_summary.html"
            encoded_content = base64.b64encode(html_content.encode("utf-8")).decode()
            mime_type = "text/html"
            download_link = f'data:{mime_type};base64,{encoded_content}'
        else:
            return summary_text, None, False, "Unsupported output format. Only Markdown and HTML are supported for download.", df_logs

        return summary_text, download_link, True, None, df_logs # Return df_logs on success

    except UnicodeDecodeError:
        return "", None, False, "Failed to read log file: UnicodeDecodeError. Try a different encoding (e.g., 'latin-1') or ensure it's a plain text file.", df_logs
    except Exception as e:
        return "", None, False, f"An unexpected error occurred during log processing: {e}", df_logs