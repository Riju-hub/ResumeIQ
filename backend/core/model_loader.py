import os
import torch
import spacy
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger("ats_resume_scorer")

# Force PyTorch and tokenizers into low-memory single-thread mode
torch.set_num_threads(1)
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

_NLP_INSTANCE = None
_EMBEDDER_INSTANCE = None

def get_spacy_model():
    global _NLP_INSTANCE
    if _NLP_INSTANCE is None:
        logger.info("Initializing spaCy model (en_core_web_sm)...")
        try:
            _NLP_INSTANCE = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("en_core_web_sm not found, trying fallback...")
            _NLP_INSTANCE = spacy.load("en_core_web_sm")
    return _NLP_INSTANCE

def get_sentence_embedder():
    global _EMBEDDER_INSTANCE
    if _EMBEDDER_INSTANCE is None:
        logger.info("Initializing SentenceTransformer (all-MiniLM-L6-v2) on CPU...")
        with torch.no_grad():
            _EMBEDDER_INSTANCE = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
    return _EMBEDDER_INSTANCE