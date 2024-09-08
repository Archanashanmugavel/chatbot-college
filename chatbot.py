import os
from pinecone import Pinecone
from dotenv import load_dotenv
import numpy as np
from langchain.llms import HuggingFacePipeline
import base64
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
from transformers import pipeline
import torch 
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import SentenceTransformerEmbeddings 
load_dotenv()
os.environ['CURL_CA_BUNDLE'] = ''
pc = Pinecone(api_key="05d70e05-3fb8-4bcf-a5bf-f86310d29108")
index_name ="chatbot"

device = torch.device('cpu')

checkpoint = "MBZUAI/LaMini-T5-738M"
print(f"Checkpoint path: {checkpoint}")
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelForSeq2SeqLM.from_pretrained(
    checkpoint,
    device_map=device,
    torch_dtype=torch.float32
)
def process_answer(instruction):


    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    index = pc.Index(index_name)
    text = instruction

    text_embed = embeddings.embed_query(text)
    get_response = index.query(
        namespace = "np4",
        vector = text_embed,
        top_k =  5,
        includeMetadata = True

    )

    meta = [ i.metadata['text'] for i in  get_response.matches]
   
    # result = ""
    # for i in get_response.matches :
    #     result = result + " " + i.metadata['text']
    
    pipe = pipeline(
        'text2text-generation',
        model = base_model,
        tokenizer = tokenizer,
        max_length = 256,
        do_sample = True,
        temperature = 0.3,
        top_p= 0.20,
    )
    
    local_llm = HuggingFacePipeline(pipeline=pipe)
    chain = load_qa_chain(local_llm , chain_type="stuff")
    ans = chain.run(input_documents = meta  , question = text)
    print(text)
    print(ans)
    return ans

# print(process_answer("what is depression ? "))
