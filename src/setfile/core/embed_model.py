from pathlib import Path
from transformers import AutoTokenizer, AutoModel
import torch

_tokenizer = None
_gemma_model = None

def load_model(text):
    global _tokenizer, _gemma_model
    
    if _tokenizer is None or _gemma_model is None:
        model_id = Path(__file__).resolve().parent.parent/'gemma-weights'
        _tokenizer = AutoTokenizer.from_pretrained(model_id)
        _gemma_model = AutoModel.from_pretrained(model_id).to(torch.device('cpu'))

    inputs = _tokenizer(text , return_tensors = "pt", padding=True, truncation = True)

    with torch.no_grad():
        outputs = _gemma_model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)

    return embeddings
