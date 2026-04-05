from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import RetrievalQA
from src.vectorstore import load_vectorstore
from src.embeddings import get_embedding_model
from src.llm import get_llm

def query_rag(question: str):
    embedding_model = get_embedding_model()
    vectorstore = load_vectorstore(embedding_model)
    
    if not vectorstore:
        return {"answer": "No documents indexed. Please ingest a PDF first.", "sources": []}
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based ONLY on the following context from automotive service manuals:

    CONTEXT:
    {context}

    QUESTION: {question}

    Provide a clear, accurate answer with references to specific chunks (text/table/image).
    """)
    
    chain = create_stuff_documents_chain(llm, prompt)
    
    result = chain.invoke({"input_documents": retriever.get_relevant_documents(question), "question": question})
    
    # Extract sources
    sources = []
    docs = retriever.get_relevant_documents(question)
    for i, doc in enumerate(docs):
        sources.append({
            "content": doc.page_content[:200] + "...",
            "type": doc.metadata.get("type", "text"),
            "source": doc.metadata.get("source", "unknown")
        })
    
    return {
        "answer": result,
        "sources": sources,
        "total_chunks": len(sources)
    }