from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from PIL import Image
import io

# Inicializa a API
app = FastAPI(title="IA Anti-Fraude Bancária")

# Define o formato de resposta que o app vai receber
class AnaliseResponse(BaseModel):
    is_fraud: bool
    risk_score: float
    scam_type: str
    solution: str

# Rota principal (só para testar se a API tá viva)
@app.get("/")
def home():
    return {"status": "API Ativa e Monitorando"}

# Rota onde o aplicativo vai enviar o print da tela
@app.post("/analisar-tela", response_model=AnaliseResponse)
async def analisar_tela(file: UploadFile = File(...)):
    # Garante que o arquivo enviado é uma imagem
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Envie uma imagem válida.")
    
    try:
        # Lê a imagem direto na memória RAM (sem salvar no computador)
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # [Simulação da IA] Aqui o modelo processaria os pixels/OCR da imagem
        # Como o modelo ainda não tá conectado, simulamos um caso de golpe:
        resultado_ia = {
            "is_fraud": True,
            "risk_score": 0.94,
            "scam_type": "Falso Suporte por Telefone",
            "solution": "Atenção: O banco nunca pede para você baixar aplicativos de suporte. Desinstale o app suspeito imediatamente."
        }
        
        return AnaliseResponse(**resultado_ia)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao processar imagem.")