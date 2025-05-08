
build: zip exe

install: build
	cp hot ~/.local/bin/

zip: clean
	cd hotpy && zip -r ../hot.zip . -x "*/__pycache__/*"

exe:
	echo '#!/usr/bin/env python3' | cat - hot.zip > hot && chmod +x hot
	rm hot.zip

deploy: build
	cp hot ~/.local/bin/

clean:
	rm -f hot.zip hot
	rm -rf hotpy/**/*.pyc
	rm -rf hotpy/**/__pycache__
