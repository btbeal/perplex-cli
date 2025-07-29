 #!/usr/bin/env python3
"""
Startup script for the Perplexity AI Clone
"""
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ["OPENAI_API_KEY", "SERP_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with these variables or set them in your environment.")
        return False
    
    print("All required environment variables are set!")
    return True

def main():
    print("Starting Perplexity AI Clone...")
    
    if not check_environment():
        return
    
    print("Starting FastAPI server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()