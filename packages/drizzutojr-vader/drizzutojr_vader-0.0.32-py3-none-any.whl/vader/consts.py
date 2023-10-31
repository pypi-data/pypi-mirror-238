import os

SERVICE_NAME = os.environ["SERVICE_NAME"]

CORE_SERVICE_URL = os.environ["CORE_SERVICE_URL"]
POLICY_SERVICE_URL = os.environ["POLICY_SERVICE_URL"]
AUTH_SERVICE_URL = os.environ["AUTH_SERVICE_URL"]
SECRETS_SERVICE_URL = os.environ["SECRETS_SERVICE_URL"]

# The following are values that can be overwritten in the individual consts files for each service

LOG_DIR = os.environ.get("LOG_DIR", "/var/log/vader")

DEFAULT_LOG_FILE = f"{LOG_DIR}/default.log"
AUDIT_LOG_FILE = f"{LOG_DIR}/audit.log"
ERROR_LOG_FILE = f"{LOG_DIR}/error.log"
ACCESS_LOG_FILE = f"{LOG_DIR}/access.log"

POLICY_TEMPLATE_DIR = "policy_templates"

OPENAPI_DIR = "openapi"
OPENAPI_FILE = "swagger.yml"
OPENAPI_PATH = f"{OPENAPI_DIR}/{OPENAPI_FILE}"

VADER_DEBUG = bool(os.environ.get("VADER_DEBUG", False))

VADER_APP_ID = "0001"
VADER_ROOT_BOUNDARY_ID = "vader"

STARTING_NAMESPACE = "admin/"

OPS_KV = "ops-kv"

MIN_STRING_LENGTH = 20
MAX_STRING_LENGTH = 100

TOKEN_TYPES = ["batch", "service"]

DEFAULT_MAX_TOKEN_TTL = "8h"
DEFAULT_MIN_TOKEN_TTL = "10m"

DEFAULT_MAX_TOKEN_MAX_TTL = DEFAULT_MAX_TOKEN_TTL
DEFAULT_MIN_TOKEN_MAX_TTL = DEFAULT_MIN_TOKEN_TTL

DEFAULT_MAX_TOKEN_BOUND_CIDRS = 20
DEFAULT_MIN_TOKEN_BOUND_CIDRS = 0
DEFAULT_INVALID_TOKEN_BOUND_CIDRS = ["127.0.0.1", "0.0.0.0"]

# VADER Directory
VADER_DIR = "/etc/vader"

# AZURE DEFAULTS - can be overridden with env variable AZURE_CREDS_FILE
DEFAULT_AZURE_CREDS_FILE = f"{VADER_DIR}/azure.json"

# MONGO DEFAULTS - can be overridden with env variable MONGO_CREDS_FILE
DEFAULT_MONGO_CREDS_FILE = f"{VADER_DIR}/mongo.json"
