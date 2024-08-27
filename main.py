from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = FastAPI()

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('./model')
model = BertForSequenceClassification.from_pretrained('./model')

class PredictRequest(BaseModel):
    texts: list[str]

@app.post("/predict")
async def predict(request: PredictRequest):
    texts = request.texts
    inputs = tokenizer(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
        pred_label = []
        for i in predictions:
            pred_label.append(model.config.id2label[i.item()])
    
    return {"predictions": pred_label}

