PWD = $(shell pwd)
BUILDDIR = $(PWD)/foss-build
BUILDNUMBER = $(shell date +%s)
VERSION = $(shell date +%Y%m%d)

all: docs common httpd simplelog dump icinga-repo monitor ids ids-repo

docs:
	@cd ${PWD}/docs && make
	@cd ${PWD}
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-docs
	@mkdir -p $(BUILDDIR)/foss-docs/var/www/html/foss/doc
	@mkdir -p $(BUILDDIR)/foss-docs/etc/skel/Desktop
	@cp -rp	docs/bok.html $(BUILDDIR)/foss-docs/var/www/html/foss/doc/index.html
	@cp -rp	docs/css $(BUILDDIR)/foss-docs/var/www/html/foss/doc/
	@cp -rp	docs/images $(BUILDDIR)/foss-docs/var/www/html/foss/doc
	@cp -rp docs/bok.pdf $(BUILDDIR)/foss-docs/etc/skel/Desktop/Dokumentation.pdf
	@cp -rp files/repo/* $(BUILDDIR)/foss-docs
	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-docs" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-docs.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

common:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-common
	@mkdir -p $(BUILDDIR)/foss-common/boot
	@mkdir -p $(BUILDDIR)/foss-common/opt/
	@cp image/isolinux/splash.png $(BUILDDIR)/foss-common/boot/
	@cp -r files/ansible $(BUILDDIR)/foss-common/opt/
	@cp files/httpd/foss_httpd.* $(BUILDDIR)/foss-common/
	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-common" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-common.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

httpd:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-httpd
	@mkdir -p $(BUILDDIR)/foss-httpd/etc/httpd/conf.d/
	@mkdir -p $(BUILDDIR)/foss-httpd/var/www/html/js
	@mkdir -p $(BUILDDIR)/foss-httpd/var/www/html/css
	@mkdir -p $(BUILDDIR)/foss-httpd/var/www/html/assets
	@mkdir -p $(BUILDDIR)/foss-httpd/var/www/html/status/cgi
	@mkdir -p $(BUILDDIR)/foss-httpd/var/www/html/status/js
	@cp -rp files/httpd/var $(BUILDDIR)/foss-httpd
	@cp -rp files/httpd/etc $(BUILDDIR)/foss-httpd
	@cp files/httpd/foss_httpd.fc $(BUILDDIR)/foss-httpd/
	@cp files/httpd/foss_httpd.te $(BUILDDIR)/foss-httpd/
	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-httpd" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-httpd.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

simplelog:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-simplelog
	@mkdir -p $(BUILDDIR)/foss-simplelog/usr/share/selinux/packages/foss-simple-log
	@mkdir -p $(BUILDDIR)/foss-simplelog/var/log
	@mkdir -p $(BUILDDIR)/foss-simplelog/var/www/html/log/
	@touch $(BUILDDIR)/foss-simplelog/var/www/html/log/searching.json
	@touch $(BUILDDIR)/foss-simplelog/var/log/incoming
	@cp -rp files/simple_log_server/etc $(BUILDDIR)/foss-simplelog
	@cp -rp	files/simple_log_server/var $(BUILDDIR)/foss-simplelog
	@cp -rp files/simple_log_server/usr $(BUILDDIR)/foss-simplelog
	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-simplelog" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-simple-log-server.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

dump:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-dump
	@mkdir -p $(BUILDDIR)/foss-dump/opt
	@mkdir -p $(BUILDDIR)/foss-dump/home/tcpdump
	@mkdir -p $(BUILDDIR)/foss-dump/etc/xdg/autostart
	@mkdir -p $(BUILDDIR)/foss-dump/usr/share/selinux/packages/foss-traffic-capture
	@mkdir -p $(BUILDDIR)/foss-dump/var/www/html/dump
	@touch $(BUILDDIR)/foss-dump/var/www/html/dump/searching.json
	@mkdir -p $(BUILDDIR)/foss-dump/var/www/html/dump/unpacked
	@cp -rp files/dump_server/opt $(BUILDDIR)/foss-dump
	@cp -rp files/dump_server/var $(BUILDDIR)/foss-dump
	@cp -rp files/dump_server/etc $(BUILDDIR)/foss-dump
	@cp files/dump_server/*.te $(BUILDDIR)/foss-dump

	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-dump" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-traffic-capture-server.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

ids-repo:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-ids-repo
	@cp -r files/ids_repo/etc $(BUILDDIR)/foss-ids-repo

	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-ids-repo" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-ids-repo.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

ids:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-ids
	@mkdir -p $(BUILDDIR)/foss-ids/root
	@mkdir -p $(BUILDDIR)/foss-ids/usr/local/bin
	@mkdir -p $(BUILDDIR)/foss-ids/etc/httpd/conf.d/
	@mkdir -p $(BUILDDIR)/foss-ids/etc/snort/rules
	@mkdir -p $(BUILDDIR)/foss-ids/etc/sysctl.d
	@mkdir -p $(BUILDDIR)/foss-ids/etc/yum.repos.d/
	@mkdir -p $(BUILDDIR)/foss-ids/etc/skel/Desktop
	@mkdir -p $(BUILDDIR)/foss-ids/etc/xdg/autostart
	@mkdir -p $(BUILDDIR)/foss-ids/usr/share/selinux/packages/foss-ids
	@mkdir -p $(BUILDDIR)/foss-ids/etc/systemd/system/
	@mkdir -p $(BUILDDIR)/foss-ids/etc/NetworkManager/dispatcher.d/
	@mkdir -p $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/etc/httpd/conf.d/
	@mkdir -p $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/etc/httpd/conf
	@mkdir -p $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/snorby/public
	@tar xzf files/ids/community.tar.gz -C $(BUILDDIR)/foss-ids/etc/snort/rules/
	@unzip -qq -d $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/ files/ids/paket/snorby-master-git-20151111.zip
	@cp -rf $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/snorby-master/* $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/snorby
	@rm -rf $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/snorby-master
	@tar xzpf files/ids/vendor-bundle.tgz -C $(BUILDDIR)/foss-ids/opt/rh/httpd24/root/var/www/html/snorby/
	@cp -rf files/ids/etc $(BUILDDIR)/foss-ids
	@cp -rf files/ids/root $(BUILDDIR)/foss-ids
	@cp -rf files/ids/usr $(BUILDDIR)/foss-ids
	@cp -rf files/ids/opt $(BUILDDIR)/foss-ids
	@cp -f files/ids/*.te $(BUILDDIR)/foss-ids
	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-ids" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
		specs/foss-ids.spec
	@find $(PWD)/rpmbuild/RPMS/ -name \*.rpm -exec mv "{}" $(PWD)/rpms \;

icinga-repo:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-icinga-repo
	@cp -rf files/icinga_repo/etc $(BUILDDIR)/foss-icinga-repo

	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-icinga-repo" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-icinga-repo.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

monitor:
	@mkdir -p $(PWD)/rpmbuild
	@mkdir -p $(PWD)/rpms
	@mkdir -p $(BUILDDIR)/foss-monitor
	@cp -rf files/monitor_server/root $(BUILDDIR)/foss-monitor
	@cp -rf files/monitor_server/etc $(BUILDDIR)/foss-monitor
	@cp -rf files/monitor_server/usr $(BUILDDIR)/foss-monitor

	@cp files/monitor_server/*.te $(BUILDDIR)/foss-monitor
	@cp files/monitor_server/*.fc $(BUILDDIR)/foss-monitor

	@rpmbuild --quiet -bb \
		--define "_topdir $(PWD)/rpmbuild" \
		--define "_srcdir $(BUILDDIR)/foss-monitor" \
		--define "_version $(VERSION)" \
		--define "_buildtag $(BUILDNUMBER)" \
	    specs/foss-monitor-server.spec
	@mv $(PWD)/rpmbuild/RPMS/noarch/foss-*.noarch.rpm rpms

clean:
	rm -rf $(BUILDDIR)
	rm -rf $(PWD)/rpmbuild
	rm -rf $(PWD)/rpms

.PHONY: docs common httpd simplelog dump ids foss-icinga-repo monitor
