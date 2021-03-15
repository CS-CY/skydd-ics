#!/bin/bash
if [ -f /root/icingaweb_pwd ]; then
    echo "Already run"
    exit 1
fi
sed -i 's/;date.timezone =/date.timezone = Europe\/Stockholm/' /etc/php.ini
# Configure database
/usr/bin/postgresql-setup initdb
systemctl enable postgresql
systemctl start postgresql
cat << EOF > /var/lib/pgsql/data/pg_hba.conf

# icinga
local   all             all                                     trust
local   icinga          icinga                                  md5
host    icinga          icinga          127.0.0.1/32            md5
host    icinga          icinga          ::1/128                 md5
# icingaweb
local   icingaweb       icingaweb                               md5
host    icingaweb       icingaweb       127.0.0.1/32            md5
host    icingaweb       icingaweb       ::1/128                 md5
EOF
systemctl restart postgresql

cd /tmp || exit
# icinga2
icinga_pw=$(openssl rand -hex 32)
sudo -u postgres psql -c "CREATE ROLE icinga WITH LOGIN PASSWORD '${icinga_pw}'";
sudo -u postgres createdb -O icinga -E UTF8 icinga
export PGPASSWORD=${icinga_pw}
psql -U icinga -d icinga < /usr/share/icinga2-ido-pgsql/schema/pgsql.sql

# setup ido db configuration
cat << EOF > /etc/icinga2/features-available/ido-pgsql.conf
/**
 * The db_ido_pgsql library implements IDO functionality
 * for PostgreSQL
 */
library "db_ido_pgsql"

object IdoPgsqlConnection "ido-pgsql" {
  user = "icinga"
  password = "${icinga_pw}"
  host = "localhost"
  database = "icinga"
}
EOF
chown icinga:icinga /etc/icinga2/features-available/ido-pgsql.conf
chmod 640 /etc/icinga2/features-available/ido-pgsql.conf

# icingaweb2
icingaweb_pw=$(openssl rand -hex 32)
sudo -u postgres psql -c "CREATE ROLE icingaweb WITH LOGIN PASSWORD '${icingaweb_pw}'";
sudo -u postgres createdb -O icingaweb -E UTF8 icingaweb
export PGPASSWORD=${icingaweb_pw}
psql -U icingaweb -d icingaweb < /usr/share/doc/icingaweb2/schema/pgsql.schema.sql
# Create a hardcoded password for the admin user
icingaweb_user_pwd=$(openssl rand -hex 16)
touch /root/icingaweb_pwd
/bin/chown 600 /root/icingaweb_pwd
echo "admin:${icingaweb_user_pwd}" > /root/icingaweb_pwd
user_password=$(openssl passwd -1 "${icingaweb_user_pwd}")
psql -U icingaweb -d icingaweb -c "insert into icingaweb_user (name, active, password_hash) values ('admin', 1, '${user_password}');"
sed -i s/p_slumptal_p/${icingaweb_user_pwd}/g /var/www/html/foss/doc/index.html
cat << EOF > /etc/icingaweb2/resources.ini
[icingaweb_db]
type = "db"
db = "pgsql"
host = "localhost"
port = "5432"
dbname = "icingaweb"
username = "icingaweb"
password = "${icingaweb_pw}"
charset = ""
persistent = "0"

[icinga_ido]
type = "db"
db = "pgsql"
host = "localhost"
port = "5432"
dbname = "icinga"
username = "icinga"
password = "${icinga_pw}"
charset = ""
persistent = "0"
EOF

cat << EOF > /etc/icingaweb2/config.ini
[global]
show_stacktraces = "0"
config_backend = "db"
config_resource = "icingaweb_db"

[logging]
log = "syslog"
level = "ERROR"
application = "icingaweb2"
EOF

cat << EOF > /etc/icingaweb2/groups.ini
[icingaweb2]
backend = "db"
resource = "icingaweb_db"
EOF

cat << EOF > /etc/icingaweb2/authentication.ini
[icingaweb2]
backend = "db"
resource = "icingaweb_db"
EOF

cat << EOF > /etc/icingaweb2/roles.ini
[Administrators]
users = "admin"
permissions = "*"
groups = "Administrators"
EOF
chown apache:icingaweb2 /etc/icingaweb2/*.ini
chmod 640 /etc/icingaweb2/*.ini

mkdir -p "/etc/icingaweb2/modules/monitoring"
chown root:icingaweb2 /etc/icingaweb2/modules
chmod  770 /etc/icingaweb2/modules
chmod  g+s /etc/icingaweb2/modules
chown apache:icingaweb2 /etc/icingaweb2/modules/monitoring
chmod  2770 /etc/icingaweb2/modules/monitoring
cat << EOF > /etc/icingaweb2/modules/monitoring/config.ini
[security]
protected_customvars = "*pw*,*pass*,community"
EOF

cat << EOF > /etc/icingaweb2/modules/monitoring/backends.ini
[icinga]
type = "ido"
resource = "icinga_ido"
EOF

cat << EOF > /etc/icingaweb2/modules/monitoring/commandtransports.ini
[icinga2]
transport = "local"
path = "/var/run/icinga2/cmd/icinga2.cmd"
EOF
chown apache:icingaweb2 /etc/icingaweb2/modules/monitoring/*.ini
chmod 660 /etc/icingaweb2/*.ini
mkdir /etc/icingaweb2/enabledModules
chown apache:icingaweb2 /etc/icingaweb2/enabledModules
chmod 2770 /etc/icingaweb2/enabledModules
ln -s /usr/share/icingaweb2/modules/monitoring /etc/icingaweb2/enabledModules


#icingacli setup token create
/usr/sbin/icinga2 feature enable command
/sbin/restorecon -e /sys -R /
systemctl restart icinga2


