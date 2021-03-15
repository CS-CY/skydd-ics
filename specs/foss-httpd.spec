# No debuginfo:
%define debug_package %{nil}
%define name      foss-httpd
%define summary   Place holder for foss-httpd
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
Requires:  httpd, openssl, perl-CGI, perl-JSON, perl-URI, perl-PerlIO-gzip, foss-common, perl-IPC-Run
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Used to generate a certificate for now, could also be done with ansible

%prep

%build
# Build a selinux policy to allow httpd to read status of services
cd %{_srcdir}
make -f /usr/share/selinux/devel/Makefile

%install
pushd %{_srcdir}
mkdir -p  %{buildroot}/usr/share/selinux/packages/foss-httpd
cp -r etc var %{buildroot}
cp  %{_srcdir}/*.pp  %{buildroot}/usr/share/selinux/packages/foss-httpd


%pre
if [ $1 -eq 1 ];then
    # install
    openssl req -new -newkey rsa:4096 -days 3650 -nodes -x509 -subj "/CN=pregenerated certificate" -keyout /etc/pki/tls/private/dummy.key -out /etc/pki/tls/certs/dummy.cert
    cat /etc/pki/tls/private/dummy.key > /etc/pki/tls/private/dummy.pem
    cat /etc/pki/tls/certs/dummy.cert >> /etc/pki/tls/private/dummy.pem
    chmod 700 /etc/pki/tls/private
    chmod 600 /etc/pki/tls/private/*
fi

%post
touch /opt/.foss-httpd
# run ansible with provided inventory which could have beeen changed by the user
/usr/bin/ansible-playbook -i /opt/ansible/inventory.yml /opt/ansible/playbooks/httpd.yml > /root/ansible-run-$$

%clean
rm -rf %{buildroot}

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-httpd
fi

%files
%defattr(-,root,root)
     %attr(0644, root, root) /etc/httpd/conf.d/foss-default.conf
%dir %attr(0755, root, root) /usr/share/selinux/packages/foss-httpd
     %attr(0644, root, root) /usr/share/selinux/packages/foss-httpd/foss_httpd.pp
%dir %attr(0755, root, root) /var/www/html/js
     %attr(0644, root, root) /var/www/html/js/*.js
%dir %attr(0755, root, root) /var/www/html/status/js
     %attr(0644, root, root) /var/www/html/status/js/*.js
%dir %attr(0755, root, root) /var/www/html/assets
     %attr(0644, root, root) /var/www/html/assets/*
%dir %attr(0755, root, root) /var/www/html/css
     %attr(0640, apache, apache) /var/www/html/css/*.css
%dir %attr(0755, root, root) /var/www/html/status
     %attr(0640, apache, apache) /var/www/html/status/*.html
%dir %attr(0755, root, root) /var/www/html/status/cgi
     %attr(0550, apache, apache) /var/www/html/status/cgi/*
