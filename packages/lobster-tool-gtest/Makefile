package:
	rm -rf lobster
	mkdir -p lobster/tools
	cp $(LOBSTER_ROOT)/lobster/__init__.py lobster
	cp -Rv $(LOBSTER_ROOT)/lobster/common lobster
	cp -Rv $(LOBSTER_ROOT)/lobster/tools/gtest lobster/tools
	@python3 -m build --wheel
