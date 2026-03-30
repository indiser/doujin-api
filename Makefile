VERSION = 2.0.0
CODENAME = Garbage Can

.PHONY: version run dev install clean

version:
	@echo "Doujin API v$(VERSION) \"$(CODENAME)\""

run:
	uvicorn main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

install:
	pip install -r requirements.txt

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
