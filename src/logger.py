import firebase_admin
from typing import Union
from datetime import datetime
from fastapi import Request, Response
from firebase_admin import credentials, firestore

def connect_firebase(cert_path: str = "secret/firebase-cred.json"):
    credential = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(credential)
    database = firestore.client()
    return database

def send_logger(request: Request, response: Response, database: object, collection: str = "logs", is_bahan: bool = False): 
    schema_logs = {
        "datetime" : datetime.now().isoformat(), 
        "method" : request.method, 
        "url" : request.url.path, 
        "headers" : dict(request.headers), 
        "client_ip" : request.client.host
    }

    if is_bahan:
        try:
            schema_logs["step_product"] = response["body"][0]["step_product"]
            schema_logs["ingredient_detected"] = response["body"][0]["ingredient_detected"]
        except Exception as E:
            schema_logs["step_product"] = f"Error: {E}"
            schema_logs["ingredient_detected"] = []
    else:
        schema_logs["product_name"]            = response["body"][0]["nama_produk"]
        schema_logs["prediction_type_product"] = response["body"][0]["prediksi_jenis"]
        schema_logs["prediction_kbli_product"] = response["body"][0]["prediksi_kbli"]
        schema_logs["prediction_result"]       = response["body"][0]["message"]
        schema_logs["product_name_nearest"]    = response['body'][0]["nama_produk_terdekat"]

    document = database.collection(collection).document()
    document.set(schema_logs)

def send_logger_validation(
        request: Request, response: Response, database: object, collection: str = "logs",
        product_name: str = "", ingredients: Union[str, None] = None, step_creation: Union[str, None] = None
    ):
    schema_logs = {
        "datetime" : datetime.now().isoformat(), 
        "method" : request.method, 
        "url" : request.url.path, 
        "headers" : dict(request.headers), 
        "client_ip" : request.client.host
    }

    schema_logs["product_name"]  = product_name
    schema_logs["ingredients"]   = ingredients
    schema_logs["step_creation"] = step_creation
    schema_logs["is_valid"] = response["body"][0]["is_valid"]
    schema_logs["reason"]   = response["body"][0]["reason"]

    document = database.collection(collection).document()
    document.set(schema_logs)