# 🛒 Conversational Commerce - MANTIS

**Asistente conversacional de ventas basado en IA para comercios**

Conversational Commerce es un chatbot desarrollado para permitir que los clientes interactúen con el catálogo de un comercio utilizando **lenguaje natural**.

En lugar de navegar manualmente por categorías o buscar productos específicos, el usuario puede expresar lo que necesita y el sistema interpreta su intención, consulta el catálogo real y proporciona productos disponibles.

El proyecto utiliza **Telegram como interfaz conversacional**, **FastAPI como backend**, **PostgreSQL como fuente de verdad del catálogo e inventario** y un **LLM local ejecutado mediante Ollama** para la interpretación de lenguaje natural.

---

## 🎯 Objetivo

Crear un asistente de ventas capaz de entender conversaciones naturales y conectarlas con información real del comercio.

Por ejemplo:

> **Usuario:**
> Quiero cosas para hacer hamburguesas.

El asistente puede identificar la intención y consultar el catálogo para encontrar productos relacionados.

Posteriormente, el usuario puede preguntar:

> **Usuario:**
> ¿Tienen 20 panes de hamburguesa?

El sistema consulta el inventario real antes de responder.

También es posible seleccionar productos directamente desde Telegram mediante botones interactivos.

---

## ✨ Funcionalidades actuales

### 🤖 Comprensión de lenguaje natural

El sistema utiliza un modelo de lenguaje local para identificar información estructurada a partir del mensaje del usuario:

* Intención
* Producto
* Ocasión
* Número de personas
* Presupuesto
* Cantidad solicitada
* Preferencias

Las intenciones principales son:

* `product_recommendation`
* `product_search`
* `stock_check`
* `general_question`
* `unknown`

---

### 🛍️ Búsqueda y recomendación de productos

El asistente consulta productos directamente desde PostgreSQL.

Las recomendaciones están basadas en el catálogo disponible y no en una lista de productos generada por el modelo.

Esto permite evitar que el LLM invente:

* Productos
* Precios
* Stock

---

### 📦 Consulta de inventario

El usuario puede consultar la disponibilidad de un producto.

Ejemplo:

> ¿Cuántas hamburguesas de res tienen?

El sistema consulta el stock almacenado en PostgreSQL y devuelve la cantidad disponible.

También puede comprobar cantidades específicas:

> ¿Tienen 20 hamburguesas de res?

La respuesta se basa en el inventario real.

---

### 🔘 Selección interactiva de productos

Cuando una búsqueda devuelve múltiples productos, Telegram muestra botones interactivos.

El usuario puede seleccionar directamente el producto que le interesa.

La selección se almacena en el contexto de la conversación mediante su `product_id`.

Esto permite mantener el producto seleccionado durante los siguientes mensajes.

---

### 💬 Memoria de conversación

Cada conversación se almacena en PostgreSQL.

El sistema mantiene:

* Conversación
* Mensajes del usuario
* Mensajes del asistente
* Intención actual
* Producto mencionado
* Producto seleccionado
* Presupuesto
* Cantidad
* Preferencias

Esto permite construir interacciones conversacionales en lugar de tratar cada mensaje como una consulta independiente.

---

## 🏗️ Arquitectura

```text
                    ┌──────────────────┐
                    │     Telegram     │
                    │   Chat Interface │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │      Backend     │
                    └────────┬─────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
          ┌───────────────┐     ┌───────────────┐
          │   LLM Local   │     │  PostgreSQL   │
          │    Ollama     │     │   + pgvector  │
          └───────┬───────┘     └───────┬───────┘
                  │                     │
                  │                     │
                  ▼                     ▼
          ┌───────────────┐     ┌───────────────┐
          │ Intent        │     │ Product       │
          │ Extraction    │     │ Catalog       │
          └───────────────┘     │ Inventory     │
                                │ Conversations │
                                └───────────────┘
```

### Principio de diseño

El proyecto sigue una separación clara entre la interpretación del lenguaje y la lógica del negocio:

> **LLM interpreta → Backend decide → PostgreSQL confirma**

El modelo de lenguaje no tiene autoridad sobre productos, precios o inventario.

---

## 📂 Estructura del proyecto

```text
conversational-commerce/
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── product.py
│   │   │   ├── conversation.py
│   │   │   ├── message.py
│   │   │   └── conversation_context.py
│   │   │
│   │   ├── schemas/
│   │   │   └── chat.py
│   │   │
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── search_service.py
│   │   │   ├── recommendation_service.py
│   │   │   └── response_service.py
│   │   │
│   │   ├── main.py
│   │   └── telegram_bot.py
│   │
│   ├── import_products.py
│   └── requirements.txt
│
├── data/
│   └── products.csv
│
├── frontend/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🧰 Tecnologías

### Backend

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **PostgreSQL**
* **pgvector**

### Inteligencia Artificial

* **Ollama**
* **Llama 3.2 3B**
* Structured intent extraction
* Conversational context

### Integración

* **Telegram Bot API**
* `python-telegram-bot`

### Infraestructura

* **Docker**
* **Docker Compose**

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <REPOSITORY_URL>
cd conversational-commerce
```

### 2. Crear entorno virtual

En Windows:

```powershell
python -m venv .venv
```

Activarlo:

```powershell
.venv\Scripts\activate
```

En Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instalar dependencias

```bash
pip install -r backend/requirements.txt
```

---

### 4. Iniciar PostgreSQL

El proyecto utiliza Docker Compose:

```bash
docker compose up -d
```

