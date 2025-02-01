from app.models.llm_manager import get_llm_manager
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={'device': 'cuda'}
        )
        self.resume_vector_store = None  # Separate vector store for resume
        self.jd_vector_store = None      # Separate vector store for job description
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.llm_manager = get_llm_manager()

    async def process_resume(self, file_path: str):
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)
            self.resume_vector_store = FAISS.from_documents(texts, self.embeddings)
            return True
        except Exception as e:
            raise Exception(f"Error processing resume: {str(e)}")

    async def process_job_description(self, text: str):
        try:
            texts = self.text_splitter.create_documents([text])
            self.jd_vector_store = FAISS.from_documents(texts, self.embeddings)
            return True
        except Exception as e:
            raise Exception(f"Error processing job description: {str(e)}")

    def get_resume_context(self, query: str, k: int = 3):
        if not self.resume_vector_store:
            return ""
        try:
            docs = self.resume_vector_store.similarity_search(query, k=k)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            raise Exception(f"Error retrieving resume context: {str(e)}")

    def get_jd_context(self, query: str, k: int = 3):
        if not self.jd_vector_store:
            return ""
        try:
            docs = self.jd_vector_store.similarity_search(query, k=k)
            return "\n".join([doc.page_content for doc in docs])
        except Exception as e:
            raise Exception(f"Error retrieving job description context: {str(e)}")

    async def optimize_resume(self, query: str):
        try:
            resume_context = self.get_resume_context(query)
            jd_context = self.get_jd_context(query)
            
            prompt = f"""[INST] You are a resume optimization assistant. Your task is to improve resume bullet points by comparing them against a job description. You must ONLY respond in the exact format specified below.

            Job Description:
            {jd_context}

            Resume Content:
            {resume_context}

            RESPOND ONLY IN THIS FORMAT:

            ORIGINAL: [copy exact bullet point from resume]
            IMPROVED: [rewritten bullet point]
            EXPLANATION: [1-2 sentences maximum explaining alignment with job]

            ORIGINAL: [next bullet point]
            IMPROVED: [rewritten bullet point]
            EXPLANATION: [1-2 sentences maximum explaining alignment with job]

            [Continue for each relevant bullet point]

            Rules:
            1. Do not include any analysis or thought process
            2. Do not add any additional text or sections
            3. Follow the exact format shown above
            4. Keep explanations to 1-2 sentences maximum
            5. Focus only on relevant bullet points that align with the job description

            [/INST]"""

            response = await self.llm_manager.generate_response(prompt)
            return response
    except Exception as e:
        raise Exception(f"Error optimizing resume: {str(e)}")