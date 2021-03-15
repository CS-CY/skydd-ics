# No debuginfo:
%define debug_package %{nil}
%define name      foss-monitor-server
%define summary   Server for monitoring, collecting and sending alarms
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
BuildArch: noarch
Requires:  foss-httpd, foss-common, foss-icinga-repo, icinga2, icingaweb2, openssl, postgresql-server, php-common, php-pgsql, httpd, nagios-plugins-all, icinga2-ido-pgsql
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Server using Icinga for monitoring, capable of sending SMS and emails on alarms

%prep

%build
# Build a selinux policy to allow httpd use icinga
cd %{_srcdir}
make -f /usr/share/selinux/devel/Makefile

%install
pushd %{_srcdir}
mkdir -p  %{buildroot}/usr/share/selinux/packages/foss-monitor
cp  %{_srcdir}/*.pp  %{buildroot}/usr/share/selinux/packages/foss-monitor/
cp -r root etc usr %{buildroot}

%pre

%post
if [ $1 -eq 1 ]; then
    #install
    /bin/systemctl enable first-boot.service
else
    # run ansible with provided inventory which could have beeen changed by the user
    /usr/bin/ansible-playbook -i /opt/ansible/inventory.yml /opt/ansible/playbooks/monitor.yml > /root/ansible-run-$$
fi
touch /opt/.foss-monitor
systemctl restart icinga2

%clean
rm -rf %{buildroot}

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-monitor
fi


%files
%defattr(-,root,root)
     %attr(0644, root, root)              /etc/skel/Desktop/L*Icinga.desktop
     %attr(0644, root, root)              /etc/skel/Desktop/firefox_monitor.desktop
     %attr(0644, root, root)              /etc/xdg/autostart/firefox_monitor_autostart.desktop
%dir %attr(0755, root, root)              /usr/share/selinux/packages/foss-monitor
     %attr(0644, root, root)              /usr/share/selinux/packages/foss-monitor/icinga.pp
     %attr(0644, root, root)              /etc/systemd/system/first-boot.service
     %attr(0644, root, root)              /etc/sudoers.d/foss_notty
     %attr(0755, root, root)              /root/init_pg.sh
     %attr(0755, root, root)              /etc/icinga2/scripts/beepsend.pl
     %attr(0755, root, root)              /etc/icinga2/scripts/sms-notification.sh
     %attr(0640, root, root)              /etc/icinga2/conf.d/foss-templates.conf
     %attr(0640, root, root)              /etc/icinga2/conf.d/foss-commands.conf
     %attr(0640, root, root)              /etc/icinga2/conf.d/foss-notifications.conf


