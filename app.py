import os
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import google.generativeai as genai
from datos import USUARIOS, PRODUCTOS, RESENAS

app = Flask(__name__)
app.secret_key = "unitec_secret_key_2026"

# 1. Configuración Segura de la API Key de Google AI Studio
API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY_SIMULADA")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return redirect(url_for('login'))

# 2. Sistema de Autenticación de Roles Basado en la Data de Prueba
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        if correo in USUARIOS and USUARIOS[correo]['password'] == password:
            session['usuario'] = correo
            session['rol'] = USUARIOS[correo]['rol']
            return redirect(url_for(USUARIOS[correo]['rol']))
        else:
            return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')

# ==========================================
# 👥 ROLE 1: EL VENDEDOR (Generador de Descripciones)
# ==========================================
@app.route('/vendedor', methods=['GET', 'POST'])
def vendedor():
    if session.get('rol') != 'vendedor': return redirect(url_for('login'))
    
    if request.method == 'POST':
        keywords = request.form.get('keywords')
        precio = float(request.form.get('precio'))
        
        prompt = f"""
        System Instruction: Actúas como un redactor experto en marketing digital y E-commerce.
        A partir de las siguientes palabras clave, genera obligatoriamente un formato JSON puro con dos campos:
        "titulo" (un título comercialmente atractivo y persuasivo) y "descripcion" (una descripción detallada, profesional y convincente de al menos 3 líneas).
        Palabras clave: {keywords}
        Respuesta en JSON puro:
        """
        try:
            response = model.generate_content(prompt)
            texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
            data_ia = json.loads(texto_limpio)
            
            nuevo_prod = {
                "id": len(PRODUCTOS) + 1,
                "titulo": data_ia["titulo"],
                "descripcion": data_ia["descripcion"],
                "precio": precio,
                "tags": keywords
            }
            PRODUCTOS.append(nuevo_prod)
            return render_template('vendedor.html', exito="Producto publicado exitosamente por la IA.", productos=PRODUCTOS)
        except Exception as e:
            return render_template('vendedor.html', error="Error con la API de Gemini", productos=PRODUCTOS)
            
    return render_template('vendedor.html', productos=PRODUCTOS)

# ==========================================
# 👥 ROLE 2: EL COMPRADOR (Buscador Semántico)
# ==========================================
@app.route('/comprador', methods=['GET', 'POST'])
def comprador():
    if session.get('rol') != 'comprador': return redirect(url_for('login'))
    
    productos_mostrar = PRODUCTOS
    recomendacion_ia = ""
    
    if request.method == 'POST' and 'busqueda' in request.form:
        busqueda_usuario = request.form.get('busqueda')
        
        prompt = f"""
        System Instruction: Eres el asistente inteligente de un Marketplace. El usuario busca un producto usando lenguaje natural.
        Analiza las necesidades del usuario y compáralas con este catálogo disponible: {PRODUCTOS}.
        Dime cuál es el ID del producto recomendado y explica detalladamente en un párrafo amigable por qué ese producto es la mejor opción para su necesidad.
        Formato de respuesta estricto: "ID Recomendado: [Número] - Explicación: [Tu explicación]"
        Búsqueda del usuario: "{busqueda_usuario}"
        """
        try:
            response = model.generate_content(prompt)
            recomendacion_ia = response.text
        except:
            recomendacion_ia = "No se pudo conectar con el buscador inteligente en este momento."

    return render_template('comprador.html', productos=productos_mostrar, recomendacion=recomendacion_ia)

@app.route('/dejar_reseña', methods=['POST'])
def dejar_resena():
    if session.get('rol') != 'comprador': return redirect(url_for('login'))
    
    comentario = request.form.get('comentario')
    usuario = session.get('usuario')
    
    prompt_moderacion = f"""
    System Instruction: Eres un sistema automatizado de seguridad y moderación de contenido para un Marketplace universitario.
    Analiza la siguiente reseña dejada por un cliente. Debes determinar dos cosas:
    1. El sentimiento general (Positivo, Negativo o Neutral).
    2. Estado de Moderación: Si contiene insultos, groserías o lenguaje inapropiado marca "RECHAZADO". Si es decente marca "APROBADO".
    Responde en formato JSON puro con los campos "sentimiento" y "estado".
    Reseña a evaluar: "{comentario}"
    """
    try:
        response = model.generate_content(prompt_moderacion)
        texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
        resultado = json.loads(texto_limpio)
        sentimiento = resultado["sentimiento"]
        estado = resultado["estado"]
    except:
        sentimiento = "Neutral"
        estado = "APROBADO"

    RESENAS.append({
        "usuario": usuario,
        "comentario": comentario,
        "sentimiento": sentimiento,
        "estado": estado
    })
    return redirect(url_for('comprador'))

# ==========================================
# 👥 ROLE 3: EL ADMINISTRADOR (Moderador)
# ==========================================
@app.route('/admin')
def admin():
    if session.get('rol') != 'admin': return redirect(url_for('login'))
    return render_template('admin.html', resenas=RESENAS)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
  
