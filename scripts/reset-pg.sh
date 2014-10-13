
sudo chown -R ubuntu /var/run/postgresql

pg_ctl stop
rm -rf /mnt/external/PGDATA
pg_ctl init -D /mnt/external/PGDATA
echo "shared_buffers = 30GB" >> /mnt/external/PGDATA/postgresql.conf
echo "host all all             all           trust" >> /mnt/external/PGDATA/pg_hba.conf
{ /usr/lib/postgresql/9.3/bin/postgres -D /mnt/external/PGDATA & }
sleep 2; psql postgres -c "CREATE USER rails WITH PASSWORD 'rails'"; psql postgres -c "CREATE DATABASE rails"; psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE rails to rails";
cd ../demo
rake db:migrate
wait
