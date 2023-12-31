 
# protonpack-huzzah32 Makefile
# 
# https://docs.circuitpython.org/en/latest/docs/workflows.html#get
#

# URL to access circuitpython hardware
#   Use CPURL environment variable if its set
CPURL := $(if $(CPURL),$(CPURL),http://circuitpython.local)

# the web api login password
CIRCUITPY_WEB_API_PASSWORD=REDACTED_FOR_GITHUB

# Comment out if you don't want to see curl activity
VERBOSE=-v

# URL for Latest CircuitPython 8.x bundle from
#   https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest
CP_BUNDLE_URL=https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20230910/adafruit-circuitpython-bundle-8.x-mpy-20230910.zip

# No config below this line
all: install .gitignore requirements.txt

install: .install-version.py .install-boot.py .install-code.py

requirements.txt:
	. ./venv/bin/activate && pip freeze > requirements.txt

version.py: code.py
	date -r code.py "+__version__ = %'%Y-%m-%d %H:%M:%S%'" > version.py

.install-%.py: %.py
	curl $(VERBOSE) -u :$(CIRCUITPY_WEB_API_PASSWORD) --create-dirs --location --location-trusted \
		--upload-file $< $(CPURL)/fs/$< \
	  	&& touch $(@)

install-lib: downloads downloads/bundle/lib/neopixel.mpy \
		downloads/bundle/lib/adafruit_fancyled/adafruit_fancyled.mpy
	cd downloads/bundle/lib && \
	curl $(VERBOSE) -u :$(CIRCUITPY_WEB_API_PASSWORD) --create-dirs --location --location-trusted \
		--upload-file adafruit_fancyled/adafruit_fancyled.mpy $(CPURL)/fs/lib/adafruit_fancyled/adafruit_fancyled.mpy \
		--upload-file adafruit_fancyled/__init__.py $(CPURL)/fs/lib/adafruit_fancyled/__init__.py \
		--upload-file neopixel.mpy $(CPURL)/fs/lib/neopixel.mpy

get-cp-info:
	test -d downloads || mkdir downloads
	cd downloads && curl $(VERBOSE) --location --location-trusted \
		-O $(CPURL)/cp/devices.json \
		-O $(CPURL)/cp/version.json

.gitignore:
	curl https://www.toptal.com/developers/gitignore/api/python,circuitpython,git,virtualenv,macos,vim,pycharm -o .gitignore
	printf "\n# ignore the downloads directory\ndownloads\n" >> .gitignore
	printf "\n# ignore version.py that updates each install\nversion.py\n" >> .gitignore
	printf "\n# ignore .install-* files that tracks installation\n.install-*\n" >> .gitignore

downloads:
	test -d downloads || mkdir downloads
	cd downloads && curl --location --progress-bar \
		-O https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/download/20221122/adafruit-circuitpython-bundle-8.x-mpy-20221122.zip \
		-O $(CP_BUNDLE_URL) \
		&& unzip adafruit-circuitpython-bundle-8.x-mpy-20221122.zip && \
		ln -s adafruit-circuitpython-bundle-8.x-mpy-20221122 bundle

clean:
	rm -fr __pycache__ version.py downloads .install-*.py
