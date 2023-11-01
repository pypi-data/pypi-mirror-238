# PyBing
Python wrapper for Bing Search results.

## Implementation

```python
from PyBingRAG.search import BingSearch

bing = BingSearch("Sachin Tendulkar")
bing_results = bing.get_results(num=4, max_lines=15)
bing_rag = bing.rag_output(prompt, nlines, hfkey)
```
