# 测试指南

## 测试环境设置

1. 安装测试依赖：
```bash
pip install -r requirements-dev.txt
```

2. 配置测试数据库：
```bash
cp .env.example .env.test
# 编辑 .env.test 设置测试环境配置
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试
```bash
# 运行特定文件
pytest tests/test_wechat.py

# 运行特定类
pytest tests/test_wechat.py::TestWeChatAPI

# 运行特定方法
pytest tests/test_wechat.py::TestWeChatAPI::test_verify_signature
```

### 生成覆盖率报告
```bash
pytest --cov=./ --cov-report=html
```

## 测试类型

### 单元测试
- 位置：`tests/unit/`
- 命名：`test_*.py`
- 测试单个函数或类的功能

### 集成测试
- 位置：`tests/integration/`
- 命名：`test_*_integration.py`
- 测试多个组件的交互

### 端到端测试
- 位置：`tests/e2e/`
- 命名：`test_*_e2e.py`
- 测试完整的用户场景

## 测试数据

### Fixtures
- 位置：`tests/conftest.py`
- 用途：提供测试数据和资源
- 作用域：function, class, module, session

### Mock 数据
- 使用 `pytest-mock` 模拟外部依赖
- 使用 `httpx` 模拟 HTTP 请求
- 使用 `fakeredis` 模拟 Redis

## 最佳实践

1. 每个测试函数只测试一个功能点
2. 使用有意义的测试名称
3. 遵循 AAA 模式：Arrange-Act-Assert
4. 避免测试之间的依赖
5. 保持测试简单和可维护
6. 及时清理测试资源 