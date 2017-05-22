MODULE_NAME = foreign-keycloak-wrapper

install:
	@pip3 install . --upgrade

uninstall:
	@pip3 uninstall $(MODULE_NAME)

clean:
	@rm -f *.pyc
