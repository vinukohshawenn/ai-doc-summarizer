from fastapi import FastAPI, Request, Form, Depends, UploadFile, File, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import io
from pypdf import PdfReader
from google import genai 

from database import SessionLocal
from models import User

# --- LLM CONFIG ---
client = genai.Client(api_key="enter_your_api_key")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- SERVER MEMORY ---
active_docs = {}      
chat_histories = {}   

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # UPDATED SYNTAX HERE
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    # UPDATED SYNTAX HERE
    return templates.TemplateResponse(request=request, name="register.html")

@app.post("/register", response_class=HTMLResponse)
def create_user(
    request: Request, 
    username: str = Form(...), 
    email: str = Form(...),
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        (User.user_name == username) | (User.user_email_id == email)
    ).first()
    
    if existing_user:
        # UPDATED SYNTAX HERE
        return templates.TemplateResponse(
            request=request, 
            name="register.html", 
            context={"error": "Username or Email already taken!"}
        )

    new_user = User(
        user_name=username,
        user_email_id=email,
        user_status="active",
        password_hash=password
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/", status_code=302)

@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request, 
    response: Response, 
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_name == username).first()

    if not user or user.user_status != 'active' or user.password_hash != password:
        # UPDATED SYNTAX HERE
        return templates.TemplateResponse(
            request=request, 
            name="login.html", 
            context={"error": "Invalid credentials."}
        )

    redirect = RedirectResponse(url="/dashboard", status_code=302)
    redirect.set_cookie(key="session_user", value=username)
    return redirect

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    session_user = request.cookies.get("session_user")
    if not session_user:
        return RedirectResponse(url="/", status_code=302)
    
    has_doc = session_user in active_docs
    history = chat_histories.get(session_user, [])
    
    # UPDATED SYNTAX HERE
    return templates.TemplateResponse(
        request=request, 
        name="dashboard.html", 
        context={
            "has_doc": has_doc,
            "chat_history": history,
            "username": session_user
        }
    )

@app.post("/upload", response_class=HTMLResponse)
async def upload_document(request: Request, file: UploadFile = File(...)):
    session_user = request.cookies.get("session_user")
    if not session_user:
        return RedirectResponse(url="/", status_code=302)

    try:
        content = await file.read()
        text_content = ""

        if file.filename.lower().endswith(".pdf"):
            pdf_reader = PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
        else:
            text_content = content.decode("utf-8")

        active_docs[session_user] = text_content
        chat_histories[session_user] = [
            {"role": "ai", "text": f"Document '{file.filename}' loaded! What would you like to know about it?"}
        ]

    except Exception as e:
        print(f"Upload error: {e}")

    return RedirectResponse(url="/dashboard", status_code=302)

@app.post("/ask", response_class=HTMLResponse)
def ask_question(request: Request, question: str = Form(...)):
    session_user = request.cookies.get("session_user")
    if not session_user or session_user not in active_docs:
        return RedirectResponse(url="/dashboard", status_code=302)

    document_text = active_docs[session_user]
    chat_histories[session_user].append({"role": "user", "text": question})

    prompt = f"Here is the reference document:\n\n{document_text}\n\nBased ONLY on the document above, answer this question: {question}"

    try:
        llm_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        answer = llm_response.text
    except Exception as e:
        answer = f"Error: {str(e)}"

    chat_histories[session_user].append({"role": "ai", "text": answer})
    return RedirectResponse(url="/dashboard", status_code=302)

@app.get("/logout")
def logout():
    redirect = RedirectResponse(url="/", status_code=302)
    redirect.delete_cookie("session_user")
    return redirect

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
