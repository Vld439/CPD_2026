from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from groq import Groq

app = FastAPI()
client = Groq() 

@app.get("/", response_class=HTMLResponse)
def instant():
    message = (
        "¡Estás en un sitio web que acaba de entrar en producción por primera vez!\n"
        "Por favor, responde con un anuncio entusiasta para dar la bienvenida a los visitantes."
    )

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": message}]
    )

    reply = response.choices[0].message.content.replace("\n", "<br/>")

    html = f"""
    <html>
        <head><title>¡En vivo al instante!</title></head>
        <body><p>{reply}</p></body>
    </html>
    """
    return html