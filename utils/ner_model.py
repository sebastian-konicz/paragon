from transformers import pipeline

# Załaduj model NER
ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

def extract_products_from_text(text):
    return ner_model(text)