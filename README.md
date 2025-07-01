# alemhist
Graph visualization for alembic history

This python script parses the output of alembic history and outputs a git-like ascii
graph with each migration hash and label.

### Installation
On Linux, you can place the [alemhist shell script](./alemhist) in ~/.local/bin and make
it executable with `chmod +x ~/.local/bin/alemhist`.

Alternatively, you can make an alias in your .bashrc or .bash_aliases, for example :

```shell
alias alemhist=alembic history --indicate-current | python3 ~/alemhist/alemhist.py --color | less -FRX
```

Optional: if you want color support, install colorama with `pip install colorama`

See the [alemhist](./alemhist) file for personalization tips.


# ale
Improved user experience of alembic CLI

### Example usage
- `ale up`: upgrade to head revision
- `ale do`: downgrade one revision
- `ale hist`: Show history as a graph, similar to `git log --oneline --graph`
- `ale m`: Merge current heads
- `ale rebase <revision> <new_base>`: Make `new_base` the new parent of `revision`
- `ale reindex <revision1> <revision2>`: Assign new random ids to `revision1` and `revision2`

### Installation
Add the following line to your .bashrc or .bash_aliases:

```shell
ale() { `python3 ~/alemhist/ale.py $*`; }
```

If needed, change the paths of `OTHER_EXE` in `ale.py` and `alemhist.py` in `alemhist` to match the path of the current folder (by default, `~/alemhist`.

### Personnalization
I added some aliases and default parameters for alembic commands.
Feel free to change them or add more depending on your needs, by modifying `ale.py`.
