
import random

class SimpleRetriever:
    def __init__(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.documents = [line.strip() for line in f if line.strip()]

    def retrieve(self, query, k=2):
        # Simple keyword matching
        scores = []
        query_terms = query.lower().split()
        for doc in self.documents:
            score = sum(1 for term in query_terms if term in doc.lower())
            scores.append((doc, score))
        
        # Sort by score and return top k
        scores.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scores[:k]]

class SimpleGenerator:
    def generate(self, context, query):
        # Mock LLM generation
        return f"Based on the context '{context}', here is the answer to '{query}'."

class RAGPipeline:
    def __init__(self, data_path):
        self.retriever = SimpleRetriever(data_path)
        self.generator = SimpleGenerator()

    def query(self, question):
        docs = self.retriever.retrieve(question)
        context = " ".join(docs)
        answer = self.generator.generate(context, question)
        return {
            "question": question,
            "context": context,
            "answer": answer
        }
