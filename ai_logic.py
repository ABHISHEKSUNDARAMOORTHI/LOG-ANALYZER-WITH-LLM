import google.generativeai as genai
import os
from dotenv import load_dotenv

def _get_suitable_model():
    """
    Finds and returns a suitable GenerativeModel that supports generate_content.
    Prioritizes 'gemini-1.5-flash-latest' or 'gemini-1.0-pro'.
    """
    try:
        available_models = genai.list_models()
        
        supported_models = []
        for m in available_models:
            if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods:
                supported_models.append(m.name)

        if 'models/gemini-1.5-flash-latest' in supported_models:
            return 'gemini-1.5-flash-latest'
        elif 'models/gemini-1.0-pro' in supported_models:
            return 'gemini-1.0-pro'
        elif 'models/gemini-pro' in supported_models:
            return 'gemini-pro'
        elif supported_models:
            for model_name in supported_models:
                if 'embedding' not in model_name and 'aqa' not in model_name:
                    return model_name.replace('models/', '')
            raise ValueError("No suitable text generation model found that supports generateContent after filtering.")
        else:
            raise ValueError("No models found that support generateContent.")

    except Exception as e:
        raise ConnectionError(f"Failed to list or select a suitable Generative AI model: {e}")


def generate_log_summary(log_snippets: str) -> str:
    """
    Analyzes provided log snippets using Google's Generative AI
    and returns a plain English summary of errors, warnings,
    and performance bottlenecks with suggested actions, formatted creatively.

    Args:
        log_snippets (str): A string containing relevant error/warning log lines.

    Returns:
        str: A concise, plain English summary and insights from the logs,
             or an error message if the AI call fails.
    """
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        return "ERROR: GOOGLE_API_KEY is not set in your .env file. Please ensure it's configured."

    try:
        genai.configure(api_key=GOOGLE_API_KEY)
    except Exception as e:
        return f"ERROR: Could not configure Google Generative AI. Check API key format or network: {e}"

    try:
        model_name = _get_suitable_model()
        model = genai.GenerativeModel(model_name)
        print(f"DEBUG: Using model: {model_name}")
    except Exception as e:
        return f"ERROR: Could not initialize Generative Model: {e}"

    # --- MODIFIED PROMPT FOR CREATIVE, POINT-BASED OUTPUT ---
    prompt = f"""
    You are an AI-powered System Health Monitor and Log Forensics Expert. Your mission is to dissect the provided log data and deliver a crystal-clear, actionable summary. Infuse your analysis with a touch of insight and urgency where needed.

    Please provide your analysis in the following structured, creative format, using Markdown for readability. Be concise but comprehensive.

    ### ⏰ Timeline Snapshot:
    - Identify the primary time range of significant events.

    ### 🚨 Critical Alarms & Issues:
    - List the most severe errors (e.g., CRITICAL, ERROR) detected.
    - Briefly explain the nature of each critical issue.

    ### ⚠️ Warnings & Potential Bottlenecks:
    - Detail any warnings or indicators of potential problems (e.g., high resource usage, API throttling, low disk space).

    ### 💡 Underlying Causes & Insights:
    - Based on the log context, what are the most probable root causes for the identified problems? Synthesize information rather than just listing.

    ### 🛠️ Recommended Immediate Actions:
    - Provide a prioritized list of actionable steps for investigation and resolution.

    ---
    Log Snippets to Analyze:
    {log_snippets}
    ---
    """

    # 5. Make the LLM API Call
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2, # Lower temperature for more focused, less creative responses
            )
        )

        if response and response.parts:
            return response.text
        elif response and response.candidates and response.candidates[0].text:
            return response.candidates[0].text
        else:
            return "AI response structure not as expected. Could not extract text from the model's response."

    except Exception as e:
        print(f"DEBUG: Error during LLM API call: {e}")
        return f"An error occurred while calling the Google Generative AI API: {e}. Please check your API key, network connection, and ensure the model is available in your region."

# --- Example Usage (for local testing of ai_logic.py) ---
if __name__ == "__main__":
    print("--- Testing AI Logic (ensure GOOGLE_API_KEY is set in .env) ---")

    dummy_log_content_with_errors = """
    2024-06-25 10:00:01,123 INFO Application started successfully. Version 1.0.
    2024-06-25 10:00:05,456 DEBUG User 'admin' logged in from IP 192.168.1.10.
    2024-06-25 10:00:15,789 WARN High CPU usage detected on 'web-server-01'. Current: 85%.
    2024-06-25 10:00:20,000 INFO Processing request for '/api/data'.
    2024-06-25 10:00:22,333 ERROR Database connection failed for 'user_db': Connection refused. Retrying in 5 seconds.
    2024-06-25 10:00:28,666 ERROR [CRITICAL] Memory leak detected in process PID 1234. OOM imminent. Please investigate immediately.
    2024-06-25 10:00:30,999 WARN API rate limit hit for external service 'analytics_api'. Requests being throttled.
    2024-06-25 10:00:35,123 INFO Data synchronization complete. 1000 records processed.
    2024-06-25 10:00:40,456 ERROR User authentication failed for 'john.doe'. Invalid credentials.
    2024-06-25 10:00:45,789 INFO Server health check passed.
    2024-06-25 10:00:50,111 WARN Disk space low on /var/log. Remaining: 5%.
    2024-06-25 10:00:55,444 INFO Batch job 'daily_report_generation' started.
    2024-06-25 10:01:05,777 INFO Batch job 'daily_report_generation' completed successfully.
    2024-06-25 10:01:10,000 ERROR [HTTP 504] Gateway Timeout from upstream server. Request ID: abcdef123.
    2024-06-25 10:01:12,333 INFO User 'jane.doe' accessed report 'financial_summary'.
    2024-06-25 10:01:18,666 ERROR Unhandled exception in data processing module: ValueError: Invalid input data.
    2024-06-25 10:01:25,999 INFO Log rotation initiated.
    2024-06-25 10:01:30,321 WARN High network latency to external service 'payment_gateway'. Ping: 500ms.
    2024-06-25 10:01:35,654 INFO System backup initiated.
    """

    print("\n--- Running with Logs Containing Errors/Warnings ---")
    summary_with_errors = generate_log_summary(dummy_log_content_with_errors)
    print(summary_with_errors)

    print("\n--- Running with Logs Containing No Errors/Warnings ---")
    dummy_log_content_no_errors = """
    2024-06-25 10:00:01,123 INFO User 'testuser' logged in.
    2024-06-25 10:00:05,456 INFO Background job 'cleanup' started.
    2024-06-25 10:00:10,789 INFO Cache refreshed successfully.
    2024-06-25 10:00:12,000 DEBUG Auth service response: 200 OK.
    """
    summary_no_errors = generate_log_summary(dummy_log_content_no_errors)
    print(summary_no_errors)

    print("\n--- Running with Empty Log Content ---")
    empty_summary = generate_log_summary("")
    print(empty_summary)