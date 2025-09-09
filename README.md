# Ze Brands Catalog API

**API** para la gestión de productos, marcas y usuarios, con autenticación **JWT**, desarrollada con **FastApi** sobre una arquitectura **hexagonal** centrada en **DDD**, 
permitiendo aislar la lógica de negocio en el dominio mientras abstrae las dependencias tecnológicas en la infraestructura,
facilitando cambios de tecnología, escalabilidad y mantenibilidad de manera más ágil.

Los usuarios ADMIN podrán crear/actualizar/eliminar productos y también podrán crear/actualizar/eliminar otros usuarios ADMIN.
Al momento de actualizar un producto se notifica vía email empleando el servicio **AWS SES**. 

Los usuarios ANONYMOUS solo pueden consultar los detalles de productos, y al consultarlo se incrementa el número de vistas del producto. 
Se expone adicionalmente un endpoint para consultar un reporte de visualizaciones de productos con filtro opcional de marca.

Se desarrollaron pruebas unitarias y de integración en código y con una **test suite** programada en **Postman con JS**.

Se aplicaron buenas prácticas como el uso de **uff linter**, gestor de dependencias **poetry**, configuración de **pre-commits**, cobertura de test, 
contenerización de la api con docker en local y en un **ECS** con **ECR** de **AWS**,
documentación de la API con **swagger**, entre otras.

---

## ⚙️ Pre-requisitos

- **Postgres database**  
- Crear la base de datos **ze_brands_test** (o la que establezca en su .env)
- Definir variables de entorno en un archivo `.env`.  
  Ejemplo de variables utilizadas:

| Variable | Descripción                                                   | Ejemplo |
|----------|---------------------------------------------------------------|---------|
| `DEV_PORT` | Puerto en el que se ejecuta la API                          | `8083` |
| `DATABASE_URL` | Conexión a la base de datos                             | `postgresql+psycopg2://postgres:postgres@localhost:5432/ze_brands_test` |
| `AUTO_MIGRATE` | Aplicar migraciones automáticamente al levantar la API  | `true` |
| `MIGRATION_PATH` | Ruta de migraciones                                   | `migrations` |
| `SECRET_KEY` | Llave secreta para JWT                                    | `supersecretkey12345` |
| `ALGORITHM` | Algoritmo de JWT                                           | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Minutos de expiración del token JWT      | `60` |
| `DEFAULT_ADMIN_USERNAME` | Usuario administrador por defecto             | `administrator` |
| `DEFAULT_ADMIN_PASSWORD` | Contraseña administrador por defecto          | `Adm1n1str@tor` |
| `DEFAULT_ADMIN_EMAIL` | Email administrador por defecto                  | `admin@gmail.com` |
| `SES_REGION_NAME` | Región AWS SES                                       | `us-east-1` |
| `SES_SENDER_EMAIL` | Email remitente de notificaciones                   | `no-reply@your-domain.com` |
| `SES_RECIPIENT_EMAIL` | Email destinatario de notificaciones             | `notify@your-domain.com` |
| `AWS_ACCESS_KEY_ID` | Access Key de AWS                                  | `***` |
| `AWS_SECRET_ACCESS_KEY` | Secret Key de AWS                              | `***` |
| `AWS_DEFAULT_REGION` | Región de AWS                                     | `us-east-1` |

Exportar las variables:
```bash
source .env
```

---

## 🚀 Ejecución del proyecto

### 1. Instalar dependencias
```bash
poetry install
```

### 2. Activar el entorno virtual
```bash
source .venv/bin/activate
# o
poetry shell
```

### 3. Linter
```bash
poetry exec lint
```

### 4. Tests
```bash
poetry exec test
```

### 5. Migraciones
Automáticamente al levantar la API se aplican migraciones, pero también pueden correrse manualmente:
```bash
poetry exec migrate
poetry run migrate-up
```

