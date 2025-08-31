#!/bin/sh
echo "Setting up database and seeding data..."

python -c "
import pymysql
import os

# SQL files to process in order
sql_files = ['on-duty.sql', 'off-duty.sql']

try:
    # Connect to MySQL (use 'db' for compose, 'localhost' for --network=host)
    db_host = os.getenv('DB_HOST', 'db')
    connection = pymysql.connect(
        host=db_host,
        user='webapp', 
        password='passworddevops3321',
        database='firefighters'
    )
    
    cursor = connection.cursor()
    
    # Process each SQL file
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            print(f'Processing {sql_file}...')
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            # Split SQL into individual statements and execute
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if not statement.startswith('SELECT'):  # Skip SELECT statements
                    try:
                        print(f'Executing: {statement[:50]}...')
                        cursor.execute(statement)
                        print('Success!')
                    except Exception as stmt_error:
                        if 'already exists' in str(stmt_error):
                            print('Table already exists, skipping...')
                        else:
                            print(f'Statement error: {stmt_error}')
        else:
            print(f'SQL file {sql_file} not found, skipping...')
    
    connection.commit()
    cursor.close()
    connection.close()
    print('Database seeding completed!')
    
except Exception as e:
    print(f'Connection error: {e}')
    print('Continuing without database seeding...')
"

echo "Starting Flask application..."
python App.py
