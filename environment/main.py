from environment.variables import EnvironmentVariable
from environment.base import *
from datetime import timedelta
import dj_database_url

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Conditional Database Configuration
# Use Railway database if in PRODUCTION or MYSQL_LOCALLY is True
# Also default to Railway if we're in a containerized environment (Railway deployment)

# Debug: Print environment values
print(f"🔍 BACKEND_ENVIRONMENT: {EnvironmentVariable.BACKEND_ENVIRONMENT}")
print(f"🔍 MYSQL_LOCALLY: {EnvironmentVariable.MYSQL_LOCALLY}")
print(f"🔍 IS_RAILWAY: {EnvironmentVariable.IS_RAILWAY}")
print(f"🔍 DATABASE_URL: {EnvironmentVariable.DATABASE_URL[:50]}...")

# Force Railway database usage in these cases:
# 1. BACKEND_ENVIRONMENT is "PROD" 
# 2. MYSQL_LOCALLY is True
# 3. We're running on Railway platform
# 4. DATABASE_URL contains Railway domain
use_railway_db = (
    EnvironmentVariable.BACKEND_ENVIRONMENT == "PROD" or 
    EnvironmentVariable.MYSQL_LOCALLY or
    EnvironmentVariable.IS_RAILWAY or
    'railway.net' in EnvironmentVariable.DATABASE_URL or
    'railway' in EnvironmentVariable.DATABASE_URL.lower()
)

print(f"🔍 USE_RAILWAY_DB: {use_railway_db}")

# Always use Railway database if DATABASE_URL contains railway domain
if 'railway.net' in EnvironmentVariable.DATABASE_URL or use_railway_db:
    # Use dj-database-url to parse Railway's DATABASE_URL
    try:
        parsed_db = dj_database_url.parse(EnvironmentVariable.DATABASE_URL)
        DATABASES = {
            'default': {
                **parsed_db,
                'CONN_MAX_AGE': 60,
                'CONN_HEALTH_CHECKS': True,
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                },
            }
        }
        print(f"🚀 Using Railway MySQL Database: {parsed_db['HOST']}:{parsed_db['PORT']}")
        
    except Exception as e:
        print(f"❌ Failed to parse DATABASE_URL: {e}")
        # Fallback to manual Railway configuration
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'railway',
                'HOST': 'maglev.proxy.rlwy.net',
                'PORT': '11657',
                'USER': 'root',
                'PASSWORD': 'cuiZEjFTitdpdnljxrVkKjDIwZWgXFHg',
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                    'charset': 'utf8mb4',
                    'use_unicode': True,
                },
                'CONN_MAX_AGE': 60,
                'CONN_HEALTH_CHECKS': True,
            }
        }
        print("🔄 Using manual Railway database configuration")
    
else:
    # Use local database configuration
    DATABASES = {
        'default': { 
            'ENGINE': 'django.db.backends.mysql',
            'NAME': EnvironmentVariable.DATABASE_NAME,
            'HOST': EnvironmentVariable.DATABASE_HOST,
            'PORT': EnvironmentVariable.DATABASE_PORT,
            'USER': EnvironmentVariable.DATABASE_USERNAME,
            'PASSWORD': EnvironmentVariable.DATABASE_PASSWORD,
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
                'use_unicode': True,
            },
            'CONN_MAX_AGE': 60,
            'CONN_HEALTH_CHECKS': True,
        }
    }
    
    print("🏠 Using Local MySQL Database")

# SQLite fallback (uncomment if needed)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


AUTH_USER_MODEL = "user.User"


ALLOWED_HOSTS = [
    "*",  # Allow all hosts (you can restrict this later)
    "clashsphere-backend-production.up.railway.app",  # Railway Production URL
    "127.0.0.1",  # Local development
    "localhost",  # Local development
]

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
