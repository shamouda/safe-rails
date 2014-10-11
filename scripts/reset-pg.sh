
pg_ctl stop
rm -rf /mnt/external/PGDATA
pg_ctl init -D /mnt/external/PGDATA
/usr/lib/postgresql/9.3/bin/postgres -D /mnt/external/PGDATA
