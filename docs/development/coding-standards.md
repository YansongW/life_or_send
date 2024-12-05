# 代码规范

## Python 代码风格

我们遵循 PEP 8 规范，并使用以下工具确保代码质量：

### 代码格式化

使用 `black` 进行代码格式化：
```bash
black .
```

### 导入排序

使用 `isort` 整理导入语句：
```bash
isort .
```

### 代码检查

使用 `flake8` 进行代码检查：
```bash
flake8
```

### 类型检查

使用 `mypy` 进行类型检查：
```bash
mypy .
```

## 命名规范

- 类名：使用 PascalCase
- 函数名：使用 snake_case
- 变量名：使用 snake_case
- 常量：使用 UPPER_CASE
- 私有成员：使用 _leading_underscore

## 文档规范

### 函数文档

使用 Google 风格的文档字符串：

```python
def function_name(param1: type1, param2: type2) -> return_type:
    """函数简短描述。

    详细描述（可选）。

    Args:
        param1: 参数1的描述
        param2: 参数2的描述

    Returns:
        返回值的描述

    Raises:
        ErrorType: 异常描述
    """
    pass
```

### 类文档

```python
class ClassName:
    """类的简短描述。

    详细描述（可选）。

    Attributes:
        attr1: 属性1的描述
        attr2: 属性2的描述
    """
    pass
```

## 测试规范

- 测试文件命名：`test_*.py` 或 `*_test.py`
- 测试类命名：`Test*`
- 测试函数命名：`test_*`
- 每个测试用例应该只测试一个功能点
- 使用 `pytest.mark.asyncio` 装饰异步测试
- 使用 `pytest.fixture` 管理测试资源

## Git 提交规范

提交信息格式：
```
<type>(<scope>): <subject>

<body>

<footer>
```

类型（type）：
- feat: 新功能
- fix: 修复
- docs: 文档
- style: 格式
- refactor: 重构
- test: 测试
- chore: 构建

示例：
```
feat(session): 添加会话超时处理

- 添加会话自动清理功能
- 优化内存使用

Closes #123
``` 