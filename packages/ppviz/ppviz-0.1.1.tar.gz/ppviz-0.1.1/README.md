# ppviz (python profiler viz'ualizer)

It's a GUI to explore/profile a python file.
(it's a little bit like snakeviz)

```
$ python -m pip install ppviz
$ ppviz sudoku.py
```
**remark**: "sudoku.py" is an example (and can be found [here](https://github.com/manatlan/sudoku_resolver/blob/master/sudoku.py)), you should use the python file you want to profile ;-)

![screenshot](screenshot.png?raw=true "Screenshot")

it uses [htag](https://github.com/manatlan/htag)(+htbulma) as gui system ;-)

currently, it only works on windows/linux/mac, but you'll need to have "google chrome" installed (it doesn't work on chromebook yet)
