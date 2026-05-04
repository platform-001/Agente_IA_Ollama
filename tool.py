import httpx
from langchain_core.tools import tool


DINAMICAS_TOOLS = {"get_customer_saldo", "get_tickets_count", "get_security_report"}
ESTATICAS_TOOLS  = {"get_customer_name"}

@tool
def get_customer_name(customer_id: str) -> str:
    """Obtiene el nombre del cliente a partir de su ID.
    El argumento debe ser el ID numérico del cliente como string."""
    print(f"[ESTÁTICO] Llamando a: http://localhost:8001/customer/{customer_id}")
    with httpx.Client() as client:
        try:
            response = client.get(f"http://localhost:8001/customer/{customer_id}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return f"El cliente con ID {customer_id} se llama {data.get('nombre')}."
        except httpx.ConnectError:
            return "Error: Servicio de clientes no disponible."
        except Exception as e:
            return f"Error consultando nombre del cliente: {str(e)}"
 
 
@tool
def get_customer_saldo(customer_id: str) -> str:
    """Obtiene el saldo ACTUAL del cliente. 
    SIEMPRE llama a esta herramienta, nunca uses el historial.
    El argumento debe ser el ID numérico del cliente como string."""
    print(f"[DINÁMICO] Llamando a: http://localhost:8001/customer/{customer_id}")
    with httpx.Client() as client:
        try:
            response = client.get(f"http://localhost:8001/customer/{customer_id}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return f"El saldo ACTUAL del cliente {data.get('nombre')} (ID={customer_id}) es ${data.get('saldo')}."
        except httpx.ConnectError:
            return "Error: Servicio de clientes no disponible."
        except Exception as e:
            return f"Error consultando saldo: {str(e)}"

@tool
def get_tickets_count(customer_id: str) -> str:
    """Consulta el número de tickets de soporte técnico activos para un cliente. Requiere el ID del cliente como string."""
    print(f"[DINÁMICO] Llamando a: http://localhost:8002/tickets/count/{customer_id}")
    with httpx.Client() as client:
        try:
            response = client.get(f"http://localhost:8002/tickets/count/{customer_id}", timeout=5)
            print(f"Respuesta recibida: {response.text}") # Esto saldrá en tu consola
            response.raise_for_status()
            data = response.json()
            return f"El cliente ID={customer_id} tiene {data.get('tickets_abiertos', 0)} tickets abiertos."
        except httpx.ConnectError:
            return "Error: Servicio de tickets no disponible."
        except Exception as e:
            return f"Error consultando tickets: {str(e)}"

@tool
def get_security_report(service_name: str) -> str:
    """Obtiene el reporte de seguridad actual para un servicio específico.
         Útil para auditorías rápidas de estado de seguridad."""
    print(f"[DINÁMICO] Llamando a: http://localhost:8003/security/report/{service_name}")
    with httpx.Client() as client:
        try:
            response = client.get(f"http://localhost:8003/security/report/{service_name}", timeout=5)
            response.raise_for_status()
            return f"Reporte de seguridad de {service_name}: {response.json()}"
        except httpx.ConnectError:
            return "Error: Servicio de seguridad no disponible."
        except Exception as e:
            return f"Error consultando seguridad: {str(e)}"

# Lista para el agente
tools = [get_customer_name, get_customer_saldo, get_tickets_count, get_security_report]