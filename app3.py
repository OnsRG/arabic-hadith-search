import streamlit as st
import streamlit.components.v1 as components
from search_engine import HadithSearchSystem
from data_loader import corpus_all


# Page config
st.set_page_config(page_title="بحث الأحاديث", page_icon="📖", layout="wide")

# RTL and Arabic styling (general page styling)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');

    html, body {
        background-image: url('https://i.imgur.com/6zxCpTE.jpeg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }

    .stApp {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: transparent !important;  /* Default: no overlay */
    }

    /* Dark mode specific styles */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: rgba(0, 0, 0, 0.6) !important;  /* 🔥 Dark overlay only in dark mode */
            color: white;
        }

        h1, h2, h3, h4, h5, h6,
        p, span, div, label {
            color: white !important;
        }

        input, textarea {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
        }

        button {
            background-color: rgba(255, 255, 255, 0.2) !important;
            color: white !important;
        }
    
    }
    </style>
""", unsafe_allow_html=True)


# Title and input
st.title("💫 كنوز الحديث النبوي")



col_query, _ = st.columns([10, 7])  
with col_query:
    query = st.text_input("أدخل استفسارك هنا:", placeholder="مثال: الصدق في القول")

search_button = False
search_mode = "اختر نوع البحث"


# Container for equal-sized inputs
with st.container():
        col1, col2 = st.columns([1, 1])

with col1:
       search_mode = st.selectbox(
            "اختر نوع البحث:",
            ["اختر نوع البحث", " البحث الدلالي (Semantic)", " البحث اللفظي (Lexical)", " البحث الهجين (Hybrid)"]
            )

with col2:
      k = st.number_input(" عدد النتائج المرغوبة:", min_value=5, max_value=50, value=5, step=1)

# Perfectly centered button
col_left, col_center, col_right = st.columns([6, 1, 6])
with col_center:
     search_button = st.button("🔍 ابحث")

@st.cache_resource(show_spinner="📖 جارٍ تحميل النظام...")
def load_search_system():
    from data_loader import corpus_all  
    return HadithSearchSystem(corpus_all)

search_system = load_search_system()
# Perform search
if search_button and query and search_mode != "اختر نوع البحث":

    with st.spinner("🔍 يتم الآن البحث في الأحاديث..."):

        if search_mode == " البحث الدلالي (Semantic)":
            results = search_system.semantic_search(query, k=k)
        elif search_mode == " البحث اللفظي (Lexical)":
            results = search_system.lexical_search(query, k=k)
        elif search_mode == " البحث الهجين (Hybrid)":
            results = search_system.hybrid_search(query, k1=100, k2=k)
        else:
            results = []

        # Simulate a unified metadata list for both semantic and lexical results
        metadata = []
        for result in results:
            hadith = result.get("hadith", {})

            document_metadata = {
                "hadith_id": hadith.get("id", "؟"),
                "chapter_number": hadith.get("chapter_number", "؟"),
                "chapter": hadith.get("chapter_title", "—"),
                "book": hadith.get("source", "غير معروف"),
                "cleaned_arabic": hadith.get("cleaned_arabic", hadith.get("text", "—")),
                "text": hadith.get("text", "—"),
                "english": hadith.get("english", ""),
                "reference": hadith.get("reference", ""),
            }

            metadata.append({
                "text": document_metadata["cleaned_arabic"],
                "metadata": document_metadata
            })


        st.markdown("### 📜 النتائج:")

        
        # Construct HTML with grid layout
        cards_html = """
        <style>
            .grid-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                padding: 20px;
                direction: rtl;
            }

            .hadith-card {
                background-color: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                padding: 1.5rem;
                border: 2px solid #ddd;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                font-family: 'Cairo', sans-serif;
            }

            .hadith-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            }

            .hadith-card::before {
                content: "﷽";
                display: block;
                font-size: 2rem;
                text-align: center;
                color: #00897b;
                margin-bottom: 1rem;
                font-family: 'Amiri', serif;
            }

            .hadith-meta {
                margin-top: 1rem;
                color: #666;
                font-size: 0.9rem;
            }

            .highlight {
                background-color: #fff3b0;
                padding: 2px;
                border-radius: 4px;
            }

            @media (prefers-color-scheme: dark) {
                .hadith-card {
                    background-color: #1e1e1e;
                    color: #eee;
                }
                .hadith-meta {
                    color: #bbb;
                }
            }
        </style>
        <div class="grid-container">
        """

        for hadith in metadata:
            meta = hadith.get("metadata", {})
            book = meta.get("book", "غير معروف")
            chapter_en = meta.get("chapter", "—")
            chapter= chapter_en.split(":")[-1].strip()
            number = meta.get("hadith_id", "؟")
            chapter_number = meta.get("chapter_number", "؟")
            text = hadith["text"]

            cards_html += f"""
                <div class="hadith-card">
                    <p style="font-size: 1.2rem; line-height: 2;">{text}</p>
                    <div class="hadith-meta">
                        📘 <b>{book}</b> |  <b>رقم الحديث: {number}</b><br>
                        🧩 <b>الفصل:</b> {chapter} (رقم {chapter_number})<br>
                    </div>
                </div>
            """

        cards_html += "</div>"

        # Display grid of hadith cards
        components.html(cards_html, height=1000, scrolling=True)