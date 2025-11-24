class BitVector:
    """
    Python int를 내부 저장소로 사용하는 일반적인 비트 벡터 클래스.
    - 비트 순회 가능
    - __getitem__ (인덱싱 가능)
    - __len__ (비트 길이)
    - set_bit(), get_bit() 지원
    """

    def __init__(self, value: int = 0, length: int = None):
        if value < 0:
            raise ValueError("BitVector는 음수 정수를 허용하지 않습니다.")

        self._value = value
        if length is None:
            self._length = value.bit_length()
        else:
            self._length = length
            # 길이가 주어졌으면 bit_length보다 커야 함(패딩 의미)
            if value.bit_length() > length:
                raise ValueError("value의 bit_length가 length보다 큼.")

    def __len__(self):
        """비트 길이 반환"""
        return self._length

    def __getitem__(self, index: int) -> int:
        """index번째 비트 반환 (0 = 최하위 비트)"""
        if not 0 <= index < self._length:
            raise IndexError("BitVector 인덱스 범위 초과")
        return (self._value >> index) & 1

    def __setitem__(self, index: int, bit: int):
        """index번째 비트 설정 (0 또는 1)"""
        if not 0 <= index < self._length:
            raise IndexError("BitVector 인덱스 범위 초과")
        if bit not in (0, 1):
            raise ValueError("bit는 0 또는 1이어야 함")

        if bit == 1:
            self._value |= (1 << index)
        else:
            self._value &= ~(1 << index)

    def __iter__(self):
        """LSB → MSB 순으로 반복(iterable)"""
        for i in range(self._length):
            yield (self._value >> i) & 1

    def __repr__(self):
        """이진 문자열로 출력"""
        return "".join(str(self[i]) for i in reversed(range(self._length)))

    # 유용한 기능들 추가
    def to_int(self) -> int:
        return self._value

    def resize(self, new_length: int):
        """비트 벡터 길이를 늘리거나 줄임"""
        if new_length < self._length:
            # 상위 비트 제거됨
            mask = (1 << new_length) - 1
            self._value &= mask
        self._length = new_length


if __name__ == "__main__":
    bv = BitVector(0b101101, length=6)
    print(bv)           # 101101

    print(len(bv))      # 6

    print(bv[0])        # LSB → 1
    print(bv[5])        # MSB → 1

    bv[2] = 0
    print(bv)           # 101001

    for b in bv:
        print(b, end=" ")  # 1 0 0 1 0 1
