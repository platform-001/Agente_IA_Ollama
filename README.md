## **Orquestador de Microservicios con IA (Ollama + LangChain)**

Este proyecto implementa una arquitectura de microservicios coordinada por un agente de IA que consulta datos en tiempo real sobre clientes, tickets y seguridad.

### **Requisitos e Instalación**

1. Instalar Python  
   Ir a https://www.python.org/downloads/ y descargar.

   Al instalar, se debe marcar la casilla que dice "Add Python to PATH". Si no lo hacen, el comando pip o python no funcionará en la terminal y dará error.  

   Una vez instalado, abra un terminal y escriba:  
   ```
   python --version
   ```
2.  Instalar Ollama  
   Descargar e instalar Ollama desde https://ollama.com/download/windows  
   Una vez instalado, abrir una terminal y descargar el modelo:
   ```
   ollama pull qwen2.5:7b
   ```
3. Librerías de IA y Frontend 
   ```
   pip install langchain langchain-community langchain-core streamlit
   ```
4. Librerías para Microservicios y Conectividad
    ```
   pip install fastapi uvicorn httpx
   ```

### **Guía de Ejecución (Orden Obligatorio)**

1. Iniciar Ollama  
    ```
   ollama run qwen2.5:14b
   ```    
2. Activar microservicios
   
    ```
   python microservicios/clientes.py
     ```
     ```
   python microservicios/tickets.py
     ```
      ```
   python microservicios/vulnerabilidades.py
     ```
3. Iniciar streamlit
   
    ```
     python -m streamlit run app.py    
   ```
