SYSTEM_PYTHONPATH:=$(PYTHONPATH)
export LOBSTER_ROOT=$(PWD)
export PYTHONPATH=$(LOBSTER_ROOT)

ASSETS=$(wildcard assets/*.svg)

lobster/html/assets.py: $(ASSETS) util/mkassets.py
	util/mkassets.py lobster/html/assets.py $(ASSETS)

lint: style
	@PYTHONPATH=$(SYSTEM_PYTHONPATH) \
	python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no \
		--ignore=assets.py \
		lobster

style:
	@python3 -m pycodestyle lobster \
		--exclude=assets.py

.PHONY: packages
packages:
	git clean -xdf
	make lobster/html/assets.py
	make -C packages/lobster-core
	make -C packages/lobster-tool-trlc
	make -C packages/lobster-tool-codebeamer
	make -C packages/lobster-tool-cpp
	make -C packages/lobster-tool-gtest
	make -C packages/lobster-tool-json
	make -C packages/lobster-tool-python
	make -C packages/lobster-metapackage
	make -C packages/lobster-monolithic
    # Print the working directory and list files before installation
	@echo "Working directory before first install: " && pwd
	@echo "Contents of current directory: " && ls
	PYTHONPATH= \
		pip3 install --prefix test_install \
		packages/*/dist/*.whl
    # Print the working directory and list files after first installation
	@echo "Working directory after first install: " && pwd
	@echo "Contents of test_install/lib/python*: " && ls test_install/lib/python*/site-packages/lobster || echo "Lobster not found in test_install"
	PYTHONPATH= \
		pip3 install --prefix test_install_monolithic \
		packages/lobster-monolithic/meta_dist/*.whl
    # Print the working directory and list files after 2nd installation
	@echo "Working directory after second install: " && pwd
	@echo "Contents of test_install_monolithic/lib/python*: " && ls test_install_monolithic/lib/python*/site-packages/lobster || echo "Lobster not found in test_install_monolithic"
	diff -Naur test_install/lib/python*/site-packages/lobster test_install_monolithic/lib/python*/site-packages/lobster -x "*.pyc"
	diff -Naur test_install/bin test_install_monolithic/bin

integration-tests: packages
	(cd integration-tests/projects/basic; make)
	(cd integration-tests/projects/filter; make)

system-tests:
	mkdir -p docs
	make -B -C test-system/lobster-json
	make -B -C test-system/lobster-python

unit-tests:
	coverage run -p \
			--branch --rcfile=coverage.cfg \
			--data-file .coverage \
			-m unittest discover -s test-unit -v

test: integration-tests system-tests unit-tests

upload-main: packages
	python3 -m twine upload --repository pypi packages/*/dist/*
	python3 -m twine upload --repository pypi packages/*/meta_dist/*

remove-dev:
	python3 -m util.release

github-release:
	git push
	python3 -m util.github_release

bump:
	python3 -m util.bump_version_post_release

full-release:
	make remove-dev
	git push
	make upload-main
	make github-release
	make bump
	git push

coverage:
	coverage combine -q
	coverage html --rcfile=coverage.cfg
	coverage report --rcfile=coverage.cfg --fail-under=57

test-ci: system-tests unit-tests coverage
	util/check_local_modifications.sh

docs:
	rm -rf docs
	mkdir docs