Verificar que el contenedor esté ejecutándose:

```bash
docker ps
```

---

### 5. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

**Nunca subir este archivo a GitHub.**

---

### 6. Instalar Ollama

Instala Ollama en tu sistema y descarga el modelo utilizado por el proyecto:

```bash
ollama pull llama3.2:3b
```

Verifica que Ollama esté funcionando:

```bash
ollama list
```

---

### 7. Cargar productos

El catálogo de prueba se encuentra en:

```text
data/products.csv
```

Ejecutar:

```bash
cd backend
python import_products.py
```

Esto cargará los productos en PostgreSQL.

---

## ▶️ Ejecutar el backend

Desde `backend/`:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Documentación interactiva:

```text
http://127.0.0.1:8000/docs
```

---

## 🤖 Ejecutar el bot de Telegram

En otra terminal:

```bash
cd backend
python -m app.telegram_bot
```

El bot comenzará a utilizar **long polling** para recibir mensajes.

Una vez iniciado, puedes abrir Telegram y comenzar una conversación con el bot.

---

## 💬 Ejemplos de interacción

### Recomendación

```text
Usuario:
Quiero cosas para hacer hamburguesas.

Bot:
🛒 Estos son los productos que encontré para hamburguesas:

• Hamburguesa de res — $12.000 por unidad
• Pan de hamburguesa — $4.000 por paquete
• Queso cheddar — $8.000 por paquete
...
```

### Búsqueda específica

```text
Usuario:
¿Tienen pan de hamburguesa?

Bot:
🔎 Encontré Pan de hamburguesa.

Precio: $4.000 por paquete
Disponibles: 80
```

### Consulta de stock

```text
Usuario:
¿Cuántas hamburguesas de res tienen?

Bot:
📦 Tenemos 50 unidades disponibles de Hamburguesa de res.
```

### Consulta de cantidad

```text
Usuario:
¿Tienen 20 hamburguesas de res?

Bot:
✅ Sí, tenemos 20 unidades de Hamburguesa de res.

Stock actual: 50.
```

### Selección de producto

Cuando existen varias coincidencias:

```text
Bot:

Encontré varios productos:

[ Hamburguesa de res ]
[ Hamburguesa de pollo ]
```

El usuario puede seleccionar directamente una opción mediante los botones de Telegram.

---

## 🔐 Control de inventario

Una de las decisiones fundamentales del proyecto es que el modelo de lenguaje **no controla los datos comerciales**.

Por ejemplo, si PostgreSQL contiene:

```text
Producto: Hamburguesa de res
Precio: 12000
Stock: 50
```

el LLM no puede modificar esos valores simplemente generando otra respuesta.

El flujo es:

```text
Mensaje del usuario
        ↓
LLM
        ↓
Intent estructurado
        ↓
Backend
        ↓
Consulta PostgreSQL
        ↓
Datos reales
        ↓
Respuesta
```

Esto reduce el riesgo de respuestas con información comercial inventada.

---

## 🗃️ Modelo de datos

### Products

Contiene el catálogo del comercio:

```text
id
name
description
category
price
stock
unit
brand
```

### Conversations

Representa una conversación con un usuario:

```text
id
user_phone
created_at
```

En Telegram, el identificador del usuario se utiliza para mantener la conversación.

### Messages

Almacena los mensajes:

```text
id
conversation_id
role
content
created_at
```

### Conversation Context

Mantiene el estado conversacional:

```text
id
conversation_id
intent
occasion
product_type
selected_product_id
people
budget
quantity
preference
```

---

## 🧠 Diseño de IA

El LLM no genera directamente una respuesta comercial basada en conocimiento propio.

Primero transforma el lenguaje natural en una estructura:

```json
{
    "intent": "stock_check",
    "occasion": null,
    "product_type": "hamburguesa de res",
    "people": null,
    "budget": null,
    "quantity": 20,
    "preference": null
}
```

Después el backend utiliza esa información para consultar el catálogo.

Esta separación permite que el componente de IA sea reemplazable sin modificar la lógica principal del comercio.

---

## 🛣️ Roadmap

### Implementado

* [x] FastAPI backend
* [x] PostgreSQL
* [x] Product catalog
* [x] Product search
* [x] Inventory queries
* [x] Local LLM
* [x] Intent extraction
* [x] Conversation persistence
* [x] Conversation context
* [x] Telegram integration
* [x] Interactive product selection

### Próximas funcionalidades

* [ ] Crear pedidos
* [ ] Order items
* [ ] Validación de stock al realizar un pedido
* [ ] Carrito de compras
* [ ] Confirmación de pedidos
* [ ] Manejo de múltiples productos en un pedido
* [ ] Estados de pedido
* [ ] Panel para administradores del comercio
* [ ] Importación de catálogos reales
* [ ] Búsqueda semántica con embeddings
* [ ] RAG sobre información de productos
* [ ] Integración con sistemas externos de inventario
* [ ] Analítica de conversaciones y ventas

---

## 🎓 Propósito del proyecto

Este proyecto fue desarrollado como un proyecto de portafolio enfocado en demostrar la integración de:

**IA + Backend + Bases de datos + APIs + Automatización + Conversational UX**

Más que construir un chatbot genérico, el objetivo es explorar cómo conectar modelos de lenguaje con **sistemas transaccionales reales**, manteniendo la información crítica bajo control del backend y de la base de datos.

---

## 📄 Licencia

Este proyecto está destinado principalmente a fines educativos y de portafolio.
