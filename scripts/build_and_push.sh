#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------
# Load env (from env/prod.env or ./prod.env)
# ------------------------------------
ENV_FILE=""
if [ -f "./env/prod.env" ]; then
  ENV_FILE="./env/prod.env"
elif [ -f "./prod.env" ]; then
  ENV_FILE="./prod.env"
fi

if [ -n "${ENV_FILE}" ]; then
  echo "==> Loading environment variables from ${ENV_FILE}"
  TMP_ENV="$(mktemp)"
  tr -d '\r' < "${ENV_FILE}" > "${TMP_ENV}"
  set -a
  # shellcheck disable=SC1090
  source "${TMP_ENV}"
  set +a
  rm -f "${TMP_ENV}"
else
  echo "==> No prod.env found at ./env/prod.env or ./prod.env — relying on already-exported env vars (if any)"
fi

# ------------------------
# Defaults & required env vars check
# ------------------------
: "${AWS_REGION:=us-east-1}"
: "${IMAGE_TAG:=latest}"
: "${CLUSTER_NAME:=ze-brands-cluster}"
: "${TASK_CPU:=512}"
: "${TASK_MEMORY:=1024}"

# Required explicit checks (fail fast with helpful messages)
: "${AWS_ACCOUNT_ID:?AWS_ACCOUNT_ID must be set (in env/prod.env or environment)}"
: "${ECR_REPOSITORY:?ECR_REPOSITORY must be set (in env/prod.env or environment)}"
: "${TASK_FAMILY:?TASK_FAMILY must be set}"
: "${SERVICE_NAME:?SERVICE_NAME must be set}"
: "${SUBNETS:?SUBNETS must be set (comma-separated)}"
: "${SECURITY_GROUPS:?SECURITY_GROUPS must be set (comma-separated)}"
: "${CONTAINER_PORT:?CONTAINER_PORT must be set (numeric)}"
: "${CONTAINER_NAME:?CONTAINER_NAME must be set}"
: "${TASK_EXECUTION_ROLE_ARN:?TASK_EXECUTION_ROLE_ARN must be set}"
: "${TASK_ROLE_ARN:?TASK_ROLE_ARN must be set}"

REPO_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}"

# Debug print
echo "==> Debug: key env vars"
echo "    AWS_ACCOUNT_ID = ${AWS_ACCOUNT_ID}"
echo "    AWS_REGION     = ${AWS_REGION}"
echo "    ECR_REPOSITORY = ${ECR_REPOSITORY}"
echo "    IMAGE_TAG      = ${IMAGE_TAG}"
echo "    CLUSTER_NAME   = ${CLUSTER_NAME}"
echo "    TASK_FAMILY    = ${TASK_FAMILY}"
echo "    SERVICE_NAME   = ${SERVICE_NAME}"
echo "    SUBNETS        = ${SUBNETS}"
echo "    SECURITY_GROUPS= ${SECURITY_GROUPS}"
echo "    CONTAINER_PORT = ${CONTAINER_PORT}"
echo "    TASK_EXEC_ROLE = ${TASK_EXECUTION_ROLE_ARN}"
echo "    TASK_ROLE_ARN  = ${TASK_ROLE_ARN}"

# validate CONTAINER_PORT is numeric
if ! [[ "${CONTAINER_PORT}" =~ ^[0-9]+$ ]]; then
  echo "ERROR: CONTAINER_PORT must be a number. Current value: '${CONTAINER_PORT}'" >&2
  exit 2
fi

# ------------------------
# Optional: create or update secret in Secrets Manager
# ------------------------
if [[ -n "${DB_SECRET_NAME:-}" && -n "${DB_SECRET_STRING:-}" ]]; then
  echo "==> Creating or updating secret ${DB_SECRET_NAME} in Secrets Manager..."
  if aws secretsmanager describe-secret --secret-id "${DB_SECRET_NAME}" --region "${AWS_REGION}" >/dev/null 2>&1; then
    echo "Secret exists -> updating value..."
    aws secretsmanager put-secret-value \
      --secret-id "${DB_SECRET_NAME}" \
      --secret-string "${DB_SECRET_STRING}" \
      --region "${AWS_REGION}"
  else
    echo "Secret does not exist -> creating..."
    aws secretsmanager create-secret \
      --name "${DB_SECRET_NAME}" \
      --description "Secret for ${TASK_FAMILY} DATABASE_URL" \
      --secret-string "${DB_SECRET_STRING}" \
      --region "${AWS_REGION}"
  fi

  DB_SECRET_ARN=$(aws secretsmanager describe-secret --secret-id "${DB_SECRET_NAME}" --region "${AWS_REGION}" --query 'ARN' --output text)
  export DB_SECRET_ARN
  echo "DB secret ARN: ${DB_SECRET_ARN}"
