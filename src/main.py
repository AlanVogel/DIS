from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status, Request
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from models.schema import Login, QuestionRequest
from services.qa_service import QAService
from services.document_service import DocumentService
from services.rag_service import RAGService
from services.redis_service import RedisService
from utils.security import create_access_token, verify_token
from utils.sanitizer import sanitize_input


class RouteHandler:
    """Handles routing configuration for the FastAPI application.

    Manages the definition and setup of API endpoints for authentication,
    file upload, and question answering.

    Attributes:
        document_service (DocumentService): Service for document processing.
        qa_service (QAService): Service for question answering.
        api_server (APIServer): Reference to the API server instance.
        app (FastAPI): FastAPI application instance.
        oauth2_scheme (OAuth2PasswordBearer): OAuth2 scheme for token-based auth.

    """
    def __init__(self, document_service: DocumentService, qa_service: QAService, api_server: "APIServer"):
        """Initialize RouteHandler with required services and server.

        Args:
            document_service (DocumentService): Document processing service.
            qa_service (QAService): Question answering service.
            api_server (APIServer): API server instance.
        """
        self.document_service = document_service
        self.qa_service = qa_service
        self.api_server = api_server
        self.app = api_server.app
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        self.configure_routes()

    @staticmethod
    def verify_token(token: str):
        """Verify the authenticity of a JWT token.

        Args:
            token (str): JWT token to verify.

        Returns:
            dict: Decoded payload if valid.

        Raises:
            HTTPException: If token verification fails.
        """
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
        async def upload_files(request: Request, files: List[UploadFile] = File(...), token: str = Depends(self.oauth2_scheme)):
            verify_token(token)
            results = []
            for file in files:
                if file.filename is None:
                    continue
                elif not file.filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                        detail="Unsupported file type")
                content = await file.read()
                result = self.document_service.process_document(file.filename, content)
                results.append({"filename": file.filename, "extracted_text": result})
            return {"results": results}

        @self.app.post("/ask")
        @self.api_server.limiter.limit("10/minute")
        async def ask_question(request: Request, request_body: QuestionRequest, token: str = Depends(self.oauth2_scheme)):
            verify_token(token)
            sanitized_question = sanitize_input(request_body.question)
            answer, entities = self.qa_service.answer_question(sanitized_question)
            return {"question": sanitized_question, "answer": answer, "entities": entities}

class APIServer:
    """Main server class for setting up the FastAPI application.

    Configures services, routes, and rate limiting for the API.

    Attributes:
        app (FastAPI): FastAPI application instance.
        limiter (Limiter): Rate limiter instance.
        redis_service (RedisService): Redis connection service.
        rag_service (RAGService): Retrieval-Augmented Generation service.
        document_service (DocumentService): Document processing service.
        qa_service (QAService): Question answering service.
        route_handler (RouteHandler): Route configuration handler.

    """
    def __init__(self):
        """Initialize APIServer with all required services and configurations."""
        self.app = FastAPI()
        self.limiter = Limiter(key_func=get_remote_address)
        self.redis_service = RedisService()
        self.rag_service = RAGService(redis_service=self.redis_service)
        self.document_service = DocumentService(redis_service=self.redis_service, rag_service=self.rag_service)
        self.qa_service = QAService(rag_service=self.rag_service)
        self.route_handler = RouteHandler(self.document_service, self.qa_service, self)
        self._setup_limiter()

    def _setup_limiter(self):
        """Set up limiter and exception handler for rate limiting."""
        self.app.state.limiter = self.limiter
        self.app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance.

        Returns:
            FastAPI: Configured application instance.
        """
        return self.app

app = APIServer().get_app()
