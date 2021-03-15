# No debuginfo:
%define debug_package %{nil}
%define name      foss-docs
%define summary   PDF and HTMl documentation for the FOSS distribution
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
Requires:  firefox
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
PDF and HTMl documentation for the FOSS distribution

%prep

%build

%install
pushd %{_srcdir}
cp -r * %{buildroot}

%post
touch /opt/.foss-docs

%clean
rm -rf %{buildroot}

%postun
rm -f /opt/.foss-docs

%files
%defattr(-,root,root)
%dir %attr(0755, root, root)                                /etc/skel/Desktop
     %attr(0644, root, root)                                /etc/skel/Desktop/Dokumentation.pdf
     %attr(0644, root, root)                                /etc/pki/rpm-gpg/RPM-GPG-KEY-skydd_ics
     %attr(0644, root, root)                                /etc/yum.repos.d/skydd-ics.repo
%dir %attr(0755, root, root)                                /var/www/html/foss/doc
     %attr(0644, root, root)                                /var/www/html/foss/doc/index.html
%dir %attr(0755, root, root)                                /var/www/html/foss/doc/css
     %attr(0644, root, root)                                /var/www/html/foss/doc/css/*
%dir %attr(0755, root, root)                                /var/www/html/foss/doc/images
     %attr(0644, root, root)                                /var/www/html/foss/doc/images/*

