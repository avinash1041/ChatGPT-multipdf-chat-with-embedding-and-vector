import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter   #use for chunks
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings  #using for embeddings
from langchain.vectorstores import FAISS  #like a local database not used servers to store vectors
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css,bot_template,user_template


def get_pdf_text(pdf_docs):  #4 pdf
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)   #pages read
        for page in pdf_reader.pages:
            text += page.extract_text()   
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000, #1000 characters
        chunk_overlap = 200, #200 charachter of previous chunk and continue to sentence
        length_function = len
    )
    chunks = text_splitter.split_text(text)   #return list of chunk 1000 charchacter types
    return chunks


#openai embedding is very fact but very costly
def get_vectorestore(text_chunks):   
    embeddings = OpenAIEmbeddings()  #very fast even 8 pages in 4sec
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")  #very slow but free, 8 pages 35min
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorestore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever=vectorestore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question':user_question})
    # st.write(response)
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
        
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents: ")
    if user_question:
        handle_userinput(user_question)
    
    # st.write(user_template.replace("{{MSG}}", "Hello robot"), unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}", "Hello avinash"), unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                #get pdf text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)
                #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)
                #2 type of way 1]openai embedding is 2]huggingface free model
                #create vector store
                vectorestore = get_vectorestore(text_chunks)
                # st.write(vectorestore)
                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorestore)
        

if __name__ == "__main__":
    main()