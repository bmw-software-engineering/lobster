package:
	rm -rf lobster dist meta_dist
	cp -Rv $(LOBSTER_ROOT)/lobster lobster
	@python3 -m build --wheel
	mv dist meta_dist
