def get_bytes(seconds: int, byte_rate: int) -> int:
    return byte_rate * seconds

def get_seconds(bytes: int, byte_rate: int) -> float:
    return float(bytes) / byte_rate
