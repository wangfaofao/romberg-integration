# Romberg Integration - Cython 版本

这是 C++ 版本 Romberg 积分算法的 Cython 改造，保持接口一致性，最大化计算效率。

## 项目结构

```
romberg/
├── RombergIntegration.pyx    # Cython 实现
├── setup.py                  # 构建脚本
├── test_romberg.py          # 单元测试
└── README.md                # 项目说明
```

## 编译安装

### 环境要求

- Python 3.6+
- Cython >= 0.29.0
- 支持 C++ 的编译器（gcc, clang, MSVC 等）

### 安装步骤

1. **安装依赖**：
```bash
pip install cython numpy
```

2. **编译扩展模块**：
```bash
python setup.py build_ext --inplace
```

3. **验证安装**：
```bash
python test_romberg.py
```

## 使用示例

```python
from RombergIntegration import RombergIntegration
import math

# 创建积分器：积分 sin(x) 在 [0, π]，精度 1e-10
integrator = RombergIntegration(0.0, math.pi, 1e-10, lambda x: math.sin(x))

# 方法 1: 递归方法（使用哈希表缓存）
result = integrator.recursive()
print(f"Recursive result: {result}")  # 期望：2.0

# 方法 2: 动态规划方法（使用二维表）
integrator2 = RombergIntegration(0.0, math.pi, 1e-10, lambda x: math.sin(x))
result2 = integrator2.dynamic_programming(maximum_step=20)
print(f"DP result: {result2}")  # 期望：2.0

# 查看中间结果
print(f"Romberg table: {integrator2.romberg_table}")
print(f"Precision table: {integrator2.precision_table}")
```

## API 文档

### 类: `RombergIntegration`

#### 构造函数

```python
RombergIntegration(a: float, b: float, precision: float, integrand: callable)
```

**参数**：
- `a` (float): 积分下界
- `b` (float): 积分上界
- `precision` (float): 精度要求（绝对误差）
- `integrand` (callable): 被积函数，接受 float，返回 float

#### 方法

##### `recursive() -> float`

执行 Romberg 积分（递归方法）。

使用递归方法和哈希表缓存计算，逐步提高精度直到满足要求。

**返回值**：计算得到的积分结果

**示例**：
```python
result = integrator.recursive()
```

##### `dynamic_programming(maximum_step: int = 20) -> float`

执行 Romberg 积分（动态规划方法）。

使用迭代动态规划方法构建 Romberg 表，逐步提高精度。

**参数**：
- `maximum_step` (int): 最大迭代步数，默认 20

**返回值**：计算得到的积分结果

**示例**：
```python
result = integrator.dynamic_programming(maximum_step=15)
```

#### 属性

##### `romberg_map`

返回递归方法中使用的缓存字典（哈希表）。键为 "m-k" 格式的字符串。

##### `romberg_table`

返回动态规划方法中构建的 Romberg 表（二维列表）。

##### `precision_table`

返回精度变化列表，记录每一步的精度改进。

## 性能优化

本 Cython 实现采用以下优化措施：

1. **静态类型**：使用 `long double` 进行高精度浮点计算
2. **编译指令**：
   - `boundscheck=False`: 关闭边界检查
   - `wraparound=False`: 关闭负索引包装
   - `cdivision=True`: 启用 C 风格整数除法
3. **C 库函数**：
   - 使用 `libc.math` 中的 `pow` 和 `fabs` 避免 Python 调用开销
4. **优化编译**：
   - `-O3` 最大优化级别
   - `-march=native` 利用原生 CPU 特性
   - `-ffast-math` 快速数学运算

## 与 C++ 版本的对比

| 特性 | C++ 版本 | Cython 版本 |
|------|---------|-----------|
| 语言 | C++ | Cython/Python |
| 编译 | g++ 直接编译 | Cython 编译为 C/C++ |
| 性能 | 原生 C++ | 接近 C++ |
| 易用性 | 需编译 | Python 接口 |
| 接口一致性 | 基础 | **完全一致** |

## 测试覆盖

实现了 10 个单元测试，涵盖：

1-8: 递归方法测试
- 常函数、线性、二次、三次多项式
- 正弦、余弦、指数、倒数函数

9-10: 动态规划方法测试
- 复杂多项式、三角组合函数

**运行测试**：
```bash
python test_romberg.py
```

**期望输出**：
```
10/10 tests passed
```

## 设计原则

1. **接口一致**：保持与 C++ 版本的接口风格一致
2. **静态类型优先**：尽可能使用 Cython 的静态类型
3. **无 cpdef**：仅使用 `cdef` 内部方法，保持清晰的 Python/C 边界
4. **高效缓存**：使用 Python dict 和 list 作为 Romberg 表存储
5. **最优计算**：采用 C 库数学函数加速

## 注意事项

- 被积函数必须是 Python 可调用对象（如 lambda、函数等）
- 精度参数应使用相对较小的值（推荐 1e-8 ~ 1e-12）
- 对于高精度需求，可增加 `maximum_step` 参数值

## 许可证

与 C++ 版本保持一致

## 作者

Cython 改造版本
