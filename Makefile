build:
	: run make install
install:
	mkdir -p $(DESTDIR)/usr/share/pardus/pardus-lightdm-greeter/module
	cp -prfv module/* $(DESTDIR)/usr/share/pardus/pardus-lightdm-greeter/module/
	cp -prfv ebaonline.py $(DESTDIR)/usr/share/pardus/pardus-lightdm-greeter/
