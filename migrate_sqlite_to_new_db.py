import os
import subprocess
from django.core.management import call_command

# Global constants for DB credentials
DB_USER = 'my_user'  # Always use the same user
DB_PASSWORD = 'my_password'  # Always use the same password

def create_database(db_type, db_name, db_user, db_password, db_host='localhost', db_port=None):
    """Create a new database."""
    if db_type == 'postgresql':
        os.system(f"createdb -h {db_host} -p {db_port or '5432'} -U {db_user} {db_name}")
    elif db_type == 'mysql':
        os.system(f"mysql -u {db_user} -p{db_password} -e 'CREATE DATABASE {db_name};'")

def update_settings_with_new_db(db_type, db_name):
    """Update the Django settings.py file with the new database."""
    with open('myproject/settings.py', 'r+') as f:
        settings = f.read()
        new_db_config = f"""
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.{db_type}',
        'NAME': '{db_name}',
        'USER': '{DB_USER}',
        'PASSWORD': '{DB_PASSWORD}',
        'HOST': 'localhost',
        'PORT': '5432' if {db_type} == 'postgresql' else '3306',
    }}
}}
"""
        # Replace or append the database settings
        settings = settings.replace('DATABASES = { ... }', new_db_config)
        f.seek(0)
        f.write(settings)

def migrate_sqlite_to_new_db(db_name, db_type='postgresql'):
    """Migrate the SQLite database to a new PostgreSQL/MySQL database."""
    
    # Create the new database
    create_database(db_type, db_name, DB_USER, DB_PASSWORD)

    # Update settings.py to use the new database
    update_settings_with_new_db(db_type, db_name)

    # Dump data from SQLite
    call_command('dumpdata', output='data.json')

    # Migrate to the new database
    call_command('migrate')

    # Load data into the new database
    call_command('loaddata', 'data.json')

if __name__ == '__main__':
    # Pass the database name as an argument
    import sys
    if len(sys.argv) != 2:
        print("Usage: python migrate_sqlite_to_new_db.py <db_name>")
        sys.exit(1)

    db_name = sys.argv[1]
    migrate_sqlite_to_new_db(db_name)
