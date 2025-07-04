from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, Request
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from models.schema import Login, QuestionRequest
from services.qa_service import QAService
from services.document_service import DocumentService
from utils.security import create_access_token, verify_token
from utils.sanitizer import sanitize_input


class RouteHandler:
    def __init__(self, document_service: DocumentService, qa_service: QAService, api_server: "APIServer"):
        self.document_service = document_service
        self.qa_service = qa_service
        self.api_server = api_server
        self.app = api_server.app

    @staticmethod
    def verify_token(token: str):
        return verify_token(token)
    
    def configure_routes(self) -> None:
        """Configure FastAPI routes for login, upload files and qa"""

        @self.app.post("/token")
        async def login(request: Login):
            if request.username == "admin" and request.password == "secret":
                return {"access_token": create_access_token({"sub": request.username}),
                        "token_type": "bearer"}
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail="Invalid credentials")

        @self.app.post("/upload")
        @self.api_server.limiter.limit("5/minute")
        async def upload_files(request: Request, files: List[UploadFile] = File(...), token: str = Depends(self.api_server.oauth2_scheme)):
            verify_token(token)
            document_service = DocumentService()
            results = []
            for file in files:
                if file.filename is None:
                    continue
                elif not file.filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                        detail="Unsupported file type")
                content = await file.read()
                result = document_service.process_document(file.filename, content)
                results.append({"filename": file.filename, "extracted_text": result})
            return {"results": results}

        @self.app.post("/ask")
        @self.api_server.limiter.limit("10/minute")
        async def ask_question(request: Request, request_body: QuestionRequest, token: str = Depends(self.api_server.oauth2_scheme)):
            verify_token(token)
            sanitized_question = sanitize_input(request_body.question)
            qa_service = QAService()
            answer, entities = qa_service.answer_question(sanitized_question)
            return {"question": sanitized_question, "answer": answer, "entities": entities}

class APIServer:
    
    def __init__(self):
        self.app = FastAPI()
        self.limiter = Limiter(key_func=get_remote_address)
        self.document_service = DocumentService()
        self.qa_service = QAService()
        self.route_handler = RouteHandler(self.document_service, self.qa_service, self)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def _setup_limiter(self):
        """Set up limiter and exception handler for rate limiting."""
        self.app.state.limiter = self.limiter
        self.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

    def get_app(self) -> FastAPI:
        return self.app

app = APIServer().get_app()
