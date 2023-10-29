from functools import lru_cache

from Crypto.Hash import keccak


@lru_cache(maxsize=4096, typed=True)
def keccak256(data: bytes|str) -> str:
    """Return the Keccak-256 hash of 'data'."""
    if isinstance(data, str):
        data = data.encode()

    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest().hex()
