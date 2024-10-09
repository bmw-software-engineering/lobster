package:
	rm -rf lobster
	mkdir -p lobster/tools
	cp -Rv $(LOBSTER_ROOT)/lobster/tools/cpp lobster/tools
	@ PYTHONPATH=$(LOBSTER_ROOT) python3 setup.py sdist bdist_wheel
