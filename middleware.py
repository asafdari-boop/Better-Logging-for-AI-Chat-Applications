from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from logger import get_context_middleware

allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost:4000",
]

middleware = [
    # Add context middleware first so it's available for all requests
    get_context_middleware(),
    Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
]