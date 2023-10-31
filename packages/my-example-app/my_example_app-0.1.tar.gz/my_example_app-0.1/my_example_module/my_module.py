# my_module.py

def add(a, b):
    """두 숫자를 더하는 함수"""
    return a + b

def subtract(a, b):
    """두 숫자를 빼는 함수"""
    return a - b

def multiply(a, b):
    """두 숫자를 곱하는 함수"""
    return a * b

def divide(a, b):
    """두 숫자를 나누는 함수"""
    if b == 0:
        raise ValueError("division by zero is not allowed")
    return a / b

if __name__ == "__main__":
    # 모듈을 직접 실행할 때 수행할 코드
    result = add(5, 3)
    print(f"5 + 3 = {result}")
    result = subtract(10, 4)
    print(f"10 - 4 = {result}")

