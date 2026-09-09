# import os
# import sys
# from pathlib import Path

# # Add project root to sys.path
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# # 1. Critical Windows fixes: prevent OpenMP/Tokenizer multithreading buffer crashes
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"

# import logging
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from backend.core.config import (
#     ALLOWED_ORIGINS, 
#     APP_DESCRIPTION, 
#     APP_TITLE, 
#     APP_VERSION, 
#     SPACY_MODEL_PRIMARY, 
#     SPACY_MODEL_SECONDARY, 
#     SENTENCE_TRANSFORMER_MODEL
# )
# from backend.api.routes import router

# logger = logging.getLogger('ats_resume_scorer')


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info('Starting ATS Resume Analyzer API...')

#     logger.info(f'Loading spaCy NLP model: {SPACY_MODEL_PRIMARY}')
#     import spacy
#     try:
#         app.state.nlp = spacy.load(SPACY_MODEL_PRIMARY)
#         logger.info(f'Loaded {SPACY_MODEL_PRIMARY}')
#     except OSError:
#         logger.warning(f'{SPACY_MODEL_PRIMARY} not found — falling back to {SPACY_MODEL_SECONDARY}')
#         app.state.nlp = spacy.load(SPACY_MODEL_SECONDARY)
#         logger.info(f'Loaded {SPACY_MODEL_SECONDARY} (fallback)')

#     logger.info(f'Loading SentenceTransformer: {SENTENCE_TRANSFORMER_MODEL}')
#     from sentence_transformers import SentenceTransformer
#     app.state.embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL)
#     logger.info(f'Loaded {SENTENCE_TRANSFORMER_MODEL}')

#     logger.info('All models loaded. API is ready to serve requests.')

#     yield

#     logger.info('Shutting down the API.')


# app = FastAPI(
#     title=APP_TITLE, 
#     description=APP_DESCRIPTION, 
#     version=APP_VERSION, 
#     lifespan=lifespan,
#     docs_url='/docs',
#     redoc_url='/redoc'
# )

# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins=ALLOWED_ORIGINS,
#     allow_credentials=True, 
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

# app.include_router(router)


# @app.get('/')
# async def root():
#     return {
#         'name': 'ATS Resume Analyzer API',
#         'version': '2.0.0',
#         'endpoints': {
#             'POST   /api/v1/analyze-resume': 'Analyze a resume',
#             'GET    /api/v1/history':        'Get user history',
#             'DELETE /api/v1/history/:id':    'Delete a history entry',
#             'GET    /api/v1/health':         'Health check',
#             'POST   /api/v1/generate-pdf':   'Generate PDF report from data',
#         },
#     }


# if __name__ == '__main__':
#     import uvicorn
#     # Notice: reload=False to prevent child-process spawn buffer corruption on Windows
#     uvicorn.run(
#         'backend.main:app',
#         host='127.0.0.1',
#         port=8000,
#         reload=False
#     )




# import os
# import sys
# from pathlib import Path
# import torch

# # Add project root to sys.path
# sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# # 1. Critical memory & thread controls to prevent OOM on 512MB RAM instances
# torch.set_num_threads(1)
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# os.environ["TOKENIZERS_PARALLELISM"] = "false"
# os.environ["OMP_NUM_THREADS"] = "1"
# os.environ["MKL_NUM_THREADS"] = "1"

# import logging
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from backend.core.config import (
#     ALLOWED_ORIGINS, 
#     APP_DESCRIPTION, 
#     APP_TITLE, 
#     APP_VERSION, 
#     SPACY_MODEL_PRIMARY, 
#     SPACY_MODEL_SECONDARY, 
#     SENTENCE_TRANSFORMER_MODEL
# )
# from backend.api.routes import router

# logger = logging.getLogger('ats_resume_scorer')


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info('Starting ATS Resume Analyzer API...')

#     # Load lightweight spaCy model
#     logger.info(f'Loading spaCy NLP model: {SPACY_MODEL_PRIMARY}')
#     import spacy
#     try:
#         app.state.nlp = spacy.load(SPACY_MODEL_PRIMARY)
#         logger.info(f'Loaded {SPACY_MODEL_PRIMARY}')
#     except OSError:
#         logger.warning(f'{SPACY_MODEL_PRIMARY} not found — falling back to {SPACY_MODEL_SECONDARY}')
#         app.state.nlp = spacy.load(SPACY_MODEL_SECONDARY)
#         logger.info(f'Loaded {SPACY_MODEL_SECONDARY} (fallback)')

#     # Load SentenceTransformer with single thread on CPU
#     logger.info(f'Loading SentenceTransformer: {SENTENCE_TRANSFORMER_MODEL}')
#     from sentence_transformers import SentenceTransformer
#     with torch.no_grad():
#         app.state.embedder = SentenceTransformer(SENTENCE_TRANSFORMER_MODEL, device="cpu")
#     logger.info(f'Loaded {SENTENCE_TRANSFORMER_MODEL}')

#     logger.info('All models loaded. API is ready to serve requests.')

#     yield

#     logger.info('Shutting down the API.')


# app = FastAPI(
#     title=APP_TITLE, 
#     description=APP_DESCRIPTION, 
#     version=APP_VERSION, 
#     lifespan=lifespan,
#     docs_url='/docs',
#     redoc_url='/redoc'
# )

# app.add_middleware(
#     CORSMiddleware, 
#     allow_origins=["*"],  # Ensures Streamlit Cloud requests are not blocked
#     allow_credentials=True, 
#     allow_methods=['*'],
#     allow_headers=['*'],
# )

# app.include_router(router)


# @app.get('/')
# async def root():
#     return {
#         'name': 'ATS Resume Analyzer API',
#         'version': '2.0.0',
#         'endpoints': {
#             'POST   /api/v1/analyze-resume': 'Analyze a resume',
#             'GET    /api/v1/history':        'Get user history',
#             'DELETE /api/v1/history/:id':    'Delete a history entry',
#             'GET    /api/v1/health':         'Health check',
#             'POST   /api/v1/generate-pdf':   'Generate PDF report from data',
#         },
#     }


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(
#         'backend.main:app',
#         host='0.0.0.0',
#         port=int(os.getenv("PORT", 8000)),
#         reload=False
#     )







import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    yield
    logger.info('Shutting down API...')


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

app.include_router(router)


@app.get('/')
async def root():
    return {
        'name': 'ATS Resume Analyzer API',
        'version': '2.0.0',
        'status': 'online'
    }


@app.get('/api/v1/health')
async def health():
    return {'status': 'healthy'}


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run('backend.main:app', host='0.0.0.0', port=port, reload=False)