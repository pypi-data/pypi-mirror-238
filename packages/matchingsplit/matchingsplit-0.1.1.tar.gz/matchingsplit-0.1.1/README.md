## matchingsplit

Split a string or group a collection of words into a list by matching another list of similar words, to create accurate subtitles from the actual script and inaccurate (generated) subtitles.

Example

```python
from matchingsplit import split

>>> split("this must be a good thing", reference=["this", "is", "a", "good", "thing"])
['this', 'must be', 'a', 'good', 'thing']

>>> split("this is a good thing", reference=["this", "must", "be", "a", "good", "thing"])
['this', '', 'is', 'a', 'good', 'thing']

>>> split("a big foo bar", ["a", "big", "ff"])
['a', 'big', 'foo bar']
```
