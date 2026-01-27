# Cython Romberg 积分项目 - PyPI 发布完整指南

## 1. 发布文件类型说明

### 1.1 源代码包 (Source Distribution - sdist)
- **文件格式**: `.tar.gz` 或 `.zip`
- **包含内容**: 源代码 (`.pyx`, `.py`, 等), 文档, 配置文件
- **用途**: 用户可在本地编译（需要编译器和依赖）
- **优点**: 
  - 体积最小
  - 支持所有平台和 Python 版本
  - 用户可看到完整源码
- **缺点**: 
  - 安装时需要本地编译
  - 安装速度慢
  - 用户需要安装编译工具链

### 1.2 二进制包 (Wheels - .whl)
- **文件格式**: `.whl`
- **包含内容**: 预编译的二进制文件 (`.so`, `.pyd` 等)
- **用途**: 用户可直接安装，无需编译
- **优点**:
  - 安装速度快
  - 无需编译工具链
  - 更好的用户体验
- **缺点**:
  - 文件体积较大
  - 需要为每个平台/Python 版本编译一次
  - 平台相关性强

### 1.3 Cython 项目的特殊性

对于 Cython 项目，您需要：

1. **源代码包** (源码 + .pyx 文件)
   - 用于希望查看源码的用户
   - 用于自定义编译的用户
   - 用于不支持的平台的用户

2. **Wheels** (预编译的 .so/.pyd 文件)
   - Linux (manylinux) wheels - 多个 Python 版本
   - macOS wheels - 多个 Python 版本
   - Windows wheels - 多个 Python 版本

## 2. 建议的发布策略

### 推荐方案：源码 + 多平台 Wheels

这是最完整和用户友好的方案：

1. **源代码包 (sdist)**
   - 供开发者使用
   - 包含 `.pyx` 源文件
   - 用户可在特殊平台上编译

2. **Wheels**
   - Linux: manylinux2014 (cp38 到 cp313)
   - macOS: universal2 (cp38 到 cp313)
   - Windows: win_amd64 (cp38 到 cp313)

## 3. 步骤指南

### 3.1 准备工作

#### 3.1.1 更新项目信息

编辑 `pyproject.toml`:
```toml
[project]
name = "RombergIntegration"
version = "1.0.0"  # 更新版本号
description = "..."
authors = [{name = "Your Name", email = "your.email@example.com"}]
```

#### 3.1.2 更新版本号

