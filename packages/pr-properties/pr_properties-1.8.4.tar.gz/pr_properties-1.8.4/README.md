安装
pip install pr-properties

这是一个读写properties工具

```python
from pr_properties import pr_properties

# 读写properties文件
p = pr_properties.read(r'./pool.properties')  # p = PropertiesHandler(r"./pool.properties").read()
print(p['master.initialSize'])  # 4
# 支持get
print(p.get('master.initialSize'))
# 修改
p['master.initialSize'] = 5
# 写入,写入后会关闭文件;写入功能请慎重使用
p.write()
p.read(r'./pool.properties')
# 验证是否修改
print(p['master.initialSize'])  # 5
```


