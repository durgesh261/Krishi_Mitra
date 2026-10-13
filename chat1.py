import os
import json
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Document:
    """Document representation compatible with LangChain Document interface"""
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"Document(page_content='{self.page_content[:60]}...', metadata={self.metadata})"

class AgriculturalRetriever:
    """Callable retriever compatible with Runnable and standard get_relevant_documents"""
    def __init__(self, vector_store, k=4):
        self.vector_store = vector_store
        self.k = k

    def get_relevant_documents(self, query):
        return self.vector_store.similarity_search(query, k=self.k)

    def invoke(self, query):
        if isinstance(query, dict) and 'question' in query:
            query = query['question']
        return self.get_relevant_documents(str(query))

    def __or__(self, other):
        # Allow pipe syntax like retriever | format_docs
        class ChainedRunnable:
            def __init__(self, step1, step2):
                self.step1 = step1
                self.step2 = step2

            def invoke(self, input_val):
                res1 = self.step1.invoke(input_val)
                return self.step2(res1) if callable(self.step2) else self.step2.invoke(res1)

            def __call__(self, input_val):
                return self.invoke(input_val)

        return ChainedRunnable(self, other)

class FastAgriculturalVectorStore:
    """
    Lightweight, high-performance in-memory TF-IDF vector store for Agricultural Knowledge.
    Bypasses PyTorch, ChromaDB, and SentenceTransformers for instant startup and zero lag.
    """
    def __init__(self, corpus_path="Data/knowledge_corpus.json"):
        self.corpus_path = corpus_path
        self.documents = []
        # Support Unicode characters for Indian regional languages and abbreviations, ignore common English stop words
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            token_pattern=r'(?u)\b\w+\b',
            ngram_range=(1, 2),
            max_features=12000,
            sublinear_tf=True
        )
        self.tfidf_matrix = None
        self._load_corpus()

    def _load_corpus(self):
        chunks = []
        if os.path.exists(self.corpus_path):
            try:
                with open(self.corpus_path, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
            except Exception as e:
                print(f"Error loading corpus: {e}")

        # If empty or file not found, populate standard domain knowledge
        if not chunks:
            try:
                import build_knowledge
                build_knowledge.build_corpus()
                if os.path.exists(self.corpus_path):
                    with open(self.corpus_path, 'r', encoding='utf-8') as f:
                        chunks = json.load(f)
            except Exception:
                pass

        if not chunks:
            chunks = [
                {
                    "title": "PM-KISAN",
                    "text": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN) provides financial support of Rs 6000 per year to eligible farmer families in three 4-monthly installments of Rs 2000 each deposited directly into bank accounts."
                },
                {
                    "title": "Crop Disease Management",
                    "text": "For fungal diseases like leaf spot and blight, spray Mancozeb or Copper Oxychloride at 2.5g/L. For sucking pests like aphids and whiteflies, use Neem oil 1500ppm (5ml/L) or Imidacloprid."
                },
                {
                    "title": "Organic Farming and Soil Health",
                    "text": "Organic farming emphasizes application of well-decomposed FYM (10-12 tons/ha), vermicompost (2-3 tons/ha), biofertilizers like Rhizobium and PSB, and mulching for moisture retention."
                }
            ]

        self.documents = [
            Document(page_content=item.get('text', ''), metadata={'source': item.get('source', ''), 'title': item.get('title', '')})
            for item in chunks if item.get('text', '').strip()
        ]

        corpus_texts = [doc.page_content for doc in self.documents]
        if corpus_texts:
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus_texts)
        print(f"[OK] Agricultural Knowledge Base initialized with {len(self.documents)} entries.")

    def get_max_similarity(self, query):
        """Returns the highest cosine similarity score for the query against the corpus"""
        if not self.documents or self.tfidf_matrix is None:
            return 0.0
        try:
            query_vec = self.vectorizer.transform([str(query)])
            sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            return float(np.max(sims)) if len(sims) > 0 else 0.0
        except Exception:
            return 0.0

    def similarity_search(self, query, k=4, min_score=0.03):
        """
        Returns relevant agricultural documents matching the query.
        Returns empty list if query does not match agricultural corpus.
        """
        if not self.documents or self.tfidf_matrix is None:
            return []
        
        try:
            query_vec = self.vectorizer.transform([str(query)])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            
            top_indices = np.argsort(similarities)[-k:][::-1]
            results = []
            for idx in top_indices:
                if similarities[idx] >= min_score:
                    results.append(self.documents[idx])
            
            return results
        except Exception as e:
            print(f"Similarity search error: {e}")
            return []

    def as_retriever(self, search_kwargs=None):
        k = 4
        if search_kwargs and 'k' in search_kwargs:
            k = search_kwargs['k']
        return AgriculturalRetriever(self, k=k)

# Backward-compatible helper functions
def fetch_website_content(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Exception:
        return ""

def extract_pdf_text(pdf_file):
    try:
        import PyPDF2
        with open(pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += (page.extract_text() or "") + "\n"
        return text
    except Exception:
        return ""

def split_text(text, chunk_size=500, chunk_overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - chunk_overlap)
    return chunks

def initialize_vector_store(contents=None):
    return FastAgriculturalVectorStore()

def initialize_vector_store_persistent(contents=None, persist_directory=None):
    return FastAgriculturalVectorStore()
