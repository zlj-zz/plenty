# -*- coding:utf-8 -*-
import os, sys

# Add source environment.
_PLENTY_PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, _PLENTY_PATH)

TEST_PATH = os.path.dirname(__file__)

# /opt/homebrew/opt/python@3.8/bin/python3 -m pytest
