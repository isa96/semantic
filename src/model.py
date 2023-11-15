import json
import faiss 
import openai
from typing import List, Union
from sentence_transformers import SentenceTransformer


OPENAI_KEY = json.load(open("./secret/openai-cred.json", "r"))["OPENAI_KEY"]
openai.api_key = OPENAI_KEY

def load_corpus():
    model = SentenceTransformer("msmarco-MiniLM-L-6-v3")
    data_maps_self_declare = json.load(open('corpus/self-declare.json', 'r'))
    index_self_declare = faiss.read_index("corpus/self-declare.index")
    data_maps_reguler = json.load(open('corpus/reguler.json', 'r'))
    index_reguler = faiss.read_index("corpus/reguler.index")
    return (
        model, data_maps_self_declare, index_self_declare,
        data_maps_reguler, index_reguler
    ) 

def fetch_product(idx: int, query: str, df: List):
    result = {}
    result["nama_produk"] = query
    try:
        info = df[idx]
        result["nama_produk_terdekat"] = info['Nama Produk / Rincian']
        result["prediksi_jenis"] = info["Jenis Produk"]
        result["prediksi_kbli"]  = info["Kode KBLI"]
        result["message"]        = "Prediction Success"
    except IndexError:
        result["nama_produk_terdekat"] = ""
        result["prediksi_jenis"] = ""
        result["prediksi_kbli"]  = ""
        result["message"]        = "Prediction Failed "
    return result

def search(query: str, index_vector: object, model_embedding: object, df: List):
    query_vector = model_embedding.encode([query])
    selected_idx = index_vector.search(query_vector, k = 1)
    selected_idx = selected_idx[1].tolist()[0][0]
    result = [fetch_product(selected_idx, query, df)]
    return result

def _set_prompt(description: str):
    custom_prompt = \
    f"""
    Ekstraksi nama bahan dalam deskripsi pemrosesan bahan, dengan contoh cukup menampilkan di bagian result dengan menghapus apabila ada bahan yang duplikat. Tanpa menggunakan embel-embel kata penjelasan.
    Untuk Result, Cukup identifikasi pada deskripsi dibawah ini dan Result hanya seputar bahan makanan atau minuman bukan kata kerja maupun kata benda.
    Deskripsi: {description}
    Result : 
    """
    return custom_prompt

def _parse_result(result: str):
    return result

def detect_bahan(description: str):
    result = {}
    result["step_product"] = description
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages = [{"role" : "user", "content" : _set_prompt(description)}], 
            temperature = 0, max_tokens = 4096, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0
        )
        response = _parse_result(response["choices"][0]["message"]["content"])
    except Exception: 
        response = ""
    result["ingredient_detected"] = response
    return result

def prompt_validation(product_name: str, ingredient: str = ""):
    custom_prompt = \
    f"""
    Tentukan kesesuaian sebuah bahan dengan nama produk berdasarkan informasi bahan, dengan hasil format cukup:

    nama_produk: {product_name}
    bahan: {ingredient}

    Untuk response cukup isi dengan format dibawah.
    Kesesuaian_produk: [Jawaban Anda: "sesuai" atau "tidak sesuai"]
    Alasan: [Jelaskan alasan mengapa Anda menganggap bahan tersebut sesuai atau tidak sesuai dengan nama produk tersebut secara singkat.]
    """
    return custom_prompt

def validation_parse_result(result: str):
    is_valid, reason = result.split("\n")
    is_valid = is_valid.split(": ")[-1]
    reason = reason.split(": ")[-1]
    return is_valid, reason

def validation_product(product_name: str, ingredient: Union[str, None] = None):
    ingredient_found = False
    result = {"is_valid" : "", "reason" : ""}
    corpus_ingredient = list(map(lambda x: x.lower(), ingredient.replace(", ", " ").lower().split()))
    for word in product_name.split():
        word = word.lower()
        if word in corpus_ingredient:
            result["is_valid"] = "sesuai"
            result["reason"] = "main course is exist in ingredient"
            ingredient_found = True
            break 
    if not ingredient_found:
        try:
            response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo", messages = [{"role" : "user", "content" : prompt_validation(product_name, ingredient)}], 
                temperature = 0, max_tokens = 1024, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0
            )
            is_valid, reason = validation_parse_result(response["choices"][0]["message"]["content"])
            result["is_valid"] = is_valid
            result["reason"] = reason
        except Exception: 
            response = ""
    return result