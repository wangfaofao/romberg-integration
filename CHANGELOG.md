# Changelog

所有对此项目的重要更改都记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，
项目遵循 [语义版本](https://semver.org/) 规范。

## [1.0.0] - 2025-01-27

### Added
- 初始发布
- 两种积分方法实现:
  - `recursive()`: 递归方法，使用哈希表缓存中间结果
  - `dynamic_programming()`: 动态规划方法，构建 Romberg 表
- 完整的单元测试（10 个测试用例）
- 详细的 API 文档
- PyPI 发布指南
- GitHub Actions 工作流配置示例

### Features
- 高精度数值积分（使用 long double）
- 接口与 C++ 版本一致
- 纯 Cython 实现，最大化性能
- 支持任意被积函数（通过 Python 可调用对象）
- 灵活的精度控制

### Documentation
- README.md: 项目说明和使用示例
- PYPI_PUBLISHING_GUIDE.md: 完整的发布指南
- 代码内详细的 docstring 文档

## 计划中的功能

### [1.1.0] - 计划中
- [ ] 添加自适应 Romberg 积分方法
- [ ] 性能基准测试
- [ ] NumPy 数组支持
- [ ] 并行计算支持

### [2.0.0] - 计划中
- [ ] 添加多维积分方法
- [ ] GPU 加速支持
- [ ] 更多数值方法（Simpson、Gauss 等）

---

## 发布历史说明

### 版本号规则
- **MAJOR**: 不兼容的 API 变化
- **MINOR**: 新功能添加（向后兼容）
- **PATCH**: 错误修复（向后兼容）

### 发布流程
1. 更新版本号 (pyproject.toml)
2. 更新此 CHANGELOG
3. 提交更改到 git
4. 创建 git tag
5. 运行发布脚本
