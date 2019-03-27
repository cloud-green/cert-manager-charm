all: lint charm/builds/cert-manager

.PHONY: lint
lint:
	flake8 --ignore=E121,E123,E126,E226,E24,E704,E265 charm/cert-manager

charm/builds/cert-manager:
	(cd charm/cert-manager; charm build -o ..)

clean:
	$(RM) -r charm/builds

sysdeps: /snap/bin/charm /usr/bin/flake8
/snap/bin/charm:
	sudo snap install charm --classic
/usr/bin/flake8:
	sudo apt-get install -y flake8
