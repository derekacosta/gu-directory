# GU Directory

Python module to search the [Georgetown University Directory](https://contact.georgetown.edu/).

## Installation

```bash
pip install git+https://github.com/derekacosta/gu-directory
```

## Usage

Results are returned as `(Name, NetID, Title, Department, Phone Number)`

### Simple Search

```python
from directory import GUDirectory

directory = GUDirectory()
results = directory.simple_search('Justice')
for result in results:
	print(result)
```

### Advanced Searches

The default behavior is to match exactly i.e. `first_match='exact'`

```python
print_results(directory.advanced_search(first='justice'))
```

The other match options are `'starts_with'` and `'contains'`

```python
print_results(directory.advanced_search(first='jus', first_match='starts_with'))
print_results(directory.advanced_search(first='sti', first_match='contains'))
```

Search fields include `'first'`, `'last'`, `'phone'`, and `'department'`

```python
print_results(directory.advanced_search(
    first='jus',
    first_match='starts_with',
    last='smi',
    last_match='starts_with',
    department='nhs',
    department_match='contains'
))
```

Searches can also search on just `'students'` or `'employees'`.  Searches default to `'both'` i.e. `category='both'`

```python
print_results(directory.advanced_search(last='suh', category='students'))
print_results(directory.advanced_search(last='suh', category='employees'))
```
