# 🔍 LLM-Powered Log Analyzer

## Overview

The **LLM-Powered Log Analyzer** is a Streamlit web application designed to simplify the process of reviewing and understanding complex server or application log files. Leveraging the power of Google's Gemini Large Language Model, this tool provides intelligent, plain-English summaries of critical events, warnings, and potential issues within your logs, along with an interactive timeline graph for visual analysis.

Say goodbye to manually sifting through thousands of log lines! Just upload your log file, and let the AI provide actionable insights.

## ✨ Features

* **AI-Powered Summaries:** Get concise, structured summaries of errors, warnings, and performance bottlenecks from your log files using Google's Gemini LLM.
* **Structured Output:** Summaries are presented in a clear, point-by-point format (Timeline, Critical Alarms, Warnings, Underlying Causes, Recommended Actions).
* **Interactive Event Timeline:** Visualize log events over time with an interactive Plotly graph, color-coded by severity (CRITICAL, ERROR, WARN, INFO, DEBUG). Easily spot trends and anomalies.
* **Flexible Log Parsing:** Intelligently parses common log formats, extracting timestamps and severity levels.
* **Downloadable Reports:** Download the AI-generated analysis in either Markdown (`.md`) or HTML (`.html`) format for sharing or record-keeping.
* **User-Friendly Interface:** Built with Streamlit for a simple and intuitive drag-and-drop file upload experience.
* **Robust Model Selection:** Automatically selects the best available Gemini model (`gemini-1.5-flash-latest`, `gemini-1.0-pro`, or `gemini-pro`) for text generation.

## 🚀 How It Works

1.  **Upload:** You upload a `.log` or `.txt` file via the Streamlit interface.
2.  **Parse:** The application parses the log file, extracting relevant lines (especially errors and warnings) and structured data (timestamps, severity levels) from all lines.
3.  **Summarize (LLM):** The extracted error/warning lines are sent to the Google Gemini LLM, which generates a comprehensive, plain-English summary of the issues.
4.  **Visualize:** The parsed log data is used to create an interactive timeline graph, allowing you to quickly see the distribution of log events over time.
5.  **Display & Download:** The AI-generated summary and the interactive graph are displayed in the web application. You also get an option to download the summary report.

## 🛠️ Setup Instructions

Follow these steps to get the Log Analyzer running on your local machine.

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone [https://github.com/your-username/llm-log-analyzer.git](https://github.com/your-username/llm-log-analyzer.git) # Replace with your actual repo URL if hosted
cd llm-log-analyzer
````

### 2\. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage project dependencies:

```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3\. Install Dependencies

All necessary Python packages are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

*(If you encounter issues with `markdown`, try `pip install markdown` separately.)*

### 4\. Set Up Google Gemini API Key

This project requires a Google Gemini API Key to interact with the Large Language Model.

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).

2.  If you don't have an API key, create one. It's free for basic usage within generous limits.

3.  Create a file named `.env` in the root directory of your project (the same directory as `main.py`).

4.  Add your API key to this `.env` file in the following format:

    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

    Replace `"YOUR_API_KEY_HERE"` with the actual key you obtained from Google AI Studio.

    **Example `.env` file:**

    ```
    GOOGLE_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXX"
    ```

    **Security Note:** Never commit your `.env` file (which contains your API key) to public version control systems like GitHub. It's already included in `.gitignore` for this reason.

## 🚀 Running the Application

Once you have completed the setup:

1.  Ensure your virtual environment is active.

2.  Navigate to the project's root directory in your terminal.

3.  Run the Streamlit application:

    ```bash
    streamlit run main.py
    ```

    Your default web browser should automatically open a new tab pointing to the application (usually `http://localhost:8501`). Keep the terminal window open as long as you want the application to run. To stop the application, press `Ctrl + C` in the terminal.

## 📂 Project Structure

```
llm-log-analyzer/
├── .env                  # Your Google Gemini API Key (keep private!)
├── .gitignore            # Specifies intentionally untracked files to ignore
├── main.py               # Main Streamlit application entry point
├── features.py           # Contains core logic for log parsing and orchestrating AI calls
├── ai_logic.py           # Handles Google Gemini API interaction and prompt engineering
├── styling.py            # Custom CSS for the Streamlit app
├── requirements.txt      # Lists all Python dependencies
└── README.md             # This file!
```

## 🧪 Testing with Sample Data

You can use the following content to create a `sample_log.log` file in your project directory for quick testing:

```log
2024-06-25 10:00:01 INFO Application started successfully. Version 1.0.
2024-06-25 10:00:05 DEBUG User 'admin' logged in from IP 192.168.1.10.
2024-06-25 10:00:15 WARN High CPU usage detected on 'web-server-01'. Current: 85%.
2024-06-25 10:00:20 INFO Processing request for '/api/data'.
2024-06-25 10:00:22 ERROR Database connection failed for 'user_db': Connection refused. Retrying in 5 seconds.
2024-06-25 10:00:28 ERROR [CRITICAL] Memory leak detected in process PID 1234. OOM imminent. Please investigate immediately.
2024-06-25 10:00:30 WARN API rate limit hit for external service 'analytics_api'. Requests being throttled.
2024-06-25 10:00:35 INFO Data synchronization complete. 1000 records processed.
2024-06-25 10:00:40 ERROR User authentication failed for 'john.doe'. Invalid credentials.
2024-06-25 10:00:45 INFO Server health check passed.
2024-06-25 10:00:50 WARN Disk space low on /var/log. Remaining: 5%.
2024-06-25 10:00:55 INFO Batch job 'daily_report_generation' started.
2024-06-25 10:01:05 INFO Batch job 'daily_report_generation' completed successfully.
2024-06-25 10:01:10 ERROR [HTTP 504] Gateway Timeout from upstream server. Request ID: abcdef123.
2024-06-25 10:01:12 INFO User 'jane.doe' accessed report 'financial_summary'.
2024-06-25 10:01:18 ERROR Unhandled exception in data processing module: ValueError: Invalid input data.
2024-06-25 10:01:25 INFO Log rotation initiated.
2024-06-25 10:01:30 WARN High network latency to external service 'payment_gateway'. Ping: 500ms.
2024-06-25 10:01:35 INFO System backup initiated.
```

Upload this file to the Streamlit app to see the AI summary and the event timeline.

## 🔮 Future Enhancements

  * **More Sophisticated Log Parsing:** Support for multi-line log entries, custom log formats, and more robust error handling for malformed lines.
  * **Severity Filtering for Graph:** Allow users to filter which severity levels are shown on the graph.
  * **Log Level Configuration:** Let users define which log levels constitute "errors" or "warnings" for LLM analysis.
  * **Real-time Log Streaming:** Integrate with a log streaming service (e.g., Kafka, Pub/Sub) for real-time analysis.
  * **Alerting Integration:** Connect to alerting systems (e.g., Slack, PagerDuty) based on critical summaries.
  * **AI Model Fine-tuning:** Fine-tune the LLM on specific log patterns for even more accurate and domain-specific insights.
  * **Token Usage Tracking:** Display LLM token usage to help users manage costs on higher tiers.

## 🤝 Contributing

Contributions are welcome\! If you have ideas for improvements, bug fixes, or new features, please open an issue or submit a pull request.

## 🙏 Acknowledgements

  * **Google Gemini:** For providing the powerful large language model.
  * **Streamlit:** For enabling rapid development of interactive web applications in Python.
  * **Plotly:** For the excellent interactive charting capabilities.
