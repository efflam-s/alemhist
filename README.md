# alemhist
Graph visualization for alembic history

This python script parses the output of alembic history and outputs a git-like ascii
graph with each migration hash and label.

Optional: if you want color support, install colorama with `pip install colorama`

On Linux, you can place the [alemhist shell script](./alemhist) in ~/.local/bin and make
it executable with `chmod +x ~/.local/bin/alemhist`.

Alternatively, you can make an alias in your .bashrc or .bash_aliases, for example :

```shell
alias alemhist=alembic history --indicate-current | python3 ~/alemhist/alemhist.py --color | less -FRX
```

See the [alemhist](./alemhist) file for personalization tips.

