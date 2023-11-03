# PyBing
Python wrapper for Bing Search results.

## Implementation

```python
from PyBingRAG.search import BingSearch

bing = BingSearch("Sachin Tendulkar")
#num - num of results to return
#max_lines - maximum number of lines/sentences to return in each result
bing_results = bing.get_results(num=4, max_lines=15)
# bing_results[i]['content'] - scrapped content
# nlines - num of iterations
# hfkey - hugging face secret key
print(bing.rag_output("Tell me about Mr. Narendra Modi?", n_iters=15, bing_results, hfkey))

```
