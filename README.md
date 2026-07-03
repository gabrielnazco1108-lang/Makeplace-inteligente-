# Marketplace Inteligente - Proyecto Integrador 🚀
### Universidad Tecnológica del Centro (UNITEC - Campus Guacara)
**Materia:** Programación I  
**Estudiante:** Gabriel Nazco  

Este repositorio contiene un prototipo funcional de una plataforma E-commerce con arquitectura basada en roles (**Vendedor, Comprador y Administrador**), integrada directamente con la API de **Google AI Studio (Gemini-Pro)** para la automatización de procesos mediante Inteligencia Artificial.

---

## 🛠️ Desafíos Técnicos y Resolución de Obstáculos

### 1. Control de "Alucinaciones" de la Inteligencia Artificial
Durante las pruebas de la Fase 1 en Google AI Studio, el modelo presentaba alucinaciones lógicas: al usar el buscador inteligente, la IA recomendaba productos ficticios o inventaba características que no existían en nuestra base de datos.
*   **Solución Aplicada:** Se refinó la ingeniería de prompts utilizando **System Instructions (Instrucciones del Sistema)** muy estrictas. Se le indicó explícitamente a Gemini: *"Eres el asistente de un catálogo cerrado. Analiza las necesidades del usuario y compáralas únicamente con este catálogo disponible: [PRODUCTOS]. Está rotundamente prohibido inventar identificadores o productos fuera de esta lista"*. Con este confinamiento del contexto, se eliminaron por completo las alucinaciones comerciales.

### 2. Estructuración y Parseo de Respuestas (JSON Limpio)
Uno de los mayores dolores de cabeza en el desarrollo backend fue lograr que la IA devolviera estructuras de datos predecibles. En las primeras interacciones, Gemini respondía con texto plano narrativo o bloques decorados con triple comilla invertida (```json), lo que rompía el servidor en Python al intentar usar `json.loads()`.
*   **Solución Aplicada:** Se ajustó el parámetro de **Temperatura a 0.2** (reduciendo la aleatoriedad de la IA para que sea más determinista) y se modificó el prompt para obligar al modelo a usar un esquema estricto de claves-valores. Complementariamente, se aplicó una función de limpieza de cadenas (`.replace()`) en el backend para remover las marcas Markdown antes de procesar la respuesta.

### 3. Seguridad de las Credenciales Corporativas (API Key)
La guía exigía proteger el acceso a la plataforma de Google AI Studio evitando la exposición de contraseñas y claves de consumo en servidores públicos de código.
*   **Solución Aplicada:** Se implementó una arquitectura basada en variables de entorno utilizando la librería `python-dotenv`. La API Key real se aloja en un archivo local `.env` que se encuentra configurado dentro del archivo `.gitignore`, garantizando su total aislamiento en GitHub.

---

## 👥 Datos de Prueba de Roles Requeridos (Test Data)

Para simular la interacción completa del ciclo de desarrollo, use las siguientes credenciales en la pantalla de login:

*   **Vendedor:** `vendedor@test.com` | Clave: `123`
*   **Comprador:** `comprador@test.com` | Clave: `123`
*   **Administrador:** `admin@test.com` | Clave: `123`
*   
