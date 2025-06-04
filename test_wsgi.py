#!/usr/bin/env python
"""
Test script to verify WSGI application can be imported and initialized
"""
import os
import sys
import django
from django.conf import settings

def test_wsgi():
    try:
        print("🧪 Testing WSGI application import...")
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'environment.main')
        
        # Test Django setup
        django.setup()
        print("✅ Django setup successful")
        
        # Test WSGI import
        from common.wsgi import application
        print("✅ WSGI application imported successfully")
        
        # Test basic Django components
        from django.core.management import execute_from_command_line
        print("✅ Django management commands available")
        
        # Test database configuration (without connecting)
        from django.conf import settings
        print(f"✅ Database engine: {settings.DATABASES['default']['ENGINE']}")
        
        print("🎉 All WSGI tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ WSGI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_wsgi()
    sys.exit(0 if success else 1) 