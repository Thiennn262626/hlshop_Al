#!/bin/bash
uvicorn main:app --reload --port 8080

# pip freeze > requirements.txt