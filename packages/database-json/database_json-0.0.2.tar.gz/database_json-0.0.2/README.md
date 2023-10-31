# How use it?

Install:
```
pip install json-database
```
import:
```py
from json_database import json_db
```
Create database (file), write:
```py
db = json_db("name")


```
get somebody from database
```py
db.get(self, name: str) -> list
```
delete somebody from database
```py
db.delete(self, name: str) -> None
```
create and redact type in database
```py
db.redact(self, name: str, new_dict: list = []) -> None
```
update information in file.json
```py
db.commit(self) -> None
```
get new self.json from file.json
```py
db.update(self) -> None
```


