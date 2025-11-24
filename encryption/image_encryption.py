#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from secrets import token_bytes
from typing import Tuple
import argparse
from pathlib import Path


def generate_key(length: int) -> bytes:
    """
    length 바이트 길이의 암호학적으로 안전한 랜덤 키 생성
    (OTP에서는 평문과 길이가 똑같아야 함)
    """
    return token_bytes(length)


def xor_bytes(data: bytes, key: bytes) -> bytes:
    """
    data와 key를 XOR한 결과를 반환.
    len(data) == len(key) 여야 함.
    """
    if len(data) != len(key):
        raise ValueError("data와 key의 길이가 다릅니다.")
    return bytes(d ^ k for d, k in zip(data, key))


def encrypt_image(
    input_path: str | Path,
    encrypted_path: str | Path,
    key_path: str | Path,
) -> None:
    """
    이미지를 OTP 방식으로 암호화.
    - input_path: 원본 이미지 파일 경로
    - encrypted_path: 암호화된 이미지 저장 경로
    - key_path: OTP 키(랜덤 바이트) 저장 경로
    """
    input_path = Path(input_path)
    encrypted_path = Path(encrypted_path)
    key_path = Path(key_path)

    # 1. 원본 이미지 읽기
    original_data = input_path.read_bytes()

    # 2. 같은 길이의 랜덤 키 생성
    key = generate_key(len(original_data))

    # 3. XOR로 암호문 생성
    encrypted_data = xor_bytes(original_data, key)

    # 4. 암호문과 키 저장
    encrypted_path.write_bytes(encrypted_data)
    key_path.write_bytes(key)

    print(f"[+] 암호화 완료")
    print(f"    원본 : {input_path}")
    print(f"    암호문: {encrypted_path}")
    print(f"    키    : {key_path} (절대 유출 금지, 재사용 금지)")


def decrypt_image(
    encrypted_path: str | Path,
    key_path: str | Path,
    output_path: str | Path,
) -> None:
    """
    암호화된 이미지를 OTP 방식으로 복호화.
    - encrypted_path: 암호화된 이미지 경로
    - key_path: 암호화에 사용된 키 파일 경로
    - output_path: 복호화된(원본) 이미지 저장 경로
    """
    encrypted_path = Path(encrypted_path)
    key_path = Path(key_path)
    output_path = Path(output_path)

    encrypted_data = encrypted_path.read_bytes()
    key = key_path.read_bytes()

    if len(encrypted_data) != len(key):
        raise ValueError("암호문과 키 길이가 다릅니다.")

    decrypted_data = xor_bytes(encrypted_data, key)
    output_path.write_bytes(decrypted_data)

    print(f"[+] 복호화 완료")
    print(f"    암호문: {encrypted_path}")
    print(f"    키    : {key_path}")
    print(f"    복호화된 이미지: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="OTP 방식 이미지 암·복호화 도구")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # encrypt 서브커맨드
    enc = subparsers.add_parser("encrypt", help="이미지 암호화")
    enc.add_argument("input", help="원본 이미지 경로 (예: input.png)")
    enc.add_argument("encrypted", help="암호화된 이미지 경로 출력 (예: encrypted.bin)")
    enc.add_argument("key", help="암호화에 사용한 키 저장 경로 (예: key.bin)")

    # decrypt 서브커맨드
    dec = subparsers.add_parser("decrypt", help="이미지 복호화")
    dec.add_argument("encrypted", help="암호화된 이미지 경로 (예: encrypted.bin)")
    dec.add_argument("key", help="키 파일 경로 (예: key.bin)")
    dec.add_argument("output", help="복호화된 이미지 출력 경로 (예: output.png)")

    args = parser.parse_args()

    if args.command == "encrypt":
        encrypt_image(args.input, args.encrypted, args.key)
    elif args.command == "decrypt":
        decrypt_image(args.encrypted, args.key, args.output)


if __name__ == "__main__":
    main()