### 6. Levantar la API
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port ${DEV_PORT:-8000}
```

### 7. Documentación
- **Swagger UI** → [http://localhost:8080/docs](http://localhost:8080/docs)  
- **Redoc** → [http://0.0.0.0:8080/](http://0.0.0.0:8080/)  

📸 Documentación API:  
![Swagger y Redoc](images/openapi-documentation.png)

---

## 🔐 Seguridad

- Creación de usuarios con **password hasheado**  
- **Login con JWT**  
- **Autorización por roles** en los endpoints  
- Usuarios deben estar **verificados** para ciertas operaciones  
- Notificación de cambios de usuario vía **AWS SES**  
- Debe configurar sus credenciales de AWS y los usuarios para SES deben estar verificados

📸 Ejemplo de notificación:  
![Notificación de cambios con SES](images/notify-product-changes.png)

---

## 🛠️ Buenas prácticas

He aplicado **arquitectura hexagonal centrada en Domain-Driven Design (DDD)**, lo cual favorece el uso de patrones **SOLID** y fomenta buenas prácticas de desarrollo.  

### Dependencias clave y buenas prácticas aplicadas

- **[Poetry](https://python-poetry.org/)** → Gestión de dependencias y entornos virtuales.  
- **[Ruff](https://github.com/astral-sh/ruff)** → Linter rápido que asegura calidad del código.  
- **[Black](https://black.readthedocs.io/)** → Formateador automático para mantener estilo consistente.  
- **[Lagom](https://github.com/meadsteve/lagom)** → Inyección de dependencias que facilita pruebas y modularidad.  
- **[Yoyo Migrations](https://ollycope.com/software/yoyo/latest/)** → Migraciones de base de datos versionadas. 
- **[Pytest](https://docs.pytest.org/)** → Framework de testing simple y potente.  
- **[Pre-commit](https://pre-commit.com/)** → Automatización de validaciones antes de cada commit.  
- Cobertura de tes con pytest-cov

Con estas dependencias se logra:  
- Código más mantenible y consistente.  
- Facilidad para pruebas unitarias y de integración.  
- Separación clara de responsabilidades.  
- Escalabilidad y flexibilidad en la evolución del sistema.  

### Pre-commit hooks configurados

- Linter (**Ruff, Black, isort**)  
- Tests (**pytest**)  
- Formateo de código y validaciones de commits  

```bash
poetry run pre-commit clean
poetry run pre-commit install
poetry run pre-commit run --all-files
```
![img.png](images/pre-commit.png)

📸 Test suite:  
![Tests y cobertura](images/suite-test.png)

📸 Coverage test:  
![test.png](images/test-and-cov.png)

- Tests de integración con DB simulada
- Cobertura actual: **142 tests → 90% coverage**

---
### Test suite
Como buena práctica se automatizó en POSTMAN una suite de pruebas con Javascript

Esta suite contiene el HAPPY PATH del ejercicio y también flujos de validaciones: qué puede hacer un ADMIN/ANONYMOUS
![test-postman-suite.png](images/test-postman-suite.png)

                    
Para usar esta suite de pruebas solo debe configurar las siguientes variables de entorno según haya configurado su .ENV
![test-postman-suite-env.png](images/test-postman-suite-env.png)

---

## 📂 Recursos adicionales

- `OpenAPI Spec` → [📄 documentation/openapi.yml](documentation/openapi.yml)  
  Que puede renderizar en https://editor.swagger.io/

- `Colección de Postman` → [📄 documentation/ZeBrands Catalog API.postman_collection.json](documentation/ZeBrands_Catalog_API.postman_collection.json)

- `Variables de entorno Postman` → [📄 documentation/LOCAL.postman_environment.json](documentation/LOCAL.postman_environment.json)

---

## 📦 Docker & Despliegue (pendiente)
1. Despliegue local

    He creado `README_DEPLOY_LOCAL.md` para abordar los temas de contenedores

    Aquí explico cómo levantar la API en un entorno local con docker
    
    [📄 README_DEPLOY_LOCAL.md](README_DEPLOY_LOCAL.md)  

2. Despliegue en AWS

    He creado `README_DEPLOY_PROD.md` para abordar despliegue en un AWS
    Aquí explico cómo desplegar con docker en un entorno real de AWS.

    Importante:  tu máquina local debe contar con el perfil de AWS configurado en ~/.aws/credentials y ~/.aws/config (con tu aws_access_key_id, aws_secret_access_key, region, etc.)

    [📄 README_DEPLOY_PROD.md](README_DEPLOY_PROD.md)  

---

## 🔗 Repositorio
```bash
git clone git@github.com:grleyvaj/ze-brands-demo.git
```
