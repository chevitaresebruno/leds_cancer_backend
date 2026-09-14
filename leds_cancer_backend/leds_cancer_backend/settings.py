"""
Django settings for leds_cancer_backend project.
Variáveis sensíveis são lidas do arquivo .env via python-decouple.
"""

from datetime import timedelta
from pathlib import Path
from typing import Any

from decouple import Csv, config

# ─── Paths ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Segurança ────────────────────────────────────────────────────────────────

SECRET_KEY: str = config("SECRET_KEY")
DEBUG: bool = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", default="localhost", cast=Csv())

# ─── CORS ─────────────────────────────────────────────────────────────────────

CORS_ALLOWED_ORIGINS: list[str] = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173",
    cast=Csv(),
)

# ─── Apps ─────────────────────────────────────────────────────────────────────

INSTALLED_APPS: list[str] = [
    # Django Internal
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third Party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    # Self Apps
    "authentication",
    "patients",
    "exams",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "leds_cancer_backend.urls"

TEMPLATES: list[Any] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "leds_cancer_backend.wsgi.application"

# ─── Banco de dados ───────────────────────────────────────────────────────────

_database_url: str = config("DATABASE_URL", default="")

if _database_url:
    import dj_database_url  # type: ignore[import-untyped]

    DATABASES: dict[str, Any] = {"default": dj_database_url.parse(_database_url)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─── Autenticação ─────────────────────────────────────────────────────────────

AUTH_USER_MODEL = "authentication.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Django REST Framework ────────────────────────────────────────────────────

REST_FRAMEWORK: dict[str, Any] = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ─── JWT ──────────────────────────────────────────────────────────────────────

SIMPLE_JWT: dict[str, Any] = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=config("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=30, cast=int)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=config("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7, cast=int)
    ),
}

# ─── drf-spectacular ─────────────────────────────────────────────────────────

SPECTACULAR_SETTINGS = {
    "TITLE": "LEDS Cancer API",
    "DESCRIPTION": "API do sistema de análise de mamografias — LEDS Cancer",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "TAGS": [
        {"name": "Autenticação", "description": "Login, registro e perfil do usuário"},
        {"name": "Pacientes", "description": "Gerenciamento de pacientes"},
        {"name": "Exames", "description": "Criação e consulta de exames de mamografia"},
        {"name": "Dashboard", "description": "Estatísticas e resumo do sistema"},
    ],
}

# ─── Image token (HMAC) ──────────────────────────────────────────────────────
# Chave secreta dedicada para assinar tokens de imagem.
# Se não definida, usa o SECRET_KEY do Django como fallback.
IMAGE_TOKEN_SECRET: str = config("IMAGE_TOKEN_SECRET", default=SECRET_KEY)
# Tempo de vida do token em segundos (padrão: 15 min)
IMAGE_TOKEN_TTL_SECONDS: int = config("IMAGE_TOKEN_TTL_SECONDS", default=900, cast=int)

# ─── Internacionalização ──────────────────────────────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ─── Arquivos estáticos e de mídia ────────────────────────────────────────────

STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
