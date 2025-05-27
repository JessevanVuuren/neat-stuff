from typing import TYPE_CHECKING
import sys
import os

# link to neat folder ../neat/*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../libs')))

# TYPE_CHECKING == True for Pylance, False for python interpreter
if TYPE_CHECKING:
    from python.libs.neaty import *
else:
    from neaty import *  # type: ignore