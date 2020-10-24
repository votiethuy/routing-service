#!/bin/bash
uvicorn -w 4 -b 0.0.0.0:800 athena:app