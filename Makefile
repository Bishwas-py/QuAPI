start:
	PYTHONPATH=. ./core/server.py --port=8000 --host=0 
freeze: 
	rm requirements.txt
	pip freeze >> requirements.txt