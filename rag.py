import os
from typing import List
from urllib import request
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA 
from langchain import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
import time

#OLLAMA_API_URL = "http://localhost:11434/embedding"


DOC_FOLDER = "/home/moksha/project2024/downloded_file"



#CHROMA_PATH = "/mnt/c/Users/Welcome/OneDrive/Desktop/chroma_db"

pdf_files = [os.path.join(DOC_FOLDER, f) for f in os.listdir(DOC_FOLDER) if f.endswith('.pdf')]

all_pages = []
for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    pages = loader.load()
    all_pages.extend(pages)

print(f"First page of the document: {all_pages[0]}")

print("DONE")
print("***************************************************")
# for page in pages:
#     print(page)


# split the doc into smaller chunks i.e. chunk_size=500
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(all_pages)

print(f"First page chunks of the document: {chunks[0]}")
#print(chunks)



used_llm = VertexAI(
    model_name="gemini-1.5-pro",
    max_output_tokens=2048,
    temperature=0.1,
    verbose=False,
)

def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time() # type: ignore
        yield       # Request making happens here
        after = time.time() # type: ignore
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time) # type: ignore

class CustomVertexAIEmbeddings(VertexAIEmbeddings):
    requests_per_minute: int
    num_instances_per_batch: int
    model_name: str
    

    def embed_documents(
        self, texts: List[str], batch_size: int = 0
    ) -> List[List[float]]:
        
        # setup rate limiter
        limiter = rate_limit(self.requests_per_minute) # type: ignore
        
        results = []
        
        docs = list(texts)
        
        while docs:
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch : ]
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)
        
        return [r.values for r in results]

embeddings = CustomVertexAIEmbeddings(
    requests_per_minute = 100,
    num_instances_per_batch = 5,
    model_name = "textembedding-gecko@latest"
)

# Extract plain text strings from chunks
text_chunks = [chunk.page_content for chunk in chunks]

# Pass the plain text strings to FAISS
db = FAISS.from_texts(text_chunks, embeddings)


# Initialize the retriever
retriever = db.as_retriever( 
    search_type="similarity",       # Other option is "mmr"
    search_kwargs={"k": 5}
)

prompt_RAG = (
    "You are a RAG model designed to answer queries using the content from the provided document. "
    "If the document contains the answer, provide a precise response based on it. "
    "If the answer isn't in the document, respond with: 'Context not found.'"
)

prompt_RAG_template = PromptTemplate(
    template=prompt_RAG,
    input_variables=["context", "question"]  # Make sure "context" matches this name throughout
)

# Create the LLMChain using the prompt template
llm_chain = LLMChain(
    llm=used_llm,
    prompt=prompt_RAG_template
)

# Set up the RetrievalQA chain using the StuffDocumentsChain
qa_chain = RetrievalQA.from_llm(
    llm=used_llm,
    retriever=retriever,
    return_source_documents=True
)

user_question = "what is the role of CPU"
results = qa_chain.invoke(input={"query": user_question})
print(results["result"])