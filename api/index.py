import os
import jwt #para verificar el JWT manualmente y mostrar el error real en vez de 403, en requirements.txt se agrega PyJWT y cryptography para esto 
from fastapi import FastAPI, Depends, HTTPException, Request  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()

@app.get("/api") #cambio para que muestre el error exacto en vez de 403 forbidden
def idea(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Falta el token de seguridad")
    
    token = auth_header.split(" ")[1]
    jwks_url = os.environ.get("CLERK_JWKS_URL")
    

    try:
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False} 
        )
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Error real de JWT: {str(e)}")

    try: #para mostrar el error real de Groq en vez de un error 500
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Vercel no encuentra la variable GROQ_API_KEY")

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        
        prompt = [{"role": "user", "content": "Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points"}]
        
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b", 
            messages=prompt, 
            stream=True
        )
    except Exception as e:
        # Si Groq falla, mostramos el error real en vez de un error 500
        raise HTTPException(status_code=500, detail=f"Error de Groq: {str(e)}")
    def event_stream():
        for chunk in stream:
            text = chunk.choices[0].delta.content
            if text:
                lines = text.split("\n")
                for line in lines[:-1]:
                    yield f"data: {line}\n\n"
                    yield "data:  \n"
                yield f"data: {lines[-1]}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")