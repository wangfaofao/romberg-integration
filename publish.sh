#!/usr/bin/env bash
# publish.sh - PyPI 发布脚本

set -e

echo "=========================================="
echo "Romberg Integration PyPI 发布脚本"
echo "=========================================="

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 检查版本号
echo -e "${YELLOW}[1/8] 检查项目配置...${NC}"
if ! grep -q "version = " pyproject.toml; then
    echo -e "${RED}错误: 无法在 pyproject.toml 中找到版本号${NC}"
    exit 1
fi

VERSION=$(grep "^version = " pyproject.toml | cut -d'"' -f2)
echo -e "${GREEN}版本号: $VERSION${NC}"

# 2. 运行测试
echo -e "${YELLOW}[2/8] 运行测试...${NC}"
if [ -f "test_romberg.py" ]; then
    python test_romberg.py || {
        echo -e "${RED}测试失败!${NC}"
        exit 1
    }
else
    echo -e "${YELLOW}警告: 找不到测试文件${NC}"
fi

# 3. 清理旧的构建文件
echo -e "${YELLOW}[3/8] 清理旧的构建文件...${NC}"
rm -rf build/ dist/ *.egg-info/ RombergIntegration.c RombergIntegration.cpp __pycache__/
echo -e "${GREEN}清理完成${NC}"

# 4. 检查依赖
echo -e "${YELLOW}[4/8] 检查构建依赖...${NC}"
python -m pip install -q build twine cython || {
    echo -e "${RED}依赖安装失败${NC}"
    exit 1
}
echo -e "${GREEN}依赖检查完成${NC}"

# 5. 构建包
echo -e "${YELLOW}[5/8] 构建源码包和 wheel...${NC}"
python -m build || {
    echo -e "${RED}构建失败${NC}"
    exit 1
}
echo -e "${GREEN}构建完成${NC}"

# 6. 验证包
echo -e "${YELLOW}[6/8] 验证构建的包...${NC}"
python -m twine check dist/* || {
    echo -e "${RED}包检查失败${NC}"
    exit 1
}
echo -e "${GREEN}包检查通过${NC}"

# 7. 列出生成的文件
echo -e "${YELLOW}[7/8] 生成的文件:${NC}"
ls -lh dist/
echo ""

# 8. 确认上传
echo -e "${YELLOW}[8/8] 准备上传到 PyPI...${NC}"
echo -e "${YELLOW}即将上传以下文件到 PyPI:${NC}"
ls dist/

read -p "是否继续? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}正在上传到 PyPI...${NC}"
    python -m twine upload dist/*
    echo -e "${GREEN}上传完成!${NC}"
    echo -e "${GREEN}项目主页: https://pypi.org/project/RombergIntegration/${NC}"
else
    echo -e "${YELLOW}取消上传${NC}"
fi
