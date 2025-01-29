from transformers import AutoModel

model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)

def embedded_vector(model, text):
    embedding = model.encode([text])
    return embedding[0].tolist()