else
  echo "No DB_SECRET_NAME/DB_SECRET_STRING provided — skipping secret creation."
  export DB_SECRET_ARN="${DB_SECRET_ARN:-}"
fi

# ------------------------
# envsubst to generate raw task-def
# ------------------------
export REPO_URI AWS_REGION AWS_ACCOUNT_ID IMAGE_TAG TASK_FAMILY TASK_CPU TASK_MEMORY TASK_EXECUTION_ROLE_ARN TASK_ROLE_ARN CONTAINER_NAME CONTAINER_PORT DB_SECRET_ARN
if ! command -v envsubst >/dev/null 2>&1; then
  echo "ERROR: envsubst not found. Install gettext (which provides envsubst)." >&2
  exit 4
fi

envsubst < task-def.tpl.json > task-def.raw.json

# ------------------------
# Use jq to set containerPort as a NUMBER (defensive)
# ------------------------
if ! command -v jq >/dev/null 2>&1; then
  echo "WARNING: 'jq' not found. Attempting a python JSON sanity check..."
  python - <<PYCODE
import json,sys
try:
  json.load(open('task-def.raw.json'))
except Exception as e:
  print('JSON validation failed:',e)
  sys.exit(1)
print('task-def.raw.json parsed as JSON (no jq available).')
PYCODE
  # still try to continue; but prefer jq for robust patching
fi

# Patch containerPort into proper numeric field
if command -v jq >/dev/null 2>&1; then
  jq --argjson port "${CONTAINER_PORT}" \
     '.containerDefinitions[0].portMappings[0].containerPort = $port' task-def.raw.json > task-def.json
else
  # fallback: just copy (we validated JSON above)
  cp task-def.raw.json task-def.json
fi

# Validate final JSON
if ! jq . task-def.json >/dev/null 2>&1; then
  echo "ERROR: Generated task-def.json is invalid JSON. Check variables and template." >&2
  exit 3
fi

echo "Generated valid task-def.json"

# ------------------------
# Register task definition
# ------------------------
echo "==> Registering task definition..."
aws ecs register-task-definition --cli-input-json file://task-def.json --region "${AWS_REGION}"

# ------------------------
# Create cluster if missing
# ------------------------
echo "==> Creating cluster (if not exists): ${CLUSTER_NAME}"
if ! aws ecs describe-clusters --clusters "${CLUSTER_NAME}" --region "${AWS_REGION}" | grep -q '"clusterArn"'; then
  aws ecs create-cluster --cluster-name "${CLUSTER_NAME}" --region "${AWS_REGION}"
else
  echo "Cluster ${CLUSTER_NAME} exists."
fi

# ------------------------
# Create or update service
# ------------------------
echo "==> Creating or updating service ${SERVICE_NAME}..."

# Prepare arrays for JSON insertion
IFS=',' read -r -a SUBNET_ARR <<< "$SUBNETS"
IFS=',' read -r -a SG_ARR <<< "$SECURITY_GROUPS"
subnets_json=$(printf "\"%s\", " "${SUBNET_ARR[@]}" | sed 's/, $//')
sg_json=$(printf "\"%s\", " "${SG_ARR[@]}" | sed 's/, $//')

# Check if service exists
service_exists=false
if aws ecs describe-services --cluster "${CLUSTER_NAME}" --services "${SERVICE_NAME}" --region "${AWS_REGION}" --query 'services[0].serviceArn' --output text 2>/dev/null | grep -q "${SERVICE_NAME}"; then
  service_exists=true
fi

if [ "${service_exists}" = false ]; then
  echo "Service does not exist -> creating..."
  aws ecs create-service \
    --cluster "${CLUSTER_NAME}" \
    --service-name "${SERVICE_NAME}" \
    --task-definition "${TASK_FAMILY}" \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[${subnets_json}],securityGroups=[${sg_json}],assignPublicIp=ENABLED}" \
    --region "${AWS_REGION}"
  echo "Service ${SERVICE_NAME} created (or AWS responded)."
else
  echo "Service exists -> updating to use task-definition ${TASK_FAMILY} and forcing new deployment..."
  aws ecs update-service \
    --cluster "${CLUSTER_NAME}" \
    --service "${SERVICE_NAME}" \
    --task-definition "${TASK_FAMILY}" \
    --force-new-deployment \
    --region "${AWS_REGION}"
  echo "Service ${SERVICE_NAME} updated."
fi

echo "==> Deployment initiated. Use aws ecs describe-services to check status."
