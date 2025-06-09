DESCRIPCION:

- FastAPI como framework 
- SQLAlchemy como ORM
- PostgreSQL como base de datos
- Pydantic para validación de datos

CONFIGURACIÓN:

  En databe.py configurar tu usuario y contraseña de PostgresSQL
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate    # Windows
  pip install -r requirements.txt
  pip install fastapi sqlalchemy psycopg2-binary uvicorn pydantic # Si no funciona el requirements.txt

  Configurar la base de datos (tienda_ropa) en PostgreSQL y modificar los credenciales en database.py 

EJECUCIÓN:

  uvicorn app:app --reload

VISUALIZACIÓN:

http://localhost:8000/docs