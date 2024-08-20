import os
import openai
import psycopg2
from PyPDF2 import PdfFileReader

# Configuración de OpenAI
openai.api_key = '<YOUR_OPENAI_API_KEY>'

# Configuración de Supabase
supabase_url = '<YOUR_SUPABASE_URL>'
supabase_key = '<YOUR_SUPABASE_KEY>'
conn = psycopg2.connect(supabase_url, sslmode='require')

def get_documents(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'rb') as file:
                reader = PdfFileReader(file)
                text = ''
                for page_num in range(reader.numPages):
                    page = reader.getPage(page_num)
                    text += page.extract_text()
                documents.append(text)
    return documents

def generate_embeddings():
    documents = get_documents('')
    
    for document in documents:
        input_text = document.replace('\n', ' ')
        
        response = openai.Embedding.create(
            model='text-embedding-ada-002',
            input=input_text
        )
        
        embedding = response['data'][0]['embedding']
        
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
                (document, embedding)
            )
        conn.commit()

if __name__ == '__main__':
    generate_embeddings()
