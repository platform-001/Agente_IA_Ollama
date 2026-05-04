import streamlit as st
from orquestador import get_agent
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tool import DINAMICAS_TOOLS


def limpiar_historial(messages: list) -> list:
    ids_dinamicos = {
        tc["id"]
        for msg in messages if isinstance(msg, AIMessage)
        for tc in (msg.tool_calls or [])
        if tc["name"] in DINAMICAS_TOOLS
    }
    return [
        msg for msg in messages
        if not (isinstance(msg, ToolMessage) and msg.tool_call_id in ids_dinamicos)
        and not (isinstance(msg, AIMessage) and msg.tool_calls and
                 all(tc["name"] in DINAMICAS_TOOLS for tc in msg.tool_calls))
    ]


# ── UI ──────────────────────────────────────────────────────────────────────

st.title("Asistente IA de Servicios")

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = get_agent()
    st.session_state.messages = []
    st.session_state.thread_id = "sesion-1"

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            agent = st.session_state.agent_executor

            state = agent.get_state(config)
            if state and state.values.get("messages"):
                agent.update_state(config, {"messages": limpiar_historial(state.values["messages"])})

            response = agent.invoke({"messages": [HumanMessage(content=prompt)]}, config=config)
            final = response["messages"][-1].content
            st.markdown(final)

    st.session_state.messages.append({"role": "assistant", "content": final})



















# import streamlit as st
# from orquestador import get_agent
# from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
# from tool import DINAMICAS_TOOLS

# # Marca que se inyecta en additional_kwargs para identificar
# # AIMessages que contienen datos dinámicos
# _DYNAMIC_TAG = "contains_dynamic_data"


# def limpiar_dinamicos(messages: list) -> list:
#     """
#     Estrategia general y escalable:
#     1. Detecta qué AIMessages invocaron herramientas dinámicas  →  los marca con _DYNAMIC_TAG
#     2. En la siguiente conversación elimina:
#        - AIMessages marcados con _DYNAMIC_TAG (respuestas con datos dinámicos)
#        - ToolMessages cuyo tool_call_id sea dinámico
#        - AIMessages que tenían tool_calls dinámicos
#     Sin listas de palabras clave, funciona con cualquier herramienta futura.
#     """

#     # Pasada 1 — recolectar IDs dinámicos y marcar AIMessages que los invocaron
#     ids_dinamicos: set[str] = set()
#     ids_ai_con_dinamicos: set = set()   # id() de los AIMessage a limpiar

#     for msg in messages:
#         if isinstance(msg, AIMessage) and msg.tool_calls:
#             dinamicos = [tc for tc in msg.tool_calls if tc["name"] in DINAMICAS_TOOLS]
#             if dinamicos:
#                 for tc in dinamicos:
#                     ids_dinamicos.add(tc["id"])
#                 ids_ai_con_dinamicos.add(id(msg))

#         # Si el mensaje fue taggeado como "contiene datos dinámicos" → también eliminar
#         if isinstance(msg, AIMessage):
#             if msg.additional_kwargs.get(_DYNAMIC_TAG):
#                 ids_ai_con_dinamicos.add(id(msg))

#     # Pasada 2 — construir lista limpia
#     resultado = []
#     for msg in messages:

#         if isinstance(msg, ToolMessage):
#             if msg.tool_call_id in ids_dinamicos:
#                 continue

#         elif isinstance(msg, AIMessage):
#             if id(msg) in ids_ai_con_dinamicos:
#                 # Si tenía tool_calls mixtos (estáticos + dinámicos), conservar solo estáticos
#                 calls_validos = [tc for tc in msg.tool_calls if tc["name"] not in DYNAMIC_TOOLS] if msg.tool_calls else []
#                 if calls_validos:
#                     resultado.append(msg.copy(update={"tool_calls": calls_validos,
#                                                        "additional_kwargs": {}}))
#                 elif msg.content and not msg.tool_calls:
#                     # Era una respuesta final taggeada → omitir completo
#                     pass
#                 # Si solo tenía tool_calls dinámicos y sin texto → omitir
#                 continue

#         resultado.append(msg)

#     print(f"[Limpieza] {len(messages)} → {len(resultado)} | IDs dinámicos: {ids_dinamicos}")
#     return resultado


# def taggear_respuesta_dinamica(messages: list) -> list:
#     """
#     Después de cada invocación, revisa si el último AIMessage
#     fue precedido por tool_calls dinámicos. Si es así, lo taggea
#     para que en el próximo turno sea eliminado.
#     """
#     # Buscar el último AIMessage final (sin tool_calls = respuesta al usuario)
#     tool_calls_dinamicos_vistos = False
#     nuevos = list(messages)

#     for msg in reversed(nuevos):
#         if isinstance(msg, AIMessage):
#             if msg.tool_calls:
#                 # Es un AIMessage intermedio con llamadas
#                 if any(tc["name"] in DYNAMIC_TOOLS for tc in msg.tool_calls):
#                     tool_calls_dinamicos_vistos = True
#             else:
#                 # Es la respuesta final al usuario
#                 if tool_calls_dinamicos_vistos and not msg.additional_kwargs.get(_DYNAMIC_TAG):
#                     # Taggear in-place (copy para no mutar el original)
#                     idx = nuevos.index(msg)
#                     nuevos[idx] = msg.copy(update={
#                         "additional_kwargs": {**msg.additional_kwargs, _DYNAMIC_TAG: True}
#                     })
#                 break

#     return nuevos


# def aplicar_limpieza(agent_executor, config: dict) -> None:
#     state = agent_executor.get_state(config)
#     if not (state and state.values.get("messages")):
#         return
#     originales = state.values["messages"]
#     limpios = limpiar_dinamicos(originales)
#     if len(limpios) != len(originales):
#         agent_executor.update_state(config, {"messages": limpios})


# def taggear_en_estado(agent_executor, config: dict) -> None:
#     state = agent_executor.get_state(config)
#     if not (state and state.values.get("messages")):
#         return
#     originales = state.values["messages"]
#     taggeados = taggear_respuesta_dinamica(originales)
#     if taggeados != originales:
#         agent_executor.update_state(config, {"messages": taggeados})


# # ── UI ──────────────────────────────────────────────────────────────────────

# st.title("Asistente IA de Servicios")

# if "agent_executor" not in st.session_state:
#     st.session_state.agent_executor = get_agent()
#     st.session_state.messages = []
#     st.session_state.thread_id = "sesion-1"

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("¿En qué puedo ayudarte?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         with st.spinner("Consultando..."):
#             config = {"configurable": {"thread_id": st.session_state.thread_id}}

#             # 1️⃣ Limpiar datos dinámicos del historial
#             aplicar_limpieza(st.session_state.agent_executor, config)

#             # 2️⃣ Invocar al agente
#             response = st.session_state.agent_executor.invoke(
#                 {"messages": [HumanMessage(content=prompt)]},
#                 config=config,
#             )

#             final_message = response["messages"][-1].content
#             st.markdown(final_message)

#     # 3️⃣ Taggear la respuesta recién generada si usó herramientas dinámicas
#     taggear_en_estado(st.session_state.agent_executor, config)

#     st.session_state.messages.append({"role": "assistant", "content": final_message})