from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Microservicio vulnerabilidades")

VULNERABILITIES_DB = {
    "auth-service": {"critical": 3, "high": 5, "medium": 0},
    "payment-api": {"critical": 0, "high": 0, "medium": 2},
    "gateway": {"critical": 0, "high": 1, "medium": 0}
}

@app.get("/security/report/{service_name}")

def get_security_report(service_name: str):
    service_key = service_name.lower()
    report = VULNERABILITIES_DB.get(service_key)
    
    if not report:
        return {
            "service": service_name,
            "status": "No se encontraron reportes",
            "mensaje": f"No hay información de seguridad disponible para el servicio: {service_name}"
        }
    
    
    summary = f"{report['critical']} Críticas, {report['high']} Altas, {report['medium']} Medias"
    
    return {
        "service": service_name,
        "vulnerabilidades": report,
        "resumen": summary,
        "mensaje": f"Reporte de seguridad para {service_name}: {summary}"
    }

if __name__ == "__main__":
    # Puerto 8003 para mantener el orden
    uvicorn.run(app, host="0.0.0.0", port=8003)