# main.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import our specific tools
from tools import verify_kyc_data, fetch_credit_data, underwriting_logic, generate_sanction_letter_file

# Setup
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('models/gemini-flash-latest')

# =====================================================================
# 1. Verification Agent (KYC)
# =====================================================================
def run_verification_agent(name):
    """Checks the Mock CRM."""
    print(f"\n[Master] -> 🕵️  Delegating to Verification Agent...")
    kyc_result = verify_kyc_data(name)
    
    if "FAILED" in kyc_result:
        return False, "KYC Check Failed. User not found."
    return True, "KYC Verified."

# =====================================================================
# 2. Router Agent (The Decision Maker) - NEW!
# =====================================================================
def run_router_agent(query):
    """Decides if we should SELL or PROCESS based on user input."""
    print(f"\n[Master] -> 🧠 Delegating to Router Agent...")
    
    prompt = f"""
    Analyze the user's input: "{query}"
    
    Determine the intent. Choose exactly one option:
    
    1. "CHAT": If the user is greeting, asking questions, expressing doubt, negotiating, or just starting the conversation.
    2. "APPLY": If the user explicitly says "yes", "go ahead", "proceed", "submit", "approve me", or confirms they want the loan.
    
    Output only the word CHAT or APPLY.
    """
    response = model.generate_content(prompt)
    decision = response.text.strip().upper()
    print(f"[Router Decision]: {decision}")
    return decision

# =====================================================================
# 3. Sales Agent (Negotiation & Persuasion)
# =====================================================================
def run_sales_agent(name, query, credit_data):
    """Discovers needs and persuades the user."""
    print(f"\n[Master] -> 💼 Delegating to Sales Agent...")
    
    schemes = credit_data['schemes'] # This is now a list of objects
    limit = credit_data['pre_approved_limit']
    
    # Create a clean string of the scheme details for the prompt
    scheme_details = ""
    for s in schemes:
        scheme_details += f"- Scheme: **{s['name']}** at **{s['rate']}%** interest for **{s['tenure']} years**.\n"
    
    # UPDATED PERSUASIVE PROMPT
    prompt = f"""
    You are a world-class Senior Relationship Manager at EY Bank. You are charismatic, professional, and highly persuasive.
    
    User Name: {name}
    User Query: "{query}"
    
    Backend Data:
    - Pre-approved Limit: ${limit} (This is "ready money")
    - Exclusive Schemes Available:
    {scheme_details}
    
    Your Strategy:
    1. **Validate & Elevate:** Acknowledge their query. Treat them like a VIP investor.
    2. **Pitch Details:** Clearly state the details of the schemes (rate, tenure) you have for them.
    3. **Persuade:** If they are hesitant, use the low rates or flexible tenure as a reason to act now.
    4. **The Close:** End with a direct, confident question to move to the next step (e.g., "Which of these options sounds best for your goals?").
    
    Goal: Get them to say "Yes" or "Proceed".
    """
    response = model.generate_content(prompt)
    return response.text

# =====================================================================
# 4. Underwriting Agent (The Logic Brain)
# =====================================================================
def run_underwriting_agent(amount, income, credit_data, salary_slip_uploaded=False):
    """Runs the strict math and logic rules."""
    print(f"\n[Master] -> ⚖️  Delegating to Underwriting Agent...")
    
    decision_raw = underwriting_logic(
        req_amount=amount,
        income=income,
        pre_approved_limit=credit_data['pre_approved_limit'],
        credit_score=credit_data['score'],
        salary_slip_uploaded=salary_slip_uploaded
    )
    
    return decision_raw

# =====================================================================
# 5. Sanction Letter Generator
# =====================================================================
def run_sanction_generator(name, amount, scheme):
    """Creates the document."""
    print(f"\n[Master] -> 📄 Delegating to Sanction Generator...")
    result = generate_sanction_letter_file(name, amount, scheme)
    return result

# =====================================================================
# MASTER AGENT (The Orchestrator)
# =====================================================================
def run_master_agent(user_data):
    print("=======================================")
    print(f"🚀 Master Agent Started for: {user_data['name']}")
    print("=======================================")

    # --- STEP 1: Verify KYC ---
    is_verified, kyc_msg = run_verification_agent(user_data['name'])
    if not is_verified:
        return f"Conversation Ended: {kyc_msg}"

    # --- STEP 2: Fetch Backend Data ---
    credit_data = fetch_credit_data(user_data['name'])

    # --- STEP 3: Router Logic (The Fix) ---
    # We check what the user actually WANTS to do.
    intent = run_router_agent(user_data['query'])

    # --- PATH A: Just Chatting / Needs Persuasion ---
    if "CHAT" in intent:
        sales_pitch = run_sales_agent(user_data['name'], user_data['query'], credit_data)
        return f"{sales_pitch}"

    # --- PATH B: Proceeding to Application ---
    elif "APPLY" in intent:
        print(f"\n[Master]: User wants to apply. Triggering Underwriting...")
        
        # Run Logic
        decision = run_underwriting_agent(
            amount=user_data['requested_amount'],
            income=user_data['income'],
            credit_data=credit_data,
            salary_slip_uploaded=user_data['salary_slip_uploaded']
        )
        print(f"[Underwriting Decision]: {decision}")

        # Handle Edge Case (Pending Docs)
        if "PENDING_DOCS" in decision:
            print("\n[Master]: ⚠️  Edge Case Detected! High amount requested.")
            return f"We are almost there! However, because the requested amount (${user_data['requested_amount']}) is significantly higher than your pre-approved limit, regulations require us to verify your income. \n\n**Action Required:** Please check the 'Simulate Salary Slip Upload' box in the sidebar and say 'Proceed' to continue."

        # Handle Approval
        if "APPROVED" in decision:
            letter_status = run_sanction_generator(user_data['name'], user_data['requested_amount'], credit_data['schemes'][0]['name'])
            return f"Congratulations! {decision} \n\n{letter_status} \n\nI have generated your official Sanction Letter. You can download it using the link below."
        
        # Handle Rejection
        else:
            return f"Application Status: {decision}. \n\nUnfortunately, we cannot proceed with this specific amount at this time. Would you like to try a lower amount?"

    # Fallback
    return "I didn't quite understand. Do you want to proceed with the loan?"

# =====================================================================
# DEMO RUNNER
# =====================================================================
if __name__ == "__main__":
    # Test Data
    USER_DATA = {
        "name": "Alex Johnson",
        "query": "I am not sure if I should take the loan.", # Should trigger CHAT
        #"query": "Yes, go ahead and approve me.",         # Should trigger APPLY
        "requested_amount": 40000,
        "income": 75000,
        "salary_slip_uploaded": False
    }
    
    print(run_master_agent(USER_DATA))