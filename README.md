# ze-brands-test


# En desarrollo aplico lint y test
poetry exec lint
poetry exec test
poetry migrate

# Con docker-compose (dev)
docker compose up --build
y la API queda expuesta en http://localhost:8081

# Crear imagen y subirla a AWS ECR
Paso 1: Login a ECR
aws ecr create-repository --repository-name ze-brands-test
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

Paso 2: Construir y etiquetar imagen
docker build -t ze-brands-test .
docker tag ze-brands-test:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ze-brands-test:latest

Paso 3: Push a ECR
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ze-brands-test:latest


docker run --rm \
  --env-file .env \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ze-brands-test:latest \
  poetry run migrate
