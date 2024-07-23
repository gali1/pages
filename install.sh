#!/bin/sh
SHELL=/bin/sh
# PATH=/usr/local/bin:/usr/bin:/bin
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin

pip install -r requirements.txt
curl https://ollama.ai/install.sh | sh
ollama server
ollama pull llama2 & ollama pull orca-mini & ollama pull tinyllama
python main.py
