from typing import Optional
import secrets
import random
import hashlib




def make_rng(seed: Optional[str] = None, secure: bool = True) -> random.Random:

    if seed is not None:

        h = hashlib.sha256(seed.encode("utf-8")).digest()
        seed_int = int.from_bytes(h[:8], "big")
        rng = random.Random(seed_int)
        return rng


    if secure:

        return secrets.SystemRandom() 


    return random.Random()