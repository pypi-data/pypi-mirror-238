
# Comet Connector

A Python package to connect and retrieve data from the Comet API.

## Usage

```python

from connectorcomet.connector import Connector

# Crear una instancia de la clase Connector
connector_instance = Connector()

# Lista de tokens
list_token_api = ['your tokens']

# Llamar al método getResults
df_results = connector_instance.getResults(list_token_api)


```

