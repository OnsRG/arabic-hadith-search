# Modern Arabic Hadith Retrieval — a semantic search approach

This project is a **modern Hadith retrieval engine** designed to improve search quality for Arabic text.  
It combines **lexical retrieval** (BM25) with **semantic retrieval** (ColBERT) to handle nuanced Arabic queries and return highly relevant Hadith passages.

---

## 🚀 Features
- **Lexical Search**: Uses BM25 for fast keyword-based retrieval.  
- **Semantic Search**: Leverages ColBERT and Ragatouille for deep contextual understanding of Arabic text.  
- **Hybrid Ranking**: Combines lexical and semantic results to maximize accuracy.  
- **Interactive UI**: Powered by Streamlit for an easy-to-use interface.  

---
## Project structure
```bash
modern-arabic-hadith-retrieval/
│── books_cleaned_structured/ # Contains cleaned Hadith books (diacritics removed, normalized text, structured with metadata like chapters & references)
│── books_with_matn/ # Similar to books_cleaned_structured, but with matn extraction applied — isolates the main Hadith content from isnād.
│── hadith_books/ # Raw/original Hadith data
│── app3.py # Main Streamlit app (UI for search)
│── data_loader.py # Loads and prepares the Hadith corpus from preprocessed JSON files.
│── indexation.py # Builds the RAG index (books_full) with text + metadata for hybrid search.
│── search_engine.py # Defines the HadithSearchSystem class:
                     # Semantic Search: Uses ColBERT (via RAGatouille) to retrieve contextually relevant Hadiths.
                     # Lexical Search: Uses BM25 to perform keyword-based search.
                     # Hybrid Search: Combines both approaches — first retrieves candidates with BM25, then reranks them semantically with ColBERT for maximum accuracy.
│── phase1_explore_data.ipynb # Data exploration and preprocessing + baseline retrieval experiments.
│── requirements.txt # Python dependencies
│── README.md # Project documentation
│── .gitignore # Ignored files (indexes)
```
## 🛠 Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/OnsRG/arabic-hadith-retrieval.git
cd arabic-hadith-retrieval
pip install -r requirements.txt
```
## ▶️ Usage
Run the Streamlit app:
```bash
streamlit run app3.py
```
Then open http://localhost:8501 in your browser.

This is an example of what you will see when using the app:

![App Screenshot](app1screenshot.png)

## 📂 Indexes
`books_full` indexes are not included in this repository due to size limits.  
You have to : 
- Build your own by running `indexation.py` on your Hadith collection.

## 🤝 Contributing

Contributions are welcome!
If you’d like to add features, improve code, or optimize indexing, please open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License — free to use and modify.

---
✨ Built with ❤️ during my Summer Internship to make Arabic Hadith retrieval smarter and more accessible.