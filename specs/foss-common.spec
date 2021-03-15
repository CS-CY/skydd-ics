# No debuginfo:
%define debug_package %{nil}
%define name      foss-common
%define summary   Configures the boot splash to use the FOSS splash etc.
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
Requires:  grub2, grub2-tools, pwgen, ansible, iptables-services, tcpdump, net-tools, foss-docs
Requires(pre): shadow-utils
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Configures the boot splash to use the FOSS splash. It also changes the password for the root user and installs the
ansible settings (it also runs them when it is an upgrade)
%prep

%build

%install
pushd %{_srcdir}
cp -r boot opt %{buildroot}

%post
if [ $1 -eq 1 ];then
    # install
	echo 'GRUB_BACKGROUND="/boot/splash.png"' >> /etc/default/grub
	perl -p -i -e "s/GRUB_TERMINAL_OUTPUT=\"console\"/GRUB_TERMINAL_OUTPUT=\"gfxterm\"/g" /etc/default/grub
    perl -p -i -e "s/insmod gfxterm$/insmod gfxterm;insmod gfxterm_background/g" /etc/grub.d/00_header
    if [ -d /sys/firmware/efi ]; then
        if [ ! -f /boot/efi/EFI/centos/grub.cfg ]; then
            if [ ! -d /boot/efi/EFI/BOOT/x86_64-efi ]; then
                mkdir -p /boot/efi/EFI/BOOT/x86_64-efi
            fi
            cp -f /usr/lib/grub/x86_64-efi/gfxterm_background.mod /boot/efi/EFI/BOOT/x86_64-efi
        fi
	    grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
    elif [ ! -f /boot/grub/i386-pc ]; then
        mkdir -p /boot/grub/i386-pc
        cp -f /usr/lib/grub/i386-pc/gfxterm_background.mod  /boot/rub/i386-pc
	    grub2-mkconfig -o /boot/grub2/grub.cfg
    fi
else
    # run ansible with provided inventory which could have beeen changed by the user
    /usr/bin/ansible-playbook -i /opt/ansible/inventory.yml /opt/ansible/playbooks/foss.yml
fi
touch /opt/.foss-common

%clean
rm -rf %{buildroot}

%postun
if [ $1 -eq 0 ];then
  rm -f /opt/.foss-common
fi

%files
%defattr(-,root,root)
     %attr(0644, root, root) /boot/splash.png
%dir %attr(0755, root, root) /opt/ansible
     %attr(0644, root, root) %config(noreplace) /opt/ansible/inventory.yml
     %attr(0644, root, root) /opt/ansible/inventory_live.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks
     %attr(0644, root, root) /opt/ansible/playbooks/httpd.yml
     %attr(0644, root, root) /opt/ansible/playbooks/monitor.yml
     %attr(0644, root, root) /opt/ansible/playbooks/foss.yml
     %attr(0644, root, root) /opt/ansible/playbooks/ids.yml
     %attr(0644, root, root) /opt/ansible/playbooks/simple_log.yml
     %attr(0644, root, root) /opt/ansible/playbooks/traffic.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/common
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/common/defaults
     %attr(0644, root, root) /opt/ansible/playbooks/roles/common/defaults/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/common/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/common/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/common/tasks
     %attr(0644, root, root) /opt/ansible/playbooks/roles/common/tasks/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/common/templates
     %attr(0644, root, root) /opt/ansible/playbooks/roles/common/templates/etc/sysconfig/iptables.j2
     %attr(0644, root, root) /opt/ansible/playbooks/roles/common/templates/root/find_install_errors.sh
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/ids
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/ids/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/ids/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/ids/tasks
     %attr(0644, root, root) /opt/ansible/playbooks/roles/ids/tasks/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/httpd
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/httpd/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/httpd/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/httpd/tasks
     %attr(0644, root, root) /opt/ansible/playbooks/roles/httpd/tasks/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/httpd/templates
     %attr(0644, root, root) /opt/ansible/playbooks/roles/httpd/templates/lighttpd.conf.j2
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/simple_log
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/simple_log/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/simple_log/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/simple_log/tasks
     %attr(0644, root, root) /opt/ansible/playbooks/roles/simple_log/tasks/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/traffic_capture
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/traffic_capture/tasks
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/traffic_capture/files
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/traffic_capture/files/root
     %attr(0644, root, root) /opt/ansible/playbooks/roles/traffic_capture/files/root/test_full_disk.sh
     %attr(0644, root, root) /opt/ansible/playbooks/roles/traffic_capture/tasks/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/traffic_capture/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/traffic_capture/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/monitor
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/monitor/handlers
     %attr(0644, root, root) /opt/ansible/playbooks/roles/monitor/handlers/main.yml
%dir %attr(0755, root, root) /opt/ansible/playbooks/roles/monitor/tasks
     %attr(0644, root, root) /opt/ansible/playbooks/roles/monitor/tasks/main.yml
