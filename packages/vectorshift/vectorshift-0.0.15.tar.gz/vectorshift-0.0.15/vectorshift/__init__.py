# __init__.py
import os

import vectorshift.deploy
import vectorshift.node
import vectorshift.pipeline
import vectorshift.vectorstore

public_key = os.environ.get('VECTORSHIFT_PUBLIC_KEY')
private_key = os.environ.get('VECTORSHIFT_PRIVATE_KEY')
