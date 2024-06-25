from langchain.vectorstores import FAISS

db= FAISS.from_documents(documents= pages,embedding= #embedding model there)
                         
db.save_local(#path on computer to save database)
    

###################### LOAD DATABASE BACK############################

vectorStore= FAISS.load_local(folder_path, embeddings)

retriever= vectorStore.as_retriever(search_type="similarity", search_kwargs={'k':3})