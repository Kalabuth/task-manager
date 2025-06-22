
````markdown
# 📝 Task Manager API

API RESTful para la gestión de tareas y listas de tareas. Permite a los usuarios registrarse, autenticarse, crear listas de tareas, gestionar tareas individuales y aplicar filtros por estado y prioridad. También calcula automáticamente el porcentaje de completitud de cada lista.

---

## 📌 Descripción del Proyecto

Este proyecto proporciona una API completa para manejar listas de tareas, desarrollada con **FastAPI**, **SQLAlchemy** y **PostgreSQL**. Las funcionalidades principales incluyen:

---

###  Funcionalidades del Proyecto

***Autenticación JWT**

  * Registro e inicio de sesión de usuarios mediante tokens JWT seguros.

  * **Registro**:
    Los usuarios pueden registrarse mediante una solicitud `POST` a `/api/v1/auth/register`, enviando un JSON como:

    ```json
    {
      "email": "usuario@example.com",
      "password": "123456"
    }
    ```

  * **Inicio de sesión (Login)**:
    Se realiza con una solicitud `POST` a `/api/v1/auth/login`, usando `form-data` con los campos:

    ```
    username=usuario@example.com
    password=123456
    ```

    La respuesta incluirá un campo `access_token` que debe usarse como token Bearer en las cabeceras de autorización:

    ```
    Authorization: Bearer <access_token>

***Gestión de Listas de Tareas**

  * CRUD completo de listas de tareas por usuario autenticado.

***Gestión de Tareas**

  * CRUD de tareas vinculadas a listas.
  * Asignación de:

    * **Estado**:
      `completed` (booleano) → `true` o `false`
    * **Prioridad** (valor numérico):

      * `1`: Alta
      * `2`: Media
      * `3`: Baja
    * **Usuario responsable** (opcional)

***Filtrado de Tareas**

  * Filtrado por `completed` (`true` / `false`) y por `priority` (`1`, `2`, `3`) en los listados por lista.

***Indicador de Completitud**

  * Se calcula y devuelve automáticamente el **porcentaje de tareas completadas** por lista.

***Cobertura de Tests**

  * Cobertura de pruebas superior al **90%** usando `pytest` y `coverage`.

---

## ⚙️ Configuración del entorno local

1. **Clona el repositorio**:

```bash
git clone https://github.com/kalabuth/task-manager-api.git
cd app
````

2. **Crea y activa un entorno virtual**:

```bash
python -m venv venv
source venv/bin/activate  # en Unix/macOS
venv\Scripts\activate     # en Windows
```

3. **Instala las dependencias**:

```bash
pip install -r requirements.txt
```

4. **Variables de entorno**

> ⚠️ Por practicidad y debido a que este proyecto es parte de una **prueba técnica**, el archivo `.env` ha sido incluido en el repositorio.
> En un entorno real, este archivo **no debe subirse** y se recomienda el uso de gestores de secretos como [Passbolt](https://www.passbolt.com/), [Vault](https://www.vaultproject.io/) o variables de entorno en tu proveedor cloud.

Contenido del archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/crehanna_db
SECRET_KEY=myjwtsecretkey
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin1234
POSTGRES_DB=crehanna_db
```

---

## 🐳 Ejecutar con Docker

### 1. Dockerizando solo la app (usando PostgreSQL local)

Si ya tienes PostgreSQL corriendo localmente, puedes usar `host.docker.internal` como host de base de datos para que el contenedor acceda al servicio local:

```env
# .env para uso con Docker y PostgreSQL local
DATABASE_URL=postgresql://user:password@host.docker.internal:5432/crehanna_db
```

```bash
docker-compose up --build
```

---

## 🧪 Ejecutar las pruebas

### En entorno local:

```bash
pytest --cov=app
```

### En Docker:

```bash
docker-compose exec app pytest --cov=app
```

> 🔍 La cobertura de pruebas actual es superior al **90%** ✅

---

## 📁 Estructura del Proyecto

```
├── app/
│   ├── api/
│   ├── aplication/
│   ├── core/
│   ├── infrastructure/
│   ├── schemas/
│   └── main.py
├── tests/
│   ├── test_integration/
│   └── test_unit/
├── docker-compose.yml
├── Dockerfile.yml
├── requirements.txt
├── .env
└── README.md
```

---

## ✍️ Autor

Juan Camilo Arias Calderón
[LinkedIn](https://www.linkedin.com/in/juan-ar/) | [GitHub](https://github.com/Kalabuth)

---
