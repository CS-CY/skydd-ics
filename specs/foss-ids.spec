# No debuginfo:
%define debug_package %{nil}
%define name      foss-ids
%define summary   Server for watching network traffic with alert rules
%if 0%{?_version:1}
%define version %{_version}
%else
%define version   1.0
%endif
%if 0%{?_buildtag:1}
%define release %{_buildtag}
%else
%define release 1
%endif
%define license   sysctl license
%define group     system/file
%define source    %{name}-%version.tar.gz
%define url       https://sysctl.se
%define vendor    sysctl
%define packager  sysctl packaging team
%define buildroot %{_tmppath}/%{name}-root
%define _prefix   /
%global __requires_exclude %{?__requires_exclude}|perl\\(config\.pl

Name:      %{name}
Summary:   %{summary}
Version:   %{version}
Release:   %{release}
License:   %{license}
Group:     %{group}
Source0:   %{source}
BuildArch: x86_64
Requires:  foss-httpd, foss-common, foss-ids-repo, daq, mariadb-server, v8314, ruby193, ruby193-ruby-devel, rh-passenger40, rh-passenger40-ruby193, httpd24, mod_proxy_html, libnet, libdnet-progs, snort, ruby193-rubygem-bundler, ruby193-rubygem-rake
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Server watching network traffic on all its connected interfaces, applying snort rules to traffic
and generating alerts which can be seen in the Snorby interface that comes installed

%prep

%build
# Build a selinux policy to allow NetworkManager to start a snort service
cd %{_srcdir}
make -f /usr/share/selinux/devel/Makefile

%install
pushd %{_srcdir}
mkdir -p  %{buildroot}/usr/share/selinux/packages/foss-ids
cp  %{_srcdir}/*.pp  %{buildroot}/usr/share/selinux/packages/foss-ids
cp -r usr etc opt root %{buildroot}

%pre

%post
touch /opt/.foss-ids
if [ $1 -eq 1 ];then
    #install
    /bin/ln -s /usr/lib64/libnet.so.1 /usr/lib64/libdnet.so.1
    # XXX fixa med %files
    /bin/ln -sf /etc/snort/rules/community-rules/community.rules /etc/snort/rules/community.rules
    /bin/ln -sf /etc/snort/rules/quickdraw/all-quickdraw.rules /etc/snort/rules/all-quickdraw.rules

    # create-sidmap.pl is from the Oinkmaster repo. Needed for regenerating the sid-msg.map used by
    # barnyard2 to map snort rule ids (SID) to a message.

    # Copy the result of what bundle install --deployment would have done (gem install lots of files..)
    #tar xzpf $base/ruby193-gems.tgz -C /opt/rh/
    # tar xzpf $base/vendor-bundle.tgz -C /var/www/html/snorby/

    mariadb_rootpw=$(/bin/pwgen -1 48)
    echo -n $mariadb_rootpw > /root/.mariadb_rootpw
    /bin/chmod 600 /root/.mariadb_rootpw

    mariadb_snortpw=$(/bin/pwgen -1 48)
    echo -n $mariadb_snortpw > /etc/snort/.mariadb_snortpw
    /bin/chmod 600 /etc/snort/.mariadb_snortpw

    /bin/ln -sf /var/www/html/foss /opt/rh/httpd24/root/var/www/html/snorby/public/foss
    touch /var/log/snort/barnyward2.waldo
    chown snort /var/log/snort/barnyward2.waldo
fi
# Always create a new not hardcoded token
token=$(openssl rand -hex 129)
echo "Snorby::Application.config.secret_token = '${token}'" > /opt/rh/httpd24/root/var/www/html/snorby/config/initializers/secret_token.rb

# httpd24 needs to listen non port 81 to not conflict with system httpd that has foss docs
sed -i 's/Listen 80/Listen 127.0.0.1:81/g' /opt/rh/httpd24/root/etc/httpd/conf/httpd.conf

systemctl restart httpd24-httpd.service
systemctl restart network

# set correct selinux labels
/sbin/restorecon -R /var /etc /usr

%clean
rm -rf %{buildroot}

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-ids
fi

%files
%defattr(-,root,root)
     %config(noreplace)          /etc/sysctl.d/88-ids.conf
     %attr(0644, root, root)     /etc/skel/Desktop/L*Snorby.desktop
     %attr(0644, root, root)     /etc/skel/Desktop/firefox_ids.desktop
     %attr(0644, root, root)     /etc/xdg/autostart/firefox_ids_autostart.desktop
%dir %attr(0755, root, root)     /usr/share/selinux/packages/foss-ids
     %attr(0644, root, root)     /usr/share/selinux/packages/foss-ids/foss_snort.pp
     %attr(0755, root, root)     /etc/NetworkManager/dispatcher.d/99-snort
     %attr(0644, root, root)     /etc/httpd/conf.d/foss-ids.conf
     %attr(0644, root, root)     /etc/systemd/system/snort@.service
     %attr(0644, root, root)     /etc/systemd/system/snorby.service
     %attr(0644, root, root)     /etc/systemd/system/barnyard2.service

     %config(noreplace)          /etc/snort/white_list.rules
     %config(noreplace)          /etc/snort/black_list.rules
     %config(noreplace)          /etc/snort/foss_snort.conf
     %config(noreplace)          /etc/snort/rules/local.rules
     %config(noreplace)          /etc/snort/rules/fossdemo.rules
%dir %attr(0755, root, root)     /etc/snort/rules/community-rules
     %config(noreplace)          /etc/snort/rules/community-rules/*
%dir %attr(0755, root, root)     /etc/snort/rules/quickdraw
     %config(noreplace)          /etc/snort/rules/quickdraw/*
     %config(noreplace)          /etc/snort/rules/sid-msg.map

     %attr(0755, root, root)     /usr/local/bin/barnyard2
     %attr(0755, root, root)     /usr/local/bin/create-sidmap.pl

     %config(noreplace)          /opt/rh/httpd24/root/etc/httpd/conf.d/snorby.conf

%dir %attr(0750, apache, apache) /opt/rh/httpd24/root/var/www/html/snorby
%dir %attr(0750, apache, apache) /opt/rh/httpd24/root/var/www/html/snorby/config
     %attr(0640, apache, apache) /opt/rh/httpd24/root/var/www/html/snorby/config/snorby_config.yml
     %attr(0750, apache, apache) /opt/rh/httpd24/root/var/www/html/snorby/*
     %attr(0750, apache, apache) /opt/rh/httpd24/root/var/www/html/snorby/.*


     %attr(0750, root, root)     /root/barn_snor.sh
     %attr(0750, root, root)     /root/maria_secure_installation.sh
     %attr(0640, root, root)     /root/snort.db
     %attr(0640, root, root)     /root/barnyard2.conf.template
     %attr(0640, root, root)     /root/database.yml
