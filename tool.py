import httpx
from langchain_core.tools import tool

@tool
def get_customer_info(customer_id: str) -> str:
    """Usa esta herramienta cuando necesites obtener el nombre y saldo de un cliente.
         El argumento debe ser el ID numérico del cliente como string."""
    print(f"Llamando a: http://localhost:8001/customer/{customer_id}")
    with httpx.Client() as client:
        try:
            response = client.get(f"http://localhost:8001/customer/{customer_id}", timeout=5)
            print(f"Respuesta recibida: {response.text}") # Esto saldrá en tu consola
            response.raise_for_status()
            data = response.json()
            return f"Cliente {data.get('nombre')}: Saldo ${data.get('saldo')}. {data.get('mensaje')}"
        except httpx.ConnectError:
            return "Error: Servicio de clientes no disponible."
        except Exception as e:
            return f"Error consultando cliente: {str(e)}"

@tool
def get_tickets_count(customer_id: str) -> str:
    """Consulta el número de tickets de soporte técnico activos para un cliente. Requiere el ID del cliente como string."""
    print(f"Llamando a: http://localhost:8002/tickets/count/{customer_id}")
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
tools = [get_customer_info, get_tickets_count, get_security_report]