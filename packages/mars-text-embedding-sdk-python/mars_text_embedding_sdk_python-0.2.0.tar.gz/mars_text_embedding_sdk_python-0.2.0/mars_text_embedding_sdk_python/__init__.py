import numpy as np

from requests import post
from dataclasses import dataclass
from typing import Optional, List, Dict
from pickle import loads
from gzip import decompress
from base64 import b64decode
from itertools import chain, starmap

@dataclass
class KeyValue:
        
    key:   str
    value: str

    def __hash__(self) -> int:
        return hash(self.key + str(self.value))

    def from_dict(d: dict) -> 'KeyValue':
        return KeyValue(
            key=d["key"],
            value=d["value"],
        )
    
    def from_tuple(t: tuple) -> 'KeyValue':
        return KeyValue(
            key=t[0],
            value=t[1],
        )
    
    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value": self.value,
        }
    
@dataclass
class Embedding:

    vector: np.ndarray
    key_value: KeyValue

@dataclass
class EmbeddingCollection:

    embeddings: List[Embedding]

    def to_array(self) -> np.ndarray:
        return np.array(
            list(
                map(
                    lambda x: x.vector,
                    self.embeddings
                )
            )
        )

@dataclass
class EmbeddingCollectionComposer:

    groups:     List[List[int]]
    embeddings: Dict[int, Embedding]

    def __getitem__(self, key: int) -> List[Embedding]:
        return EmbeddingCollection(
            embeddings=list(
                map(
                    lambda x: self.embeddings[x],
                    self.groups[key]
                )
            )
        )
    
    def to_arrays(self, agg = lambda x: x) -> List[np.ndarray]:
        return list(
            map(
                lambda i: agg(self[i].to_array()),
                range(
                    len(self.groups)
                )
            )
        )

@dataclass
class Result:

    data:   Optional[EmbeddingCollectionComposer]   = None
    error:  Optional[str]                   = None

@dataclass
class EmbeddingSDK:
    
    url: str

    @staticmethod
    def _prepare_objects(objects: List[KeyValue]) -> dict:

        """
            Returns a dictionary of unique objects.
        """
        return dict(
            map(
                lambda x: (hash(x), x),
                objects
            )
        )

    def __call__(self, objects: List[List[KeyValue]], dims: int = 300) -> Result:

        """
            Converts a list of key-value objects, into a list of embedding objects.

            :param objects: A list of lists of key-value objects to be converted into embeddings.
            :param dims: The number of dimensions of the embedding. Check API documentation for supported dimensions.
            :return: EmbeddingCollectionComposer.
        """

        try:
            object_dicts = self._prepare_objects(
                chain(*objects)
            )
            response = post(
                self.url, 
                json={
                    "query": """
                        query VectorQuery($keyValues: [[KeyValueInput!]!]!) {
                            fromKeyValues(keyValues: $keyValues) {
                                asVectors(model: D"""+str(dims)+""") {
                                    vectors {
                                        compressed
                                    }
                                }
                            }
                        }
                    """,
                    "variables": {
                        "keyValues": [
                            list(
                                map(
                                    lambda x: x.to_dict(),
                                    object_dicts.values(),
                                )
                            )
                        ],
                    }
                }
            )

            if response.status_code == 200:
                if "errors" in response.json():
                    return Result(error=response.json()["errors"][0]["message"])
                
                return Result(
                    data=EmbeddingCollectionComposer(
                        groups=list(
                            map(
                                lambda xs: list(
                                    map(
                                        lambda y: hash(y),
                                        set(xs)
                                    )
                                ),
                                objects,
                            )
                        ),
                        embeddings=dict(
                            starmap(
                                lambda key, compressed_vector: (
                                    key,
                                    Embedding(
                                        vector=np.array(
                                            loads(
                                                decompress(
                                                    b64decode(
                                                        compressed_vector["compressed"]
                                                    )
                                                )
                                            )
                                        ),
                                        key_value=object_dicts[key],
                                    ),
                                ),
                                zip(
                                    object_dicts.keys(),
                                    response.json()["data"]["fromKeyValues"][0]['asVectors']['vectors'],
                                )
                            )
                        )
                    )
                )

        except Exception as e:
            return Result(error=str(e))
