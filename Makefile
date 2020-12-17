.SILENT: ;

install: 
	python setup.py install

develop:
	python setup.py develop

clean:
	rm -rf build *.egg-info *.log report.tar.gz

uninstall:
	rm -rf venv build dist *.egg-info
	find . -type d -name '__pycache__' -exec rm -r {} +

run:
	python -m dirac

test-all:
	python -m unittest discover

# Requires additional installs
generate-uml:
	pyreverse -o png -p kMap ./kmap
	
help:
	echo 'Usage:'   
	echo '    make <command> [options]'
	echo 'Commands:'
	echo '    install      Installs the application.'
	echo '    develop      Installs the application in development mode.'
	echo '    clean        Removes dist and build directories.'
	echo '    uninstall    Removes the virtual environment, dist, build and all __pycache__ directories.'
	echo '    run          Starts the application.'
	echo '    test-all     Runs all available tests.'