from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize
import nltk
import numpy as np
from ragatouille import RAGPretrainedModel

RAG = RAGPretrainedModel.from_pretrained("akhooli/Arabic-ColBERT-100K")

nltk.download('punkt')

class HadithSearchSystem:
    def __init__(self, hadiths, index_name="books_full"):
        self.hadiths = hadiths
        
        #  Load semantic model + index
        index_path = f".ragatouille/colbert/indexes/{index_name}"
        self.rag_model = RAG.from_index(index_path)

        #  Prepare BM25
        tokenized_corpus = [word_tokenize(hadith['text'].lower()) for hadith in hadiths]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def semantic_search(self, query, k=5):
        results = self.rag_model.search(query, k=k)
    
        #print("Semantic search results:", results)
        if results is None:
            return []

        # RAG returns: list of dicts with {'document_id', 'text', 'metadata', 'score'}
        hits = []
        for result in results:
            matching_hadith = result['document_metadata']
            if matching_hadith:
                hits.append({
                    'hadith': matching_hadith,
                    'score': result['score']
                })
        return hits

    def lexical_search(self, query, k=5):
        tokenized_query = word_tokenize(query.lower())
        doc_scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(doc_scores)[-k:][::-1]
        return [{
            'hadith': self.hadiths[idx],
            'score': doc_scores[idx]
        } for idx in top_indices]

    def hybrid_search(self, query, k1=100, k2=5):
        # Step 1: Lexical search
        lexical_results = self.lexical_search(query, k=k1)

        # Step 2: Extract hadiths and their texts
        hadiths = [res['hadith'] for res in lexical_results]
        texts = [h['text'] for h in hadiths]

        # Step 3: Semantic reranking
        reranked_pairs = self.rag_model.rerank(query, texts)

        # Debug print
        print("Reranked pairs:", reranked_pairs)

        # Step 4: Match results back to hadiths
        reranked = []
        for pair in reranked_pairs:
            score = pair['score']
            text = pair['content']  # ✅ use 'content' not 'text'
            for hadith in hadiths:
                if hadith['text'] == text:
                    reranked.append({
                        'hadith': hadith,
                        'score': score
                    })
                    break

        # Step 5: Return top k2
        reranked.sort(key=lambda x: x['score'], reverse=True)
        return reranked[:k2]