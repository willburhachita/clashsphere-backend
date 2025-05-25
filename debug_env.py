#!/usr/bin/env python3
import os
from decouple import config

print("=== Environment Variables Debug ===")
print(f"MYSQL_DATABASE: {config('MYSQL_DATABASE', 'NOT_SET')}")
print(f"RAILWAY_TCP_PROXY_DOMAIN: {config('RAILWAY_TCP_PROXY_DOMAIN', 'NOT_SET')}")
print(f"RAILWAY_TCP_PROXY_PORT: {config('RAILWAY_TCP_PROXY_PORT', 'NOT_SET')}")
print(f"MYSQLUSER: {config('MYSQLUSER', 'NOT_SET')}")
print(f"MYSQL_ROOT_PASSWORD: {config('MYSQL_ROOT_PASSWORD', 'NOT_SET')}")

print("\n=== All Railway-related environment variables ===")
for key, value in os.environ.items():
    if 'MYSQL' in key or 'RAILWAY' in key:
        # Hide password for security
        if 'PASSWORD' in key:
            print(f"{key}: {'*' * len(value) if value else 'NOT_SET'}")
        else:
            print(f"{key}: {value}")

print("\n=== Database configuration as loaded ===")
try:
    from environment.variables import EnvironmentVariable
    print(f"DATABASE_NAME: {EnvironmentVariable.DATABASE_NAME}")
    print(f"DATABASE_HOST: {EnvironmentVariable.DATABASE_HOST}")
    print(f"DATABASE_PORT: {EnvironmentVariable.DATABASE_PORT}")
    print(f"DATABASE_USERNAME: {EnvironmentVariable.DATABASE_USERNAME}")
    print(f"DATABASE_PASSWORD: {'*' * len(EnvironmentVariable.DATABASE_PASSWORD) if EnvironmentVariable.DATABASE_PASSWORD else 'NOT_SET'}")
except Exception as e:
    print(f"Error loading EnvironmentVariable: {e}") 