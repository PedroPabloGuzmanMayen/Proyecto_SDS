import joblib
import gradio as gr
from google import genai
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
import re
import asyncio

FEATURE_COLS = ['url_suspicious', 'has_url', 'impersonation_url', 'has_urgency', 'has_reward', 'has_impersonation', 'has_threat', 'has_cta']

svm_model = joblib.load('../models/svm_model.pkl')
nn_model = joblib.load('../models/mlp_model.pkl')


load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)


whitelist_df = pd.read_csv("../data/whitelist.csv")
whitelist = set(
    whitelist_df["numero"]
    .astype(str)
    .str.strip()  
)


def normalize_phone(phone):
    phone = str(phone)
    
    phone = re.sub(r"\D", "", phone)
    
    if phone.startswith("502"):
        phone = phone[3:]
    
    phone = phone[-8:]
    
    return phone


def extract_features(text):
    text = str(text)
    tl = text.lower()

    has_url = int(bool(re.search(r'https?://\S+|www\.\S+', text)))

    legit_domains = r'(tigo\.com\.gt|claro\.com\.gt|movistar\.com\.gt|' \
                    r'bac\.net|banrural\.com\.gt|bam\.com\.gt|' \
                    r'sat\.gob\.gt|igss\.org\.gt|renap\.gob\.gt|' \
                    r'correos\.gob\.gt|bit\.ly|qrco\.de)'

    url_suspicious = 0
    for url in re.findall(r'https?://\S+', text):
        if not re.search(legit_domains, url, re.I):
            url_suspicious = 1

    msg_length = len(text)
    word_count = len(text.split())

    urgency_words = ['urgente','urgentemente','inmediatamente','hoy mismo',
                     'horas','rápido','rápidamente','pronto','ahora','mora']
    has_urgency = int(any(w in tl for w in urgency_words))

    cta_words = ['llama','llame','llamá','clic','click','ingresa','ingrese',
                 'actualiza','actualice','confirma','confirme','paga','pague',
                 'pagá','descarga','verificá','verifica','accede','acceda']
    has_cta = int(any(w in tl for w in cta_words))

    reward_words = ['ganaste','ganó','felicidades','felicitaciones','premiado',
                    'gratis','gratuito','regalo','sorteo','recompensa','seleccionado','premio']
    has_reward = int(any(w in tl for w in reward_words))

    threat_words = ['decomiso','pérdida','bloqueo','bloqueado','suspensión',
                    'cancelado','penalidad','multa','retención','retenido',
                    'daño','vencimiento','vence','plazo']
    has_threat = int(any(w in tl for w in threat_words))

    impersonation_patterns = ['guatex','emetra','migracion','migración',
                             'aeropuerto','sat aduanas','renap alerta',
                             'bam notif','bac alerta','banrural informa','bam']
    has_impersonation = int(any(w in tl for w in impersonation_patterns))

    impersonation_url = int(has_impersonation and url_suspicious)

    return pd.DataFrame([{
        'has_url': has_url,
        'url_suspicious': url_suspicious,
        'msg_length': msg_length,
        'word_count': word_count,
        'has_urgency': has_urgency,
        'has_cta': has_cta,
        'has_reward': has_reward,
        'has_threat': has_threat,
        'has_impersonation': has_impersonation,
        'impersonation_url': impersonation_url
    }])


async def get_embedding(text):
    loop = asyncio.get_event_loop()

    def call():
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=[text]
        )
        return result.embeddings[0].values

    emb = await loop.run_in_executor(None, call)
    return np.array(emb).reshape(1, -1)


async def predict_nn(text):
    try:
        emb = await get_embedding(text)
        prob = await asyncio.to_thread(
            lambda: nn_model.predict_proba(emb)[0][1]
        )
        return prob
    except:
        return None

async def predict_svm(text):
    def compute():
        features = extract_features(text)
        features = features[FEATURE_COLS]
        return svm_model.predict_proba(features)[0][1]

    return await asyncio.to_thread(compute)


async def predict_pipeline(text, phone):

    phone = normalize_phone(phone)
    print(phone)
    print(phone and phone in whitelist)
    if phone and phone in whitelist:
        return f"✅ NO SPAM (whitelist)\nNúmero: {phone}"

    nn_task = predict_nn(text)
    svm_task = predict_svm(text)

    prob_nn, prob_svm = await asyncio.gather(nn_task, svm_task)

    probs = []
    if prob_nn is not None:
        probs.append(prob_nn)
    probs.append(prob_svm)

    final_prob = float(np.mean(probs))
    label = "Spam 🚨" if final_prob > 0.4 else "No Spam ✅"

    prob_nn_str = f"{prob_nn:.2f}" if prob_nn is not None else "N/A"

    return f"""
Resultado: {label}

NN (semántico): {prob_nn_str}
SVM (features): {prob_svm:.2f}
Final: {final_prob:.2f}
"""

demo = gr.Interface(
    fn=predict_pipeline,
    inputs=[
        gr.Textbox(lines=4, placeholder="Escribe el mensaje..."),
        gr.Textbox(placeholder="+502XXXXXXXX (opcional)")
    ],
    outputs="text",
    title="Detector de Spam Guatemala 🇬🇹",
    description="Whitelist + IA híbrida (NN + SVM)"
)

if __name__ == "__main__":
    demo.launch()