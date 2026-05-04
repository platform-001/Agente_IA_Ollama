from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Microservicio de Tickets")

TICKETS_DATA = {
    "123": 8,
    "456": 5,
    "789": 5
}

@app.get("/tickets/count/{customer_id}")
def get_tickets_count(customer_id: str):
    num_tickets = TICKETS_DATA.get(customer_id)
    
    if num_tickets is None:
        # Si no existe el cliente en la base de tickets, lanzamos error 404
        raise HTTPException(status_code=404, detail=f"No se encontró información para el ID {customer_id}")
    
    # 
    return {
        "customer_id": customer_id,
        "tickets_abiertos": num_tickets,
        "mensaje": f"El cliente {customer_id} tiene {num_tickets} tickets abiertos."
    }

if __name__ == "__main__":
    # Puerto 8002 para que conviva con el de clientes en el 8001
    uvicorn.run(app, host="0.0.0.0", port=8002)