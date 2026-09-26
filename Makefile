SERVICE := alf
DESTDIR ?= dist_root
SERVICEDIR ?= /srv/$(SERVICE)

.PHONY: build install

build:
	echo nothing to build

install: build
	mkdir -p $(DESTDIR)$(SERVICEDIR)
	yq -y 'del(.services."alf_deps")' docker-compose.yml > $(DESTDIR)$(SERVICEDIR)/docker-compose.yml
	yq -y 'del(.services."alf_deps")' docker-compose.yml > $(DESTDIR)$(SERVICEDIR)/docker-compose.yml

	
	mkdir -p $(DESTDIR)$(SERVICEDIR)/src
	cp -r src/* $(DESTDIR)$(SERVICEDIR)/src/
	cp Dockerfile $(DESTDIR)$(SERVICEDIR)/Dockerfile
	
	mkdir -p $(DESTDIR)/etc/systemd/system/faustctf.target.wants/
	ln -s /etc/systemd/system/docker-compose@.service $(DESTDIR)/etc/systemd/system/faustctf.target.wants/docker-compose@$(SERVICE).service


