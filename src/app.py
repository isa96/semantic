import uvicorn
from typing import Union
from fastapi import FastAPI, Request
from logger import send_logger, connect_firebase
from fastapi.middleware.cors import CORSMiddleware
from model import load_corpus, search, detect_bahan, validation_product

# Define global variable
app = FastAPI()
database = connect_firebase()
model, mapping_sd, index_sd, mapping_reg, index_reg = load_corpus()

# Enable Cross-Origin Resource Sharing (CORS) for all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = origins,
    allow_headers = origins,
)

# Define base response
response = {"message" : "Success", "status_code" : 200, "body" : []}


@app.middleware("http")
async def logger(request: Request, call_next: object):
    response = await call_next(request)
    return response 

@app.get("/")
async def root():
    response["body"].append("Access Swagger via IP:8000/docs")
    return response

@app.post("/self-declare/predict")
async def classify_text_self_declare(text: str, request: Request):
    if text != "":
        response["body"] = search(text, index_sd, model, mapping_sd)
    else: 
        response["message"] = "text blank"
        response["status_code"] = 404
    send_logger(request, response, database)
    return response

@app.post("/reguler/predict")
async def classify_text_reguler(text: str, request: Request):
    if text != "":
        response["body"] = search(text, index_reg, model, mapping_reg)
    else: 
        response["message"] = "text blank"
        response["status_code"] = 404
    send_logger(request, response, database)
    return response

@app.post("/reguler/check-bahan/")
async def detect_nama_bahan(text: str, request: Request):
    if text != "":
        response["body"] = [detect_bahan(text)]
    else: 
        response["message"] = "text blank"
        response["status_code"] = 404
    send_logger(request, response, database, is_bahan = True)
    return response

@app.get("/expert-system/validation")
async def validation_product_name(product_name: str, ingredients: Union[str, None] = None, step_creation: Union[str, None] = None):
    if not (ingredients is None and step_creation is None):
        if ingredients is None:
            response["body"] = [{"is_valid" : "sesuai", "reason" : "main course is satisfied in step_creation"}]
        else:
            result = validation_product(product_name, ingredients)
            response["body"] = [result]
    else:
        response["status_code"] = 401
        response["message"] = "at least parameter one of ingredient or step_creation not null."
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)