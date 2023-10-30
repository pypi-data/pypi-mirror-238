# Kaftar SDK

## Usage

Package installation

``` bash
pip install kaftar
```

Here is how to set a multiple notification task on Rabbitmq with client package:

``` python
from kaftar import Notification


app = Notification('app_name')
recipient = [
    {'receiver': 'user@exampe.com', 'uuid': 'b60bf22b-6df8-439b-ba6f-73f203e692d1'},
    {'receiver': '+9893002220022', 'uuid': 'b60bf22b-6df8-439b-ba6f-73f203e692d1'}
]
app.send_notification(
    {
        'subject': 'subject 1',
        'content': 'sample 2'
    },
    recipient,
    # send on timestamp
    "1696421378")

```
