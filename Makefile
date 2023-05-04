export PYTHONPATH=lobster-core

lint: style
	@python3 -m pylint --rcfile=pylint3.cfg \
		--reports=no lobster-* \
		--ignore=setup.py \
		--ignore-paths=lobster-.*/build

style:
	@python3 -m pycodestyle lobster-* \
		--exclude=assets.py,setup.py,build,dist \

packages:
	git clean -xdf

	make -C lobster-core
	make -C lobster-tool-cpp
	make -C lobster-tool-codebeamer
	make -C lobster-tool-gtest
	make -C lobster-tool-python
	make -C lobster-metapackage
	PYTHONPATH= pip3 install --prefix test_install lobster-*/dist/*.whl trlc

test: packages
	make -C integration-tests/projects/basic

upload_main: packages
	python3 -m twine upload --repository pypi lobster-*/dist/*

remove_dev:
	python3 -m util.release

github_release:
	git push
	python3 -m util.github_release

bump:
	python3 -m util.bump_version_post_release
