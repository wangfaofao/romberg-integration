"""
setup.py - Cython Romberg 积分项目构建脚本

这个文件用于向后兼容。建议使用 pyproject.toml 进行现代化配置。
"""

from setuptools import setup, Extension
from Cython.Build import cythonize

# 定义扩展模块
ext_modules = [
    Extension(
        name="RombergIntegration",
        sources=["RombergIntegration.pyx"],
        language="c++",
        extra_compile_args=[
            "-O3",  # 最大优化
            "-march=native",  # 原生架构优化
            "-ffast-math",  # 快速数学运算
        ],
        extra_link_args=[],
    )
]

# 编译 Cython 扩展
extensions = cythonize(
    ext_modules,
    language_level="3",
    compiler_directives={
        "boundscheck": False,
        "wraparound": True,  # 允许负索引
        "cdivision": True,
        "language_level": "3",
    },
)

setup(
    ext_modules=extensions,
)
