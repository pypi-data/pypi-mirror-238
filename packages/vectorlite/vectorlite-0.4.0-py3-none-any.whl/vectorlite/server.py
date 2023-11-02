from fastapi import FastAPI, File, UploadFile
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from .core import VectorLite
import subprocess
import os

app = FastAPI(title="VectorLite API Server",
    description="Lightweight vector database.")
vl = VectorLite()

@app.post("/create/", tags=["Data Operations"], summary="Add data to the database")
async def create(file: UploadFile):
    """Add new data to the VectorLite database."""
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    loader = PyPDFLoader(file.filename)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    vl.create(texts)
    
    os.remove(file.filename)  # Delete the file after loading it into the database

    return {"status": "Data added successfully"}


@app.get("/read_all/", tags=["Data Operations"], summary="Read all data from the database")
async def read_all(max_items: int = None):
    """
    Retrieve all data from the VectorLite database.
    Use the `max_items` query parameter to limit the number of records returned.
    """
    return vl.read_all(max_items)

@app.get("/read/", tags=["Data Operations"], summary="Read data by index")
async def read(idx: int):
    """Retrieve specific data from the VectorLite database using its index."""
    return {"data": vl.read(idx)}

@app.put("/update/", tags=["Data Operations"], summary="Update data by index")
async def update(idx: int, new_data: str):
    """Update a specific data entry in the VectorLite database using its index."""
    vl.update(idx, new_data)
    return {"status": "Data updated successfully"}

@app.delete("/delete/", tags=["Data Operations"], summary="Delete data by index")
async def delete(idx: int):
    """Delete a specific data entry from the VectorLite database using its index."""
    vl.delete(idx)
    return {"status": "Data deleted successfully"}

@app.get("/similarity_search/", tags=["Search"], summary="Find similar entries based on a query")
async def similarity_search(query: str, k: int = 5):
    """
    Search the VectorLite database for entries similar to the provided query.
    Use the `k` query parameter to specify how many top results you want.
    """
    return vl.similarity_search(query, k)

@app.get("/semantic_search/", tags=["Search"], summary="Find semantically similar entries based on a query")
async def semantic_search(query: str, k: int = 5):
    """
    Search the VectorLite database for entries semantically similar to the provided query.
    Use the `k` query parameter to specify how many top results you want.
    """
    return vl.semantic_search(query, k)

def main():
    cmd = ["uvicorn", "vectorlite.server:app", "--host", "0.0.0.0", "--port", "4440", "--reload"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()