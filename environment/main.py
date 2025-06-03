from environment.variables import EnvironmentVariable
from environment.base import *
from datetime import timedelta
import dj_database_url

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Use dj-database-url to parse Railway's DATABASE_URL
DATABASES = {
    'default': dj_database_url.parse(
        EnvironmentVariable.DATABASE_URL,
        conn_max_age=60,
        conn_health_checks=True,
    )
}

# Add MySQL-specific options
DATABASES['default']['OPTIONS'] = {
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    'charset': 'utf8mb4',
    'use_unicode': True,
}

# Fallback configuration (commented out, but kept for reference)
# DATABASES = {
#     'default': { 
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': EnvironmentVariable.DATABASE_NAME,
#         'HOST': EnvironmentVariable.DATABASE_HOST,
#         'PORT': EnvironmentVariable.DATABASE_PORT,
#         'USER': EnvironmentVariable.DATABASE_USERNAME,
#         'PASSWORD': EnvironmentVariable.DATABASE_PASSWORD,
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'charset': 'utf8mb4',
#             'use_unicode': True,
#         },
#         'CONN_MAX_AGE': 60,
#         'CONN_HEALTH_CHECKS': True,
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


AUTH_USER_MODEL = "user.User"


ALLOWED_HOSTS = ["*"]

if EnvironmentVariable.DEBUG == "True":
    ALLOWED_HOSTS.append("127.0.0.1")


# JWT Configuration
JWT_SECRET_KEY = EnvironmentVariable.JWT_SECRET_KEY
JWT_ALGORITHM = "HS256"


# Cipher Configurations
CIPHER_SECRET_KEY = EnvironmentVariable.AES_SECRET_KEY
CIPHER_BLOCK_SIZE = 16

# Simple JWT Configurations
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2)
}
