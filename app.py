# app.py
import streamlit as st
import requests

st.set_page_config(page_title="EY GenAI Banker", page_icon="🏦", layout="wide")

st.title("🏦 EY Agentic Banker")
st.markdown("### Techathon Demo: Multi-Agent Orchestration")

# --- Sidebar: Simulation Controls ---
with st.sidebar:
    st.header("🎛️ Simulation Controls")
    
    # Identity Switcher
    # We use a key to detect changes
    user_profile = st.selectbox(
        "Select Customer Persona:", 
        ["Alex Johnson", "Neha R"], 
        key="user_profile_select"
    )
    
    if user_profile == "Alex Johnson":
        default_income = 75000
        pre_approved_hint = "Limit: $50k"
    else:
        default_income = 120000
        pre_approved_hint = "Limit: $100k"

    st.info(f"**CRM Data Loaded:** {pre_approved_hint}")
    
    income = st.number_input("Monthly Income ($)", value=default_income)
    req_amount = st.number_input("Requested Loan Amount ($)", value=80000, step=5000)
    
    st.markdown("---")
    st.markdown("**⚠️ Edge Case Trigger**")
    salary_slip = st.checkbox("Simulate 'Salary Slip' Upload?", value=False)
    
    # Add a Reset Button to restart the demo easily
    if st.button("🔄 Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# --- PERSUASIVE INTRODUCTION LOGIC ---
# This ensures a specific greeting appears every time the user lands or resets
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    
    # Dynamic Persuasive Greeting based on the User
    if user_profile == "Alex Johnson":
        greeting = (
            "**Hello Alex!** 👋 I’m your dedicated AI Wealth Partner at EY. \n\n"
            "I’ve reviewed your portfolio, and I see you're eligible for our **exclusive 'Corp-Advantage' rates** "
            "usually reserved for top-tier clients. We have **$50,000** pre-approved and waiting for you. \n\n"
            "Are you looking to leverage this capital for a car, an investment, or personal growth today?"
        )
    else:
        greeting = (
            "**Welcome, Neha!** 👋 Great to see you again. \n\n"
            "Your financial standing is excellent. Our system has unlocked a **$100,000 limit** specifically for you "
            "under the **'Tech-Professional'** scheme. This comes with our most flexible repayment terms. \n\n"
            "How can we put this capital to work for you right now?"
        )
        
    st.session_state.messages = [{"role": "assistant", "content": greeting}]

# --- Chat Interface ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle Input ---
if prompt := st.chat_input("Type your response here..."):
    # 1. User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Prepare Payload
    payload = {
        "name": user_profile,
        "query": prompt,
        "requested_amount": req_amount,
        "income": income,
        "salary_slip_uploaded": salary_slip
    }

    # 3. Call API with Spinner
    with st.chat_message("assistant"):
        with st.spinner("🔄 EY Agents Working... (Sales -> Verification -> Underwriting)"):
            try:
                response = requests.post("http://127.0.0.1:8000/chat", json=payload)
                data = response.json()
                bot_reply = data["response"]
                has_file = data.get("has_file", False)

                # Typewriter effect for the reply
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                # 4. Show Download Button if Success
                if has_file:
                    st.markdown("---")
                    st.success("🎉 Sanction Letter Generated!")
                    st.markdown(f"[📥 Download Official Sanction Letter](http://127.0.0.1:8000/download-sanction)")

            except Exception as e:
                st.error(f"Connection Error: {e}")