# !!! THIS IS A WORK IN PROGRESS !!!


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
Most Bash commands print out help if you call them with `-h` or sometimes `--help`. Try it out with `gunzip` and `wc`! More complete help can usually be found in their man pages by calling e.g. `man wc`.
:::

Doing it in two lines is fine, but we can do better! (This will be a recurring theme.)
```
gunzip -c wotw.txt.gz | wc -w
```

What does `gunzip -c` do? It uncompresses `wotw.txt.gz`, but instead of writing to a file, it writes to its `stdout` (which stands for "standard out"). The pipe symbol `|` means to pass `stdout` of the previous command to `stdin` (standard input) of the next command. So the command above uncompresses `wotw.txt.gz` and feeds it to `wc`, which counts the number of words and writes to its `stdout`. Since `wc` isn't attached to anything (there's no `|` after it), Bash prints it to the terminal.

Voila! In a single line, you got the number of words in War of the Worlds without writing any files!

::: aside
Both `gunzip` and `wc` will operate on files if you provide them as arguments, or on `stdin` if you don't. That's why `wc wotw.txt` and `gunzip -c wotw.txt.gz | wc -w` both work. This isn't anything special about Bash -- the authors of `gunzip` and `wc` coded them to do this, as it's pretty standard in Linux.
:::

Just like a command that isn't followed by `|` prints its `stdout` to the terminal, if a command expects `stdin` but isn't preceded by `|`, it'll read from the keyboard. Try typing `wc` and hitting enter. Note that nothing happens. Type a few lines. Although it looks like nothing is happening, it's in fact sending those lines to `wc`'s `stdin`. You can signal you're done by hitting ctrl-D. `wc` now reports how many lines, words, and characters you typed.

