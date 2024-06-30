.PHONY: install run clean

install:
	pip install -r requirements.txt
	
setup:
	mkdir -p cloned_repo vector_database
run:
	python main.py

clean:
	rm -rf cloned_repo vector_database
