.PHONY: all generate clean

all: generate

generate:
	python3 generate-repo.py

clean:
	rm -f Packages Packages.gz Packages.xz Packages.zst Release
