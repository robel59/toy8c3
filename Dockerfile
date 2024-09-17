# Use Python 3.8.10 base image
FROM python:3.8.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Install PostgreSQL or MySQL client (depending on which DB you're using)
# For PostgreSQL:
RUN apt-get update && apt-get install -y postgresql-client

# For MySQL:
# RUN apt-get update && apt-get install -y default-mysql-client

# Copy and run the database migration script
COPY migrate_sqlite_to_new_db.py /app/migrate_sqlite_to_new_db.py

# Run the migration script as part of the build process
RUN python migrate_sqlite_to_new_db.py

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