::: aside
In Bash, pressing ctrl-D sends an end-of-file (EOF) signal to whatever process is reading from `stdin`. If Bash itself is reading from `stdin` (that is, if you're about to type a command into a terminal), it will exit Bash! You can call `set -o ignoreeof` to prevent Bash from doing this. Add it to your `.bashrc` right now!
:::

# Count How Many Times Each Word Appears in War of the Worlds

We'll start with a simple but not very accurate method.
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | sort -nr | head
```

Run it and try to make out what it's doing, then we'll work through from left to right.

The `tr` command ("translate" or "transliterate") reads from its `stdin`, converts some characters, and writes them to its `stdout`. In this particular case, any time it sees the space character (specified by `' '` above), it converts it to newline (specified by `'\n'` above). To see what this does, try:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | head
```

The command above first uncompresses `wotw.txt.gz`, then replaces every space with a line break, then `head` prints the first few lines.

::: aside
`\n` is used to represent newline in many Bash programs (including `tr`), but it is just a convention that the authors of programs follow. It's just two regular old characters.
:::

The `sort` command sorts in alphabetical order. It may seem strange to do this here, but it's required by `uniq`, which comes next in the pipeline. To check your knowledge, what do you think the following does? Try to work it out without copy/pasting it.
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | head | sort
```

The `uniq` command removes a line if it's the same as the line immediately before it. The `-c` causes the count of the number of adjacent identical lines to be output before the line. Try:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | head
```

The output looks pretty weird, doesn't it? That's why I said the method is simple but not accurate -- it doesn't account for punctuation, blank lines, upper and lower case, etc. We'll fix that in a later section.

Here's the final command again:
```
gunzip -c wotw.txt.gz | tr ' ' '\n' | sort | uniq -c | sort -nr | head
```

`sort -n` sorts in **numerical** rather than alphabetical order. `sort -r` reverses the order. Like many older Bash commands, command line options that are single letter can be mushed together, so `sort -nr` is the same as `sort -n -r`, and means to sort from highest number to lowest.

::: aside
Each command in a pipeline of commands runs in parallel, and Linux handles all the buffering between commands. This typically makes one-liners faster than running each command separately.
:::

## Handling Punctuation

I frequently run exactly the pipeline from the last section for a quick and dirty word lists, but there's a problem. Try this:
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

We're getting into edge cases, where it's probably better to write a script or use an actual NLP package, so we're not going to fix it. Here's the final version:
```
gunzip -c wotw.txt.gz | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n' | sort \
                      | uniq -c | sort -nr | head
```

# Errors

As a programming language, Bash is terrible at error handling. For anything big, you should be using a more modern language. But even on the command line, it's useful to deal with errors. We'll demonstrate with the `find` command:
```
find . -name '*.html' > html_files.list
```

The `find` command looks for all files in or under the current directory that end with `.html` and writes them to its `stdout`. The `>` takes `stdout` from the previous command and writes it to the file specified right after, overwriting if it already exists.

What happens if there's an error? Try the following:
```
find /etc -name 'man*'
```

This tries to list all files under `/etc` that start with `man`. This will fail on directories you don't have permission for. Notice that the errors are interspersed with the files it found. Try the following:
```
find /etc -name 'man*' > man_files.list
```

Are you surprised by the result? Run `cat man_files.list` to see what's in it.

What's going on here is that `find` writes files it finds to its `stdout` and errors to its `stderr`. Just like `stdout`, `stderr` will end up printed in the terminal if it's not otherwise redirected. `>` redirected `stdout` to a file; `stderr` ended up on the terminal.

You can redirect `stderr` using `2>`:
```
find /etc -name 'man*' > man_files.list 2> find_errors
```

Since both `stdout` and `stderr` are redirected, nothing is output to the terminal. The files found are in `man_files.list` and the errors are in `find_errors`.

Let's put it all together. Find all files that start with `man` under `/etc`, exclude ones that contain `management`, and throw away any error messages:
```
find /etc -name 'man*' 2> /dev/null | grep -v management
```

The `find` command runs. The `2> /dev/null` causes `find`'s `stderr` to be discarded and the `|` causes `find`'s `stdout` to be passed to `grep`. `grep -v management` outputs all lines from its `stdin` to `stdout` except those containing "management". Since there's nothing redirecting `grep`'s `stdout`, it gets output to the terminal.

For reasons lost to time, `2|` doesn't redirect `stderr` even though it really seems like it should.

::: aside
In Linux, the file system is used for lots of unusual stuff. Devices like microphones, network connections, and even information about what's running on your computer are all controlled through things that look like files in the file system. `/dev/null` is one of these. It isn't a "real" file, but rather something you can connect `stdout` or `stderr` to if you want to just discard it.
:::

# Command Substitution

Anywhere in Bash that you could write a string, you can instead run a command and its `stdout` will be used. For example, you could write:
```
echo The number of words in War of the Worlds is 59923
```

But you could also write:
```
echo The number of words in War of the Worlds is $(gunzip -c wotw.txt.gz | wc -w)
```

Anything within the `$()` construct is executed as a command, and its `stdout` is used right in the same place.

::: aside
`$(cmd)` is the more modern way to write `` `cmd` ``, which you may see in older code.
:::

The most common use of command substitution is probably setting variables:
```
nwords=$(gunzip -c wotw.txt.gz | wc -w)
echo The number of words in War of the Worlds is $nwords
```

But you really can use it anywhere. Can you figure out what this does?
```
$(echo l)$(echo s) *.html
```


# What Common Words Aren't in War of the Worlds?

Let's revisit War of the Worlds. What are common words that don't appear in it? We'll use the tool `comm` (for "common") to figure it out. Take a look at the files `words1` and `words2` in this directory. Then run:
```
comm words1 words2
```
The first column of output lists lines in `words1` that are not in `words2`. The second lists lines in `words2` that are not in `words1`. The final column lists lines that are in both.

You can suppress any of the columns with command line arguments. For example, to list only lines that are in the first file:
```
comm -2 -3 words1 words2
```

This suppresses lines that are only in the second and are in both. Try other combinations of `-1`, `-2`, and `-3` and see if they do what you'd expect.

Now imagine `words1` contains all the words from War of the Worlds and `words2` contained a list of common words. What would the command be?

::: aside
`comm` requires both input files to be sorted.
:::

## Running on War of the Worlds

You can use (almost) the command we ran before to get all the unique words in War of the Worlds:
```
gunzip -c wotw.txt.gz | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n' | sort -u > wotw_words.sorted
```

The only difference is `sort -u`, which sorts its `stdin` and removes duplicate lines.

The file `1000_words.gz` in this repo's directory contains a list of 1000 common words in order of how common they are. For later use, we need them sorted.
```
gunzip -c 1000_words.gz | sort > 1000_words.sorted
```

To count how many words in `1000_words.sorted` do **not** occur in `wotw_words.sorted`:
```
comm -1 -3 wotw_words.sorted 1000_words.sorted | wc -l
```

## Let's Do It In One Line!

```
comm -1 -3 <(gunzip -c wotw.txt.gz | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n' | sort -u) <(gunzip -c 1000_words.gz | sort) | wc -l
```

::: aside
There's a reason they call it "code"!
:::

Let's break it down. You can think of `<(cmd)` as a Bash construct that runs `cmd` and stores its `stdout` into a new file. It then replaces the `<(cmd)` in the command you typed with the name of that file. So if you type:
```
wc <(echo foo bar baz)
```

The first thing that happens is Bash runs `echo foo bar baz` and stores it in a file named something like `/dev/fd/63`. It then runs `wc /dev/fd/63`.

So the steps for our one-liner above are:

1. Bash runs `gunzip -c wotw.txt.gz | tr 'A-Z' 'a-z' | tr -cs 'a-z' '\n' | sort -u` and stores it in e.g. `/dev/fd/63`.
2. Bash runs `gunzip -c 1000_words.gz | sort` and stores it in e.g. `/dev/fd/64`.
3. Bash runs `comm -1 -3 /dev/fd/63 /dev/fd/64 | wc -l`

::: aside
The steps are actually run simultaneously, so you can benefit from parallelism, but watch out if the commands have side effects other than writing to `stdout`! Linux handles streaming the data -- it's not actually stored on the file system.
:::

The `<(cmd)` construct is known as "input process substitution", and you can use it anywhere you'd use a file that gets read.


# Output Process Substitution

There's also the construct `>(cmd)`, known as "output process substitution". You use it anywhere you'd normally use a file that you're writing to, but want to do additional processing on. Probably the most common usage is if you're processing something big, and you want to do more than one thing with the output without creating temporary files.

Let's say I want to find all the chapter titles in War of the Worlds. I also want the number of words on each line and the number of characters on each line. Here's how I'd do it in three lines:
```
gunzip -c wotw.txt.gz | grep -E '^[A-Z ]+$' | grep -v CHAPTER > chapters
gunzip -c wotw.txt.gz | awk '{print NF}' > words_per_line
gunzip -c wotw.txt.gz | awk '{print length}' > characters_per_line
```

The first command finds lines that are all upper case, excludes ones that have the word "CHAPTER", and writes to the file "chapters". The second command uses `awk` to print the number of fields `NF` in each line and stores it in "words_per_line". The last command prints the length of each line.

::: aside
`awk` is itself a programming language. It's quite good and processing tabular text; that is, text separated by whitespace or other delimiters. It reads from its `stdin` and processes line by line. It's small and very fast.
:::

To do it in one line, we'll use the `tee` command, which reads its `stdin` and copies to both its `stdout` **and** to all files specified on its command line. Imagine you want to write the current date to three files. The obvious way to do it is:
```
date > file1
cp file1 file2
cp file1 file3
```

But we can do it in one line with:
```
date | tee file1 file2 > file3
```

`tee` writes to the files specified on its command line (`file1` and `file2`) and also to its `stdout` (which ends up in `file3`). 

So to process War of the Worlds and write the `chapters`, `words_per_line`, and `characters_per_line` files, we can replace the files with the output process substitution construct `>()`:

```
gunzip -c wotw.txt.gz \
  | tee >(grep -E '^[A-Z ]+$' | grep -v CHAPTER > chapters) \
        >(awk '{print NF}' > words_per_line) \
  | awk '{print length}' > characters_per_line \
```

This uncompresses War of the Worlds and feeds it to the `stdin` of three different pipelines simultaneously:

1. `grep -E '^[A-Z ]+$' | grep -v CHAPTER > chapters`
2. `awk '{print NF}' > words_per_line`
3. `awk '{print length}' > characters_per_line`

This example is somewhat contrived, but imagine you're streaming something huge from a network connection and you want only subsets of the data.

::: aside
Another common use of `tee` is if you want to write results to a file **and** see them on your terminal. I use this all the time to monitor long jobs. Just run e.g. `longcmd | tee save.out`. Whatever `longcmd` writes to `stdout` will end up both in `save.out` and on the terminal (since `tee`'s `stdout` isn't redirected).
:::

# A Whirlwind Tour of Useful Tools

There are a huge number of tools that ship with Linux distributions, and even more available as packages. This section gives you a whirlwind tour of some of the more common ones.

Don't reinvent the wheel!

::: aside
All the tools introduced in this section take options I don't describe. If a command kinda seems like it could do what you want, try `-h` or `--help` and see if it does!
::: 

- **awk** — *A mini programming language that excels at tabular data.*  
  Example: Print the second word of each line of `wotw.txt.gz`:
  ```
  gunzip -c wotw.txt.gz | awk '{print $2}'
  ```

- **cat** — *Copy all files specified on the command line to `stdout`. You can use `-` to mean `cat`'s `stdin`.*  
  Example: Output the words in `words1`, `words2`, then the word "states":
  ```
  echo states | cat words1 words2 -
  ```

- **comm** — *Print lines in common between two files.*  
  Example: Show words in `words1` that aren't in `words2`:
  ```
  comm -2 -3 words1 words2
  ```

- **cut** — *Extract fields from lines.*  
  Example: Show the 2nd through 4th words in each line of `wotw.txt.gz`:
  ```
  gunzip -c wotw.txt.gz | cut -f2-4 -d' '
  ```

- **file** - *Show information about the file type.*
  ```
  file wotw.txt.gz tutorial.html
  ```

- **find** - *A mini programming language to find files.*
  Example: List all plain files that are newer than `style.html`:
  ```
  find . -type f -newer style.html
  ```

- **grep** - *Find lines matching a regular expression.*
  Example: Find all words in `wotw.txt.gz` that consist of a vowel followed by a consonant followed by a vowel:
  ```
  gunzip -c wotw.txt.gz | grep -o '\b[aeiou][^aeiou][aeiou]\b'
  ```

- **head** - *Print the first N lines or characters of a file. Can also print all but the last N.*
  Example: Print the first 200 characters of `tutorial.html`:
  ```
  head -c 200 tutorial.html
  ```
  
- **less** - *Show a file one page at a time.*
  ```
  gunzip -c wotw.txt.gz | less
  ```

- **paste** - *Combine files side-by-side.*
  ```
  paste words1 words2
  ```

- **sed** - *Mini language to modify files.*
  Example: Replace all strings of digits in `wotw.txt.gz` with "\<NUMBER\>":
  ```
  gunzip -c wotw.txt.gz | sed 's/[0-9][0-9]*/<NUMBER>/g'
  ```

- **seq** - *List numbers in order with formatting.*
  ```
  seq -f 'This is line %g' 1 10
  ```

- **shuf** - *Efficiently extract lines at random without replacement.*
  ```
  gunzip -c wotw.txt.gz | shuf -n5
  ```

- **sort** - *Sort lines by various criteria.*
  Example: Sort `wotw.txt.gz` first in reverse alphabetical order of the first word, then in alphabetical order of the third word:
  ```
  gunzip -c wotw.txt.gz | sort -k1,1r -k3,3
  ```

- **tail** - *Print the last N lines or characters of a file. Can also print starting at N.*
  Example: Print the third line onward of `tutorial.html`:
  ```
  tail -n +3 tutorial.html
  ```

  `tail` can also monitor a file for new text, outputting as lines are added. This is useful for watching a running process. For example, you can watch system logs in real time with:
  ```
  tail -f /var/log/syslog
  ```

- **tee** - *Copies its `stdin` to files named on the command and its `stdout`.*
  Example: Create three files with the current date:
  ```
  date | tee file1 file2 > file3
  ```

# Quoting

Run the following:
```
echo    Hello   my   name  is    Adam
```

Are you surprised by the result? To explain, start by looking at `echo.py`:
```
cat echo.py
```

This is just a simplistic example of `echo` written in Python. It shows what arguments the program actually gets.

::: aside
In Linux and similar environments, arguments are always strings.
:::

Try calling:
```
./echo.py     Hello   my   name  is    Adam
```

What's happening is Bash does a lot of processing of the command line you type before it calls the command. You've seen a bunch of that in the examples -- process substitution, command substitution, even variables. Try the following:
```
name=Adam
./echo.py    Hello   my   name  is    $name
```

See that `$name` has been replaced by "Adam" before `echo.py` sees it? Well, another thing Bash does when processing the command line is remove extra white space. To pass strings that contain whitespace, you have to use quotes:
```
./echo.py '    Hello   my   name  is    $name'
```
What the single quote does is tell Bash to treat everything between the quotes as a single argument, ignoring all special characters. So the above command passes only *one* argument to `echo.py`, and it contains the string `$name` rather than "Adam". Try to predict what this will do then run it and see how you did!
```
./echo.py '    Hello   my   name  is'    $name
```

Bash also supports double quotes. They're similar to single quotes, but `$` **is** expanded, both for variables and command substitution:
```
book=wotw
./echo.py "   The book $book has:  $(gunzip -c $book.txt.gz | wc -w) words."
```

You can use single quotes within double quotes and double quotes within single quotes. **BUT** the inner quotes have no special meaning!
```
./echo.py "The book is called '$book'"
./echo.py 'The book is called "$book"'
```

The last type of quoting uses the backslash character `\`. It tells bash to ignore any special meaning of the following character (including whitespace!). Compare and contrast:
```
./echo.py The book is called "$book"
./echo.py The book is called \"$book\"
./echo.py "The book is called \"$book\""
```

Now for a doozy:
```
./echo.py "The book is called "$book""
```

The problem is that Bash looks for quote from left to right. So first it finds `"The book is called "` and substitutes `The book is called `. Then it sees `$book` and substitutes `wotw`. Lastly, it sees `""` and substitutes the empty string. Since there are no unquoted spaces, it's one argument.

