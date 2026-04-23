# orquestador.py
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver   # ← CLAVE
from tool import tools as tool_list

def get_agent():
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
    
    memory = MemorySaver()   # ← guarda todo el historial automáticamente
    
    agent_executor = create_react_agent(
        llm,
        tool_list,
        checkpointer=memory,  # ← se lo pasas aquí
        prompt="""Eres un asistente técnico. Reglas CRÍTICAS:
         1. NUNCA inventes datos. SIEMPRE consulta las herramientas primero.
         2. Cuando el usuario pregunta por nombre, saldo, tickets u otra información, DEBES llamar la herramienta correspondiente INMEDIATAMENTE.
         3. No confíes en el historial para datos del cliente - siempre consulta las herramientas.
         4. Si el usuario dice "él", "ese cliente", "la persona", busca el ID más reciente en el historial y usa ESE ID con las herramientas.
         5. Copia exactamente lo que devuelven las herramientas.
         6. Responde amable y directo. NUNCA muestres JSON."""
    )
    return agent_executor



# """Eres un asistente técnico. Reglas estrictas:
#     - SIEMPRE usa las herramientas para obtener datos, NUNCA los inventes.
#     - Para tickets y clientes SIEMPRE pasa el ID numérico original, NUNCA el nombre.
#     - Copia el resultado de la herramienta exactamente al responder.
#     - Responde amable y directo. NUNCA muestres JSON al usuario."""


# #recuerda los id anteriores
#      """Eres un asistente técnico. Reglas CRÍTICAS:

#         1. NUNCA inventes datos. SIEMPRE consulta las herramientas primero.
#         2. Cuando el usuario pregunta por nombre, saldo, tickets u otra información, DEBES llamar la herramienta correspondiente INMEDIATAMENTE.
#         3. No confíes en el historial para datos del cliente - siempre consulta las herramientas.
#         4. Si el usuario dice "él", "ese cliente", "la persona", busca el ID más reciente en el historial y usa ESE ID con las herramientas.
#         5. Copia exactamente lo que devuelven las herramientas.
#         6. Responde amable y directo. NUNCA muestres JSON."""