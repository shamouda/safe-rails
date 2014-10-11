psql postgres -c "CREATE user rails with password 'rails';"
psql postgres -c "CREATE DATABASE rails;"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE rails to rails;"
