run:
	/opt/homebrew/opt/python@3.11/libexec/bin/python src/run.py
check:
	pyright --pythonpath "/opt/homebrew/opt/python@3.11/libexec/bin/python" src
format:
    ruff format robot
