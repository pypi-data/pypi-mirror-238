# Example
```python
from mars_text_embedding_sdk_python import EmbeddingSDK, KeyValue

objects = [
    [
        KeyValue(key="hello", value="world"),
        KeyValue(key="hello", value="world"),
        KeyValue(key="you", value="are"),
    ],
    [
        KeyValue(key="you", value="are"),
        KeyValue(key="cool", value="beans"),
        KeyValue(key="cool", value="beans"),
    ]
]

sdk = EmbeddingSDK("http://localhost:4001/graphql")
emb_comp = sdk(objects, dims=300).data
arrs = emb_comp.to_arrays(lambda x: x.mean(axis=0)) # aggregate embeddings to their mean
```