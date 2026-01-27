#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模块名称: test_romberg_compare.py
功能描述: Cython 与 C++ 版本 Romberg 积分对标测试

本模块对比 Cython 版本与 C++ 版本的实现结果，验证两个版本的数值精度和算法正确性。
以 C++ 版本的测试结果为标准答案，确保 Cython 版本的计算结果完全一致。

作者: wangheng <wangfaofao@gmail.com>
版本: 1.0.0
更新时间: 2026-01-27
"""

import math
import sys
from RombergIntegration import RombergIntegration


class TestResult:
    """测试结果记录"""

    def __init__(self, test_name, expected, actual, error, passed):
        self.test_name = test_name
        self.expected = expected
        self.actual = actual
        self.error = error
        self.passed = passed


def approx_equal(expected, actual, tolerance):
    """比较两个浮点数是否相等（允许误差范围）"""
    return abs(expected - actual) < tolerance


def print_result(result):
    """打印单个测试结果"""
    status = "✓ PASS" if result.passed else "✗ FAIL"
    print(f"{result.test_name:<50} {status}")
    print(f"  期望值: {result.expected:.12e}")
    print(f"  实际值: {result.actual:.12e}")
    print(f"  误差:  {result.error:.12e}\n")


def test_1_constant_function():
    """测试1: 常函数 f(x) = 1, 积分区间 [0, 1]
    C++ 标准答案: 1.0, 误差: 0.0
    """
    expected = 1.0
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: 1.0)
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 1: Constant f(x) = 1 on [0, 1]", expected, result, error, passed
    )


def test_2_linear_function():
    """测试2: 线性函数 f(x) = x, 积分区间 [0, 1]
    C++ 标准答案: 0.5, 误差: 0.0
    """
    expected = 0.5
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x)
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 2: Linear f(x) = x on [0, 1]", expected, result, error, passed
    )


def test_3_quadratic_function():
    """测试3: 二次函数 f(x) = x^2, 积分区间 [0, 1]
    C++ 标准答案: 0.333333333333, 误差: 0.0
    """
    expected = 1.0 / 3.0
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x * x)
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 3: Quadratic f(x) = x² on [0, 1]", expected, result, error, passed
    )


def test_4_cubic_function():
    """测试4: 三次函数 f(x) = x^3, 积分区间 [0, 1]
    C++ 标准答案: 0.25, 误差: 0.0
    """
    expected = 0.25
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x * x * x)
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 4: Cubic f(x) = x³ on [0, 1]", expected, result, error, passed
    )


def test_5_sine_function():
    """测试5: 正弦函数 f(x) = sin(x), 积分区间 [0, π]
    C++ 标准答案: 2.0, 误差: 8.055622141567e-17
    """
    expected = 2.0
    integrator = RombergIntegration(0.0, math.pi, 1e-10, lambda x: math.sin(x))
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 5: Sine f(x) = sin(x) on [0, π]", expected, result, error, passed
    )


def test_6_cosine_function():
    """测试6: 余弦函数 f(x) = cos(x), 积分区间 [0, π/2]
    C++ 标准答案: 1.0, 误差: 1.209969624494e-16
    """
    expected = 1.0
    integrator = RombergIntegration(0.0, math.pi / 2.0, 1e-10, lambda x: math.cos(x))
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 6: Cosine f(x) = cos(x) on [0, π/2]", expected, result, error, passed
    )


def test_7_exponential_function():
    """测试7: 指数函数 f(x) = e^x, 积分区间 [0, 1]
    C++ 标准答案: 1.718281828459, 误差: 1.451746708958e-16
    """
    expected = math.e - 1.0
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: math.exp(x))
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 7: Exponential f(x) = e^x on [0, 1]", expected, result, error, passed
    )


def test_8_reciprocal_function():
    """测试8: 倒数函数 f(x) = 1/x, 积分区间 [1, e]
    C++ 标准答案: 1.0, 误差: 1.767249541151e-16
    """
    expected = 1.0
    integrator = RombergIntegration(1.0, math.e, 1e-10, lambda x: 1.0 / x)
    result = integrator.recursive()
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 8: Reciprocal f(x) = 1/x on [1, e]", expected, result, error, passed
    )


def test_9_dp_quadratic_function():
    """测试9: 动态规划方法 - 二次函数 f(x) = x^2, 积分区间 [0, 1]
    C++ 标准答案: 0.333333333333, 误差: 0.0
    """
    expected = 1.0 / 3.0
    integrator = RombergIntegration(0.0, 1.0, 1e-10, lambda x: x * x)
    result = integrator.dynamic_programming(20)
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 9: DP method - Quadratic f(x) = x² on [0, 1]",
        expected,
        result,
        error,
        passed,
    )


def test_10_dp_sine_function():
    """测试10: 动态规划方法 - 正弦函数 f(x) = sin(x), 积分区间 [0, π]
    C++ 标准答案: 2.0, 误差: 8.055622141567e-17
    """
    expected = 2.0
    integrator = RombergIntegration(0.0, math.pi, 1e-10, lambda x: math.sin(x))
    result = integrator.dynamic_programming(20)
    error = abs(expected - result)
    passed = approx_equal(expected, result, 1e-8)
    return TestResult(
        "Test 10: DP method - Sine f(x) = sin(x) on [0, π]",
        expected,
        result,
        error,
        passed,
    )


def run_all_tests():
    """运行所有对标测试"""
    print("=" * 70)
    print("Romberg Integration - Cython vs C++ 对标测试")
    print("=" * 70)
    print()

    tests = [
        test_1_constant_function,
        test_2_linear_function,
        test_3_quadratic_function,
        test_4_cubic_function,
        test_5_sine_function,
        test_6_cosine_function,
        test_7_exponential_function,
        test_8_reciprocal_function,
        test_9_dp_quadratic_function,
        test_10_dp_sine_function,
    ]

    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
            print_result(result)
        except Exception as e:
            print(f"✗ {test_func.__name__} 执行错误: {e}\n")
            results.append(TestResult(test_func.__name__, 0, 0, float("inf"), False))

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print("=" * 70)
    print("测试摘要")
    print("=" * 70)
    print(f"通过: {passed}/{total}")
    print(f"失败: {total - passed}/{total}")
    print("=" * 70)

    # 对比说明
    print("\n对标结果说明：")
    print("✓ 所有测试与 C++ 版本结果一致")
    print("✗ 如果有失败，表示 Cython 版本与 C++ 版本存在差异")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
