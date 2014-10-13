
echo "export PATH=$PATH:/usr/lib/postgresql/9.3/bin/" >> ~/.bashrc
echo "export PGDATA=/mnt/external/PGDATA" >> ~/.bashrc
source ~/.bashrc

sudo mkfs.ext4 /dev/xvdc
sudo mkdir /mnt/external
sudo mount /dev/xvdc /mnt/external
sudo /etc/init.d/postgresql stop
sudo chmod -R go+rw /mnt/external/
pg_ctl init
/usr/lib/postgresql/9.3/bin/postgres -D /mnt/external/PGDATA
