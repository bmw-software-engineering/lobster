ASSETS=$(wildcard assets/*.svg)

package: lobster/html/assets.py
	@python3 setup.py sdist bdist_wheel

lobster/html/assets.py: $(ASSETS) ../util/mkassets.py
	../util/mkassets.py lobster/html/assets.py $(ASSETS)
