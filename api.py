# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
# Import your new brain
import main 

app = FastAPI(title="EY Agentic Bot API")

# --- Data Model ---
class UserQuery(BaseModel):
    name: str  # "Alex Johnson" or "Neha R"
    query: str
    requested_amount: int
    income: int
    salary_slip_uploaded: bool = False

# --- Chat Endpoint ---
@app.post("/chat")
async def handle_chat_request(user_data: UserQuery):
    print(f"[API] Request: {user_data.name} asking for ${user_data.requested_amount}")
    
    # Convert Pydantic model to dict for the main script
    data_dict = user_data.dict()
    
    try:
        # Call the Master Agent
        final_report = main.run_master_agent(data_dict)
        
        # Check if a sanction letter was created
        has_file = False
        if "Sanction_Letter.txt" in os.listdir("."):
             if "SUCCESS" in final_report:
                 has_file = True

        return {
            "response": final_report,
            "has_file": has_file
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"response": f"System Error: {str(e)}", "has_file": False}

# --- File Download Endpoint ---
from fastapi.responses import FileResponse
@app.get("/download-sanction")
def download_file():
    file_path = "Sanction_Letter.txt"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename="EY_Sanction_Letter.pdf.txt", media_type="text/plain")
    return {"error": "File not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)