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

## 📂 Indexes
FAISS indexes are not included in this repository due to size limits.  
You have to : 
- Build your own by running `indexation.py` on your Hadith collection.

## 🤝 Contributing

Contributions are welcome!
If you’d like to add features, improve code, or optimize indexing, please open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License — free to use and modify.

✨ Built with ❤️ during my Summer Internship to make Arabic Hadith retrieval smarter and more accessible.