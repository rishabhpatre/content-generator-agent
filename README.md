# Arxiv to LinkedIn Agent 🚀

An autonomous AI agent that fetches the latest research papers from Arxiv, analyzes them for virality using Google Gemini, and generates professional, engaging LinkedIn posts daily.

## ✨ Features
- **Fetch Recent Papers**: Queries Arxiv for the latest "LLM" and "Artificial Intelligence" papers.
- **Gather AI News**: Aggregates news from top AI blogs (OpenAI, Google, Anthropic, etc.) via RSS.
- **Daily AI Concept**: Generates an educational "Concept of the Day" (e.g., LoRA, RAG) with a **visual flowchart** (Mermaid.js).
- **Smart Analysis**: Uses **Google Gemini 2.5 Flash** (Free Tier) to pick the most engaging topics.
- **Multi-Format Content**: Creates research summaries, news updates, and educational deep-dives.
- **Daily Automation**: Runs automatically via GitHub Actions every day at 07:00 AM IST.

## 🛠️ Usage

### Local Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/rishabhpatre/content-generator-agent.git
    cd content-generator-agent
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables:
    Create a `.env` file in the root directory:
    ```
    GOOGLE_API_KEY=your_gemini_api_key
    ```
4.  Run the agent:
    ```bash
    python main.py
    ```

### 🤖 Automation Setup (GitHub Actions)
To have this run daily and email you the post:

1.  **Fork/Clone** this repository to your GitHub.
2.  Go to **Settings > Secrets and variables > Actions** in your repo.
3.  Add the following **Repository Secrets**:
    *   `GOOGLE_API_KEY`: Your Gemini API Key ([Get it here](https://aistudio.google.com/app/apikey)).
    *   `SMTP_EMAIL`: The Gmail address to send *from*.
    *   `SMTP_PASSWORD`: Your Gmail App Password.
        > **How to get this (Gmail):**
        > 1. Go to [Google My Account](https://myaccount.google.com/).
        > 2. Search for "App passwords" -> Create one named "LinkedIn Agent".
        > 3. Copy the 16-character code.
    *   `RECIPIENT_EMAIL`: The email address to receive the post *at*.
4.  **Done!** The workflow will run automatically every day at 07:00 AM IST (01:30 UTC).

## 📁 Project Structure
- `src/arxiv_client.py`: Fetches papers from Arxiv.
- `src/llm_processor.py`: Uses Gemini to analyze papers and write posts.
- `src/email_client.py`: Handles sending emails via SMTP.
- `main.py`: The entry point script.
- `.github/workflows/daily_digest.yml`: Automation configuration.

## 📄 License
MIT License. Feel free to use and modify!
