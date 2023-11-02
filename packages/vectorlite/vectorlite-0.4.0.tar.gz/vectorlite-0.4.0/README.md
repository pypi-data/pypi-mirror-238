# VectorLiteDB

**VectorLite** is a simple vector database powered by `sentence-transformers` and `hnswlib`, designed for efficient storage and search of textual data.

# 🚀 Quick Install

```pip install vectorlite```

# Usage

## Run as api server

1. ```serve vectorlite```

2. Navigate to http://localhost:4440/docs

## Run integrated in code
### Initialization

```python
from vectorlite import VectorLite
vl = VectorLite()
```

### Adding Data

```python
data = ["Sample text 1", "Sample text 2", "Another example"]
vl.create(data)
```

### Read All Data

```python
all_data = vl.read_all()
```

To limit the number of records returned:

```python
limited_data = vl.read_all(max_items=2)
```

### Read Specific Data by Index

```python
item = vl.read(1)
```

### Update Data by Index

```python
vl.update(1, "Updated sample text 2")
```

### Delete Data by Index

```python
vl.delete(1)
```

### Similarity Search

```python
results = vl.similarity_search("A related sample text", k=3)
```

### Semantic Search

```python
results = vl.semantic_search("A related sample text", k=3)
```
