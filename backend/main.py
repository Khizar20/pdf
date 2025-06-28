from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from bson import ObjectId
from dotenv import load_dotenv
from io import BytesIO
from pypdf import PdfReader
import requests
from fastapi.responses import RedirectResponse
# Import StaticFiles
from fastapi.staticfiles import StaticFiles


# Load environment variables
# hello000
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
# More robust environment variable handling
try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
except (ValueError, TypeError):
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default fallback value
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# App setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/", StaticFiles(directory="../frontend/public", html=True), name="static")


# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client["chatbot_db"]
users_collection = db["users"]
pdf_collection = db["pdfs"]

# Security setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Helper functions
def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users_collection.find_one({"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/api/signup")
def signup(user: User):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    users_collection.insert_one({"username": user.username, "hashed_password": hashed_password})
    return {"success": True, "message": "User created successfully"}

@app.post("/api/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = users_collection.find_one({"username": form_data.username})
    if not user_data or not verify_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": form_data.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"]}

@app.post("/api/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        file_contents = await file.read()
        pdf_id = pdf_collection.insert_one({
            "filename": file.filename,
            "content": file_contents,
            "uploaded_by": current_user["username"]
        }).inserted_id
        return {"success": True, "message": "PDF uploaded successfully", "pdf_id": str(pdf_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/extract_pdf/{pdf_id}")
async def extract_pdf(pdf_id: str, current_user: dict = Depends(get_current_user)):
    try:
        pdf_data = pdf_collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf_data:
            raise HTTPException(status_code=404, detail="PDF not found")

        pdf_bytes = BytesIO(pdf_data["content"])
        reader = PdfReader(pdf_bytes)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

        return {"filename": pdf_data["filename"], "extracted_text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat_with_pdf/{pdf_id}")
async def chat_with_pdf(pdf_id: str, user_message: str, current_user: dict = Depends(get_current_user)):
    try:
        if not GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="Groq API key is missing. Set it in the .env file.")

        pdf_data = pdf_collection.find_one({"_id": ObjectId(pdf_id)})
        if not pdf_data:
            raise HTTPException(status_code=404, detail="PDF not found in database.")

        pdf_bytes = BytesIO(pdf_data["content"])
        reader = PdfReader(pdf_bytes)

        extracted_text = "\n".join([reader.pages[i].extract_text() for i in range(min(5, len(reader.pages))) if reader.pages[i].extract_text()])

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Extracted text is empty. The PDF might be scanned images.")

        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are an AI assistant that helps summarize and explain PDF content."},
                {"role": "user", "content": f"PDF Content:\n{extracted_text}\n\nUser Question: {user_message}"}
            ],
            "temperature": 0.7
        }

        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        groq_reply = response.json()["choices"][0]["message"]["content"]
        return {"success": True, "message": groq_reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Redirect to chatbot page after login
#@app.get("/")
#def redirect_to_chatbot():
    #return RedirectResponse(url="/index.html")
# Either remove this entirely or change to:
@app.get("/api")
def root():
    return {"message": "API is running"}
