from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Microservicio de Clientes")

# Base de datos local 
CUSTOMERS_DB = {
    "123": {"nombre": "Juan Pérez", "saldo": 120},
    "456": {"nombre": "Ana García", "saldo": 90},
    "789": {"nombre": "Carlos Ruiz", "saldo": 300}
}

@app.get("/customer/{customer_id}")
def read_customer(customer_id: str):
    cliente = CUSTOMERS_DB.get(customer_id)
    
    if not cliente:
        # devuelve un error 404 
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
        
    # Devolvemos el objeto 
    return {
        "id": customer_id,
        "nombre": cliente["nombre"],
        "saldo": cliente["saldo"],
        "mensaje": f"El cliente {cliente['nombre']} tiene un saldo de ${cliente['saldo']}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)