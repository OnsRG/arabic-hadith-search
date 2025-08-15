import os
import json
from ragatouille import RAGPretrainedModel

RAG = RAGPretrainedModel.from_pretrained("akhooli/Arabic-ColBERT-100K")


cleaned_books=["riyad_assalihin_with_matn.json","bukhari_with_matn.json","muslim_with_matn.json","abudawud_with_matn.json","tirmidhi_with_matn.json","nasai_with_matn.json","malik_with_matn.json","ahmed_with_matn.json"]

# Combined corpus
corpus_all = []

# Loop through each file
for file_name in cleaned_books:
    file_path = os.path.join('books_with_matn', file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        book_data = json.load(f)

    for entry in book_data:
        if entry.get("extracted_arabic"):
            corpus_all.append({
                "id": str(entry.get("id")),
                "chapter_number": entry.get("chapter_number", None),
                "chapter_title": entry.get("chapter_title", "—"),
                "cleaned_arabic": entry.get("cleaned_arabic", ""),
                "english": entry.get("english", ""),
                "text": entry.get("extracted_arabic", ""),  # used for indexing
                "source": entry.get("source", "unknown source"),
                "reference": entry.get("reference", "")
            })
        

for h in corpus_all:
    h['id'] = str(h['id'])

# Indexing configuration
index_name = "books_full"
# batch_size = 300
total = len(corpus_all)

# Extract text and metadata from updated corpus
texts = [doc["text"] for doc in corpus_all]  
metadatas = [
    {
        "id": doc["id"],
        "chapter_title": doc["chapter_title"],
        "chapter_number": doc.get("chapter_number", ""),
        "source": doc["source"],
        "reference": doc["reference"],
        "english": doc["english"],
        "cleaned_arabic": doc["cleaned_arabic"]
    }
    for doc in corpus_all
]

# for i in range(0, total, batch_size):
text_batch = texts #[i:i + batch_size]
metadata_batch = metadatas #[i:i + batch_size]
RAG.index(collection=texts, document_metadatas=metadatas, index_name=index_name)
    # print(f"✅ Indexed {i + len(text_batch)} / {total} hadiths")
