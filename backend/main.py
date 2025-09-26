# Usar versión mínima mientras se completa la migración
from main_minimal import app

if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8000)
