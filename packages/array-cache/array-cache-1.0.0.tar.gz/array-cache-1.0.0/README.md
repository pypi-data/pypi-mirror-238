# array-cache

## Usage

```python
from array_cache import ArrayCache

# save to cache every x item
CACHE_DELAY=10

cached_array = array_cache.ArrayCache(data_array, "my-identifier", CACHE_DELAY)
for one_word in cached_array.get_data():
    # use here
```

## Upload to PyPi

```sh
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m build
python3 -m pip install --upgrade twine
# create egg-info folder
python3 -m twine upload dist/*
```

## License

Licensed under the MIT License - [LICENSE](LICENSE)
