maixcdk-example: example component for MaixCDK
=====

## Publish

```
python setup.py sdist
# python setup.py sdist bdist_wheel
twine upload dist/*
```


## Install

```
pip install maixcdk-example
```

Set index url for pip temporarily:
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple maixcdk-example
```

Or globally set index url for pip:
```
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```






