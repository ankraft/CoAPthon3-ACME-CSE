#
#	Makefile
#
#	To build the package and upload it to PyPi
#
#	Targets:
#		- build (default)
#		- local-install

#		- publish
#		- clean

SRCDIR = .
DISTDIR = ${SRCDIR}/dist

build:
	cd ${SRCDIR} && python -m build

publish: clean build
	twine upload `ls -t ${DISTDIR}/*.whl | head -1`

local-install:
	cd ${DISTDIR} && python -m pip install --force-reinstall `ls -1 | grep .whl | head -1`

local-uninstall:
	python -m pip uninstall -y `ls -1 ${DISTDIR} | grep .whl | head -1`

clean: 
	rm -r ${SRCDIR}/*.egg-info
	rm -r ${DISTDIR}