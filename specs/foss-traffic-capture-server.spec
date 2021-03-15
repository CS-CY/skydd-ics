# No debuginfo:
%define debug_package %{nil}
%define name      foss-traffic-capture-server
%define summary   Server for collecting network traffic
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
Requires:  foss-httpd, foss-common, tcpdump, wireshark, ngrep, perl-URI-Encode, perl-IO-Zlib, perl-Net-DNS, python-inotify, perl-IPC-Run
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Server capturing network traffic. By default it will listen on all interfaces that go active and save the traffic with
tcpdump to /home/tcpdump, rotating and cleaning up automatically when disk gets filled.

%prep

%build
# Build a selinux policy to allow tcpdump to dump to /home/tcpdump.
# Build a selinux policy to allow httpd to read from /home/tcpdump.
cd %{_srcdir}
make -f /usr/share/selinux/devel/Makefile

%install
pushd %{_srcdir}
mkdir -p  %{buildroot}/usr/share/selinux/packages/foss-traffic-capture
cp  %{_srcdir}/*.pp  %{buildroot}/usr/share/selinux/packages/foss-traffic-capture
cp -r opt var usr etc home %{buildroot}

%pre

%post
touch /opt/.foss-traffic
if [ $1 -ne 1 ];then
    # run ansible with provided inventory which could have beeen changed by the user
    /usr/bin/ansible-playbook -i /opt/ansible/inventory.yml /opt/ansible/playbooks/traffic.yml > /root/ansible-run-$$
fi
systemctl restart network

%clean
rm -rf %{buildroot}

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-traffic
fi

%files
%defattr(-,root,root)
%dir %attr(0755, root, root)       /var/www/html/dump
     %attr(0664, apache, apache)   /var/www/html/dump/searching.json
     %attr(0664, apache, apache)   /var/www/html/dump/file-sharp.svg
     %attr(0644, root, root)       /var/www/html/dump/index.html
     %attr(0644, root, root)       /var/www/html/dump/log.html
%dir %attr(0755, root, root)       /var/www/html/dump/css
     %attr(0640, apache, apache)   /var/www/html/dump/css/*
%dir %attr(0755, root, root)       /var/www/html/dump/cgi
     %attr(0550, apache, apache)   /var/www/html/dump/cgi/*
%dir %attr(0755, root, root)       /var/www/html/dump/js
     %attr(0644, root, root)       /var/www/html/dump/js/*
%dir %attr(0755, apache, apache)   /var/www/html/dump/unpacked
%dir %attr(0755, tcpdump, tcpdump) /home/tcpdump
     %attr(0644, root, root)       /etc/sysctl.d/88-inspelningsserver.conf
     %attr(0644, root, root)       "/etc/skel/Desktop/Länk till trafikvy.desktop"
     %attr(0644, root, root)       /etc/skel/Desktop/firefox.desktop
     %attr(0644, root, root)       /etc/xdg/autostart/firefox_autostart.desktop
%dir %attr(0755, root, root)       /usr/share/selinux/packages/foss-traffic-capture
     %attr(0644, root, root)       /usr/share/selinux/packages/foss-traffic-capture/dumper_tcpdump.pp
     %attr(0644, root, root)       /usr/share/selinux/packages/foss-traffic-capture/dumper_httpd.pp
     %attr(0755, root, root)       /etc/NetworkManager/dispatcher.d/99-tcpdump
     %attr(0644, root, root)       /etc/systemd/system/tcpdump@.service
     %attr(0644, root, root)       /etc/systemd/system/reaper.service
%dir %attr(0755, root, root)       /opt
     %attr(0755, root, root)       /opt/reaper.py*
     %attr(0755, root, root)       /opt/chaosreader
