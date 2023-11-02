from flask import Flask
from vectorvault import Vault

app = Flask(__name__)
vault = Vault(user='john.rood@decision.com',
              api_key='4e258eea_c7d2_457c_8831_4853e43c4900',
              openai_key='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',
              vault='youtubeexplode',
              verbose=True)
@app.route('/')
def hello():
    return "Hello, World!"
