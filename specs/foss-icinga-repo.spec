# No debuginfo:
%define debug_package %{nil}
%define name      foss-icinga-repo
%define summary   Repo for icinga rpms
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
Requires:  foss-common
Requires(pre): shadow-utils, centos-release-scl
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Icinga repo

%prep

%install
pushd %{_srcdir}
cp -r etc %{buildroot}

%post
touch /opt/.foss-monitor-repo

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-monitor-repo
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
     %attr(0644, root, root)              /etc/yum.repos.d/icinga2.repo
     %attr(0644, root, root)              /etc/pki/rpm-gpg/RPM-GPG-KEY-icinga
