import streamlit as st
from orquestador import get_agent
from langchain_core.messages import HumanMessage

st.title("Asistente IA de Servicios")

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = get_agent()
    st.session_state.messages = []
    # LangGraph maneja TODO el historial
    st.session_state.thread_id = "sesion-1"

# Mostrar historial visual
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            #  LangGraph recuerda todo lo anterior
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            
            response = st.session_state.agent_executor.invoke(
                {"messages": [HumanMessage(content=prompt)]},
                config=config   # ←  historial a cargar para este mensaje
            )
            final_message = response["messages"][-1].content
            st.markdown(final_message)

    st.session_state.messages.append({"role": "assistant", "content": final_message})