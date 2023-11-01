# PyBing
Python wrapper for Bing Search results.

## Implementation

```python
from PyBing.search import BingSearch

bing = BingSearch("Sachin Tendulkar")
bing_results = bing.get_results(num=4, max_lines=15)
```
