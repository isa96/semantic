# SemanticKBLI
Semantic Search Classification with Transformers and FastAPI

# Benchmarking

| Source Data | Module         | Algorithm | Acc. Jenis Produk (%) | Acc. KBLI (%)|
|-------------|----------------|-----------|-----------------------|--------------|
| Mei         | Self Declare   | AutoML C# | 56.461                | 48.787       |
| Juni        | Self Declare   | AutoML C# | 56.461                | 83.041       |
| Juni        | Self Declare with Enrichment  | S-Bert KNN    | 99.477                | 98.929       |
| Juli        | Reguler        | S-Bert KNN    | 100.00                | 97.841       |

# Tutorial Run Service
1. Create docker container on local.
```
docker build -t fastapi-service .
```
2. Running container
```
docker run -d -p 8000:8000 --name fastapi-container --restart unless-stopped fastapi-service
```
3. Access Swagger Documentation via
```
localhost:8000/docs
```