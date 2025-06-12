# How Many Words Are There in War of the Worlds?

Let's jump right in! How many words are there in the book War of the Worlds? It's included in the repo as `wotw.txt.gz`, a plain text file that's been compressed with gzip. You might be tempted to do it in Python, but it's really quick in Bash:
```
gunzip wotw.txt.gz
wc wotw.txt
```

The first command uncompresses `wotw.txt.gz` to `wotw.txt` and deletes `wotw.txt.gz`. The second command counts the lines, words, and characters in `wotw.txt` (`wc` stands for "word count", but counts lines and characters too).

The rest of the tutorial assumes `wotw.txt.gz` exists, so let's recompress it.
```
gzip wotw.txt
```

::: aside
Aside: Most Bash commands print out help if you call them with `-h` or sometimes `--help`. Try it out with `gunzip` and `wc`! More complete help can usually be found in their man pages by calling e.g. `man wc`.
:::

Doing it in two lines is fine, but we can do better! (This will be a recurring theme.)
```
gunzip -c wotw.txt.gz | wc -w
```

What does `gunzip -c` do? It uncompresses `wotw.txt.gz`, but instead of writing to a file, it writes to `stdout` (which stands for "standard out"). The pipe symbol `|` means to pass `stdout` of the previous command to `stdin` (standard input) of the next command. So the command above uncompresses `wotw.txt.gz` and feeds it to `wc`, which counts the number of words and writes to its stdout. Since `wc` isn't attached to anything (there's no `|` after it), Bash prints it to the terminal.

Voila! In a single line, you got the number of words in War of the Worlds without writing any files!

::: aside
Aside: Both `gunzip` and `wc` will operate on files if you provide them as arguments, or on `stdin` if you don't. That's why `wc wotw.txt` in the first example and `wc -w` both work. This isn't anything special about Bash -- the authors of `gunzip` and `wc` coded them to do this, as it's pretty standard in Linux.
:::

Just like a command that isn't followed by `|` prints its stdout to the terminal, if a command expects stdin but isn't preceded by `|`, it'll read from the keyboard. Try typing `wc` and hitting enter. Note that nothing happens. Type a few lines. Although it looks like nothing is happening, it's in fact sending those lines to `wc`'s stdin. You can signal you're done by hitting ctrl-D. `wc` now reports how many lines, words, and characters you typed.

::: aside
Aside: In Bash, pressing ctrl-D sends an end-of-file (EOF) signal to whatever process is reading from `stdin`. If Bash itself is reading from `stdin` (that is, if you're about to type a command into a terminal), it will exit Bash! You can call `set -o ignoreeof` to prevent Bash from doing this. Add it to your `.bashrc` right now!
:::

# Count How Many Times Each Word Appears in War of the Worlds

We'll start with a simple but not very accurate method.
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | sort -nr | head
```

Run it and try to make out what it's doing, then we'll work through from left to right.

The `tr` command ("translate" or "transliterate") reads from its stdin, converts some characters, and writes them to its stdout. In this particular case, any time it sees the space character (specified by `' '` above), it converts it to newline (specified by `'\n'` above). To see what this does, try:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | head
```

The command above first uncompresses `wotw.txt.gz`, then replaces every space with a line break, then `head` prints the first few lines.

::: aside
Aside: `\n` is used to represent newline in many Bash programs (including `tr`), but it is just a convention that the authors of programs follow, nothing special in Bash itself.
:::

The `sort` command sorts in alphabetical order. It may seem strange to do this here, but it's required by `uniq`, which comes next in the pipeline. To check your knowledge, what do you think the following does? Try to work it out without copy/pasting it.
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | head | sort
```

The `uniq` command removes a line if it's the same as the line immediately before it. The `-c` causes the count of the number of adjacent identical lines to be output before the line. Try:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | head
```

That looks pretty weird, doesn't it? That's why I said the method is simple but not accurate -- it doesn't account for punctuation, blank lines, upper and lower case, etc. We'll fix that in a later section.

Here's the final command again:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | sort -nr | head
```

`sort -n` sorts in **numerical** rather than alphabetical order. `sort -r` reverses the order. Like many older Bash commands, command line options that are single letter can be mushed together, so `sort -nr` is the same as `sort -n -r`, and means to sort from highest number to lowest.

# Cleaning Up

I frequently run exactly the pipeline from the last section for quick and dirty word lists, but there's a problem. Try this:
```
echo 'Hello! My name is Adam.' | tr ' ' '\n'
```

See how punctuation is attached to the words? We want "Hello" and "Adam", not "Hello!" and "Adam.". Here's a little trick:
```
echo 'Hello! My name is Adam.' | tr -c 'a-zA-Z' '\n'
```

The `-c` argument to `tr` means to "complement" the characters in the match, so instead of matching letters, the above matches on all **non-letters**. This still isn't perfect since it's inserted newlines we don't need. You can use the `-s` ("squeeze") argument to `tr` to only insert one newline regardless of how many non-characters there are in a row. And while we're at it, let's convert uppercase to lowercase.
```
echo 'Hello! My name is Adam.' | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n'
```

There is one problem left. What happens here?
```
echo "What's your name?" | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n'
```

We're getting into edge cases here, where it's probably better to write a script or use an actual NLP package, so we're not going to fix it. Here's the final version:
```
gunzip -c wotw.txt.gz | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n' | sort \
                      | uniq -c | sort -nr | head
```