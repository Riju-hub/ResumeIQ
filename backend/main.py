import os
import sys
from pathlib import Path

# Fix path resolution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import gc
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Enforce strict single-threaded execution to stay within 512MB RAM
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from backend.core.config import (
    APP_DESCRIPTION, 
    APP_TITLE, 
    APP_VERSION
)
from backend.api.routes import router

logger = logging.getLogger('ats_resume_scorer')


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('ATS Resume Analyzer API starting up...')
    # Garbage collection on startup
    gc.collect()
    yield
    logger.info('Shutting down API...')
    gc.collect()


app = FastAPI(
    title=APP_TITLE, 
    description=APP_DESCRIPTION, 
    version=APP_VERSION, 
    lifespan=lifespan,
    docs_url='/docs',
    redoc_url='/redoc'
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_credentials=True, 
    allow_methods=['*'],
    allow_headers=['*'],
)

# Prefix all API router endpoints under /api/v1
app.include_router(router)


@app.get('/')
async def root():
    return {
        'name': 'ATS Resume Analyzer API',
        'version': APP_VERSION or '2.0.0',
        'status': 'online'
    }


@app.get('/api/v1/health')
async def health():
    return {
        'status': 'healthy',
        'ready': True
    }


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run('backend.main:app', host='0.0.0.0', port=port, reload=False)