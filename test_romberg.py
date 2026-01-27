"""
test_romberg.py - Cython Romberg 积分算法的单元测试
"""

import math
import sys
from RombergIntegration import RombergIntegration


def test_1_constant_function_recursive():
    """测试 1: 常函数积分 (递归方法)
    积分常函数 f(x)=1 在 [0, 1]，期望结果：1
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: 1.0)
    result = integrator.recursive()
    expected = 1.0
    assert abs(result - expected) < 1e-9, f"Test 1 failed: {result} vs {expected}"
    print(f"✓ Test 1 passed: constant function (recursive) = {result}")


def test_2_linear_function_recursive():
    """测试 2: 线性函数积分 (递归方法)
    积分线性函数 f(x)=x 在 [0, 1]，期望结果：0.5
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x)
    result = integrator.recursive()
    expected = 0.5
    assert abs(result - expected) < 1e-9, f"Test 2 failed: {result} vs {expected}"
    print(f"✓ Test 2 passed: linear function (recursive) = {result}")


def test_3_quadratic_function_recursive():
    """测试 3: 二次函数积分 (递归方法)
    积分 f(x)=x^2 在 [0, 1]，期望结果：1/3 ≈ 0.333333
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x * x)
    result = integrator.recursive()
    expected = 1.0 / 3.0
    assert abs(result - expected) < 1e-9, f"Test 3 failed: {result} vs {expected}"
    print(f"✓ Test 3 passed: quadratic function (recursive) = {result}")


def test_4_cubic_function_recursive():
    """测试 4: 三次函数积分 (递归方法)
    积分 f(x)=x^3 在 [0, 1]，期望结果：0.25
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x * x * x)
    result = integrator.recursive()
    expected = 0.25
    assert abs(result - expected) < 1e-9, f"Test 4 failed: {result} vs {expected}"
    print(f"✓ Test 4 passed: cubic function (recursive) = {result}")


def test_5_sine_function_recursive():
    """测试 5: 正弦函数积分 (递归方法)
    积分 f(x)=sin(x) 在 [0, π]，期望结果：2
    """
    integrator = RombergIntegration(0.0, math.pi, 1e-10, lambda x: math.sin(x))
    result = integrator.recursive()
    expected = 2.0
    assert abs(result - expected) < 1e-9, f"Test 5 failed: {result} vs {expected}"
    print(f"✓ Test 5 passed: sine function (recursive) = {result}")


def test_6_cosine_function_recursive():
    """测试 6: 余弦函数积分 (递归方法)
    积分 f(x)=cos(x) 在 [0, π/2]，期望结果：1
    """
    integrator = RombergIntegration(0.0, math.pi / 2, 1e-10, lambda x: math.cos(x))
    result = integrator.recursive()
    expected = 1.0
    assert abs(result - expected) < 1e-9, f"Test 6 failed: {result} vs {expected}"
    print(f"✓ Test 6 passed: cosine function (recursive) = {result}")


def test_7_exponential_function_recursive():
    """测试 7: 指数函数积分 (递归方法)
    积分 f(x)=e^x 在 [0, 1]，期望结果：e - 1 ≈ 1.718281
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: math.exp(x))
    result = integrator.recursive()
    expected = math.e - 1.0
    assert abs(result - expected) < 1e-9, f"Test 7 failed: {result} vs {expected}"
    print(f"✓ Test 7 passed: exponential function (recursive) = {result}")


def test_8_reciprocal_function_recursive():
    """测试 8: 倒数函数积分 (递归方法)
    积分 f(x)=1/x 在 [1, 2]，期望结果：ln(2) ≈ 0.693147
    """
    integrator = RombergIntegration(1.0, 2.0, 1e-10, lambda x: 1.0 / x)
    result = integrator.recursive()
    expected = math.log(2.0)
    assert abs(result - expected) < 1e-9, f"Test 8 failed: {result} vs {expected}"
    print(f"✓ Test 8 passed: reciprocal function (recursive) = {result}")


def test_9_polynomial_function_dynamic():
    """测试 9: 多项式函数积分 (动态规划方法)
    积分 f(x)=x^4 + 2*x^2 + 1 在 [0, 1]
    解析解: ∫(x^4 + 2*x^2 + 1)dx = x^5/5 + 2x^3/3 + x|_0^1 = 1/5 + 2/3 + 1 = 28/15 ≈ 1.866667
    """
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x**4 + 2 * x**2 + 1)
    result = integrator.dynamic_programming(maximum_step=20)
    expected = 28.0 / 15.0  # 1/5 + 2/3 + 1 = 28/15
    assert abs(result - expected) < 1e-9, f"Test 9 failed: {result} vs {expected}"
    print(f"✓ Test 9 passed: polynomial function (dynamic programming) = {result}")


def test_10_trigonometric_function_dynamic():
    """测试 10: 三角函数积分 (动态规划方法)
    积分 f(x)=sin(x)*cos(x) 在 [0, π]，期望结果：0
    """
    integrator = RombergIntegration(
        0.0, math.pi, 1e-10, lambda x: math.sin(x) * math.cos(x)
    )
    result = integrator.dynamic_programming(maximum_step=20)
    expected = 0.0
    assert abs(result - expected) < 1e-8, f"Test 10 failed: {result} vs {expected}"
    print(f"✓ Test 10 passed: trigonometric function (dynamic programming) = {result}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Running Cython Romberg Integration Tests")
    print("=" * 60)

    tests = [
        test_1_constant_function_recursive,
        test_2_linear_function_recursive,
        test_3_quadratic_function_recursive,
        test_4_cubic_function_recursive,
        test_5_sine_function_recursive,
        test_6_cosine_function_recursive,
        test_7_exponential_function_recursive,
        test_8_reciprocal_function_recursive,
        test_9_polynomial_function_dynamic,
        test_10_trigonometric_function_dynamic,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} error: {e}")
            failed += 1

    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {failed} test(s) failed!")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
