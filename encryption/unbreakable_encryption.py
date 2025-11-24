from secrets import token_bytes
from typing import Tuple

def random_key(length: int) -> int:
    # length만큼 임의의 바이트를 생성
    tb: bytes = token_bytes(length)
    # 바이트를 비트 문자열로 변환한 후 반환
    return int.from_bytes(tb, "big")

def encrypt(original: str) -> Tuple[int, int]:
    original_bytes: bytes = original.encode()
    dummy: int = random_key(len(original_bytes))
    original_key: int = int.from_bytes(original_bytes, "big")
    encrypted: int = original_key ^ dummy
    return dummy, encrypted

def decrypt(key1: int, key2: int) -> str:
    decrypted: int = key1 ^ key2
    temp: bytes = decrypted.to_bytes((decrypted.bit_length() + 7)//8, "big")
    return temp.decode()

if __name__ == "__main__":
    key1, key2 = encrypt("One Time Pad!")
    result: str = decrypt(key1, key2)
    print(result)