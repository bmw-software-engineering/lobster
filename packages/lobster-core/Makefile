package:
	rm -rf lobster
	mkdir -p lobster/tools
	cp $(LOBSTER_ROOT)/lobster/*.py lobster
	cp -Rv $(LOBSTER_ROOT)/lobster/config lobster
	cp -Rv $(LOBSTER_ROOT)/lobster/html lobster
	cp -Rv $(LOBSTER_ROOT)/lobster/tools/core lobster/tools
	@python3 setup.py sdist bdist_wheel