遵循 [语义版本](https://semver.org/) 规范:
- Major.Minor.Patch (例如: 1.0.0, 1.1.0, 2.0.0)

### 3.2 本地构建测试

#### 步骤 1: 清理旧的构建文件
```bash
rm -rf build/ dist/ *.egg-info/
```

#### 步骤 2: 构建源代码包和 wheel
```bash
# 方法 1: 使用 build 包 (推荐)
python -m pip install build twine
python -m build

# 方法 2: 使用旧方式
python setup.py sdist bdist_wheel
```

#### 步骤 3: 验证构建文件
```bash
ls -lh dist/
# 应该看到:
# RombergIntegration-1.0.0.tar.gz  (源码包)
# RombergIntegration-1.0.0-cp313-cp313-linux_x86_64.whl  (wheel)
```

#### 步骤 4: 检查包内容
```bash
# 检查 wheel 文件
python -m zipfile -l dist/RombergIntegration-1.0.0-cp313-*.whl

# 检查源码包
tar -tzf dist/RombergIntegration-1.0.0.tar.gz | head -20
```

### 3.3 上传到 TestPyPI (可选但推荐)

#### 步骤 1: 获取 API Token

1. 访问 https://test.pypi.org
2. 注册账户
3. 创建 API Token (Account Settings -> API tokens)

#### 步骤 2: 配置 .pypirc

创建 `~/.pypirc`:
```ini
[distutils]
index-servers =
    testpypi
    pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # 您的 token

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # 您的 token
```

#### 步骤 3: 上传到 TestPyPI
```bash
python -m twine upload --repository testpypi dist/*
```

#### 步骤 4: 测试安装
```bash
pip install -i https://test.pypi.org/simple/ RombergIntegration
python -c "from RombergIntegration import RombergIntegration; print('Success!')"
```

### 3.4 上传到官方 PyPI

#### 步骤 1: 获取 PyPI Token

1. 访问 https://pypi.org
2. 注册账户（或使用现有账户）
3. 创建 API Token (Account Settings -> API tokens)

#### 步骤 2: 上传
```bash
python -m twine upload dist/*
```

系统会提示您输入用户名和密码（使用 `__token__` 作为用户名，token 作为密码）

#### 步骤 3: 验证上传
```bash
# 等待几分钟后
pip install RombergIntegration

# 测试
python -c "from RombergIntegration import RombergIntegration; print('Success!')"
```

## 4. 使用 GitHub Actions 自动化发布 (推荐)

创建 `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  build-wheels:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12', '3.13']

    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build cython
      
      - name: Build wheels
        run: python -m build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          path: dist/

  publish:
    needs: build-wheels
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/download-artifact@v3
        with:
          path: dist/
      
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

使用:
```bash
# 发布版本
git tag v1.0.0
git push origin v1.0.0
# GitHub Actions 会自动构建并上传
```

## 5. 版本更新流程

### 5.1 修改版本号

编辑 `pyproject.toml` 中的版本号：
```toml
version = "1.0.1"  # 从 1.0.0 更新到 1.0.1
```

### 5.2 更新 CHANGELOG

创建 `CHANGELOG.md`:
```markdown
## [1.0.1] - 2025-01-27

### Fixed
- Fixed bug in dynamic_programming method
- Improved numerical stability

### Changed
- Updated documentation

## [1.0.0] - 2025-01-27

### Added
- Initial release
- Recursive method with memoization
- Dynamic programming method
```

### 5.3 提交和标记

```bash
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to 1.0.1"
git tag v1.0.1
git push origin main
git push origin v1.0.1
```

## 6. 最佳实践清单

### 发布前

- [ ] 所有测试通过 (`python test_romberg.py`)
- [ ] 更新了版本号
- [ ] 更新了 CHANGELOG
- [ ] 更新了 README
- [ ] 检查了 LICENSE
- [ ] 验证了 pyproject.toml 配置

### 发布时

- [ ] 在 TestPyPI 上测试
- [ ] 验证 wheel 文件包含二进制文件 (不是源码)
- [ ] 验证源码包包含 .pyx 文件
- [ ] 检查包在不同 Python 版本上的安装

### 发布后

- [ ] 验证 PyPI 上的项目页面
- [ ] 测试 pip install 安装
- [ ] 测试导入和基本功能
- [ ] 创建 GitHub Release
- [ ] 更新项目主页和文档

## 7. 常见问题

### Q: 需要为每个平台编译 wheel 吗?

**A**: 对于生产环境，推荐为主要平台编译:
- Linux (manylinux2014, manylinux_2_28)
- macOS (universal2, x86_64, arm64)
- Windows (win_amd64, win32)

您可以使用 `cibuildwheel` 工具自动化这个过程。

### Q: 如何处理不支持的平台?

**A**: 发布源码包，用户可在本地编译:
```bash
pip install --no-binary :all: RombergIntegration
```

### Q: wheel 和源码包都要发布吗?

**A**: 推荐发布两种:
- **源码包**: 供开发者和特殊环境使用
- **Wheels**: 供普通用户快速安装

### Q: 如何更新已发布的版本?

**A**: PyPI 不允许覆盖已发布的版本。您必须更新版本号:
```toml
version = "1.0.1"  # 从 1.0.0 更新
```

## 8. 文件清单 - 完整项目应包含

```
romberg-integration/
├── RombergIntegration.pyx          # Cython 源代码
├── RombergIntegration.pxd          # (可选) Cython 头文件
├── setup.py                        # 向后兼容构建脚本
├── pyproject.toml                  # 现代构建配置 (推荐)
├── MANIFEST.in                     # 源码包文件清单
├── LICENSE                         # MIT 许可证
├── README.md                       # 项目说明
├── CHANGELOG.md                    # 版本历史
├── .gitignore                      # Git 忽略列表
├── test_romberg.py                 # 单元测试
├── .github/
│   └── workflows/
│       └── publish.yml             # GitHub Actions 发布配置
└── docs/                           # (可选) 文档目录
```

## 9. 后续改进建议

1. **增加测试覆盖**: 在 `tests/` 目录中添加更多测试
2. **添加文档**: 使用 Sphinx 生成 HTML 文档
3. **性能基准**: 添加基准测试脚本
4. **持续集成**: 配置 GitHub Actions 自动运行测试
5. **类型提示**: 添加 `.pyi` 类型提示文件

## 10. 参考资源

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI 官网](https://pypi.org/)
- [Cython 文档](https://cython.readthedocs.io/)
- [setuptools 文档](https://setuptools.pypa.io/)
- [twine 文档](https://twine.readthedocs.io/)
