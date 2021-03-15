#!/bin/sh

# prepare for barnyard2 and snorby
pass=$(cat /root/.mariadb_rootpw)
snort_pass=$(cat /etc/snort/.mariadb_snortpw)
# This creates snort and snorby databases for barnyard2 and snorby
cd /root/ || exit
sed -e "s/XXXXXX/${snort_pass}/" /root/snort.db > /root/snort.db2
mysql -uroot -p"${pass}" < /root/snort.db2
rm /root/snort.db2
sed -e "s/XXXXXX/${snort_pass}/" /root/barnyard2.conf.template > /root/barnyard2.conf
cp /root/barnyard2.conf /etc/snort/

# regenerate sid-msg.map, not needed unless the rules changes
# perl /usr/local/bin/create-sidmap.pl /etc/snort/rules > /etc/snort/rules/sid-msg.map

snort_pass=$(cat /etc/snort/.mariadb_snortpw)
sed -e "s/XXXXXX/${snort_pass}/" database.yml > /opt/rh/httpd24/root/var/www/html/snorby/config/database.yml

# shellcheck disable=SC1091
. /opt/rh/ruby193/enable

# Let snorby do its initilization now that the database is up and configured
cd /opt/rh/httpd24/root/var/www/html/snorby || exit
/opt/rh/ruby193/root/bin/bundle exec rake snorby:setup RAILS_ENV=production
