# GenAI Banker - Tata Capital Techathon
This is a full-stack, multi-agent AI solution built for the EY Techathon (TATA Capital BFSI Challenge).

The project simulates an intelligent, persuasive sales agent that guides a customer from an initial chat to a final loan sanction, handling complex business logic and edge cases.

## Architecture: The "Agentic Orchestra"

This solution uses a "Master-Worker" model without relying on complex frameworks (like CrewAI), making it stable and fast. The `main.py` script acts as the Master Agent (orchestrator) and coordinates a team of specialists:

* **Master Agent:** The main orchestrator that routes tasks.
* **Router Agent:** Intelligently decides if the user is "chatting" or "ready to apply."
* **Verification Agent:** Connects to a Mock CRM to fetch KYC data.
* **Sales Agent:** Connects to a Mock Offer Mart to pitch persuasive, data-driven schemes (rates, tenure).
* **Underwriting Agent:** Connects to a Mock Credit Bureau and runs the hard-coded business logic (e.g., `< 700 score = REJECT`).
* **Sanction Letter Agent:** Generates the final `.txt` sanction letter.

## Tech Stack
* **Frontend:** Streamlit
* **Backend:** FastAPI
* **AI Engine:** Google Gemini
* **Orchestration:** "Framework-less" Python

## How to Run This Demo

1.  **Clone the repo:**
    `git clone [your-repo-url]`
2.  **Create a virtual environment:**
    `python -m venv venv`
    `.\venv\Scripts\activate`
3.  **Install dependencies:**
    `pip install -r requirements.txt`
4.  **Create your secret file:**
    * Create a file named `.env`
    * Add your Google API key: `GOOGLE_API_KEY=AIza...`
5.  **Run the Backend (Terminal 1):**
    `python api.py`
6.  **Run the Frontend (Terminal 2):**
    `streamlit run app.py`
    
