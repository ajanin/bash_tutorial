# Bash Tutorial

This is a tutorial for bash by Adam Janin. It is intended for people who have a passing familiarity with bash (e.g. you know what a path is, `cd ~/git/bash_tutorial` makes sense to you, etc.). It is inspired by (Unix for Poets)[https://www.cs.upc.edu/~padro/Unixforpoets.pdf] by Ken Church (probably from the early '90s), but has been updated for more modern sensibilities.

# Installation

```
mkdir ~/git
cd ~/git
git clone https://github.com/ajanin/bash_tutorial.git
cd bash_tutorial
```

# How to Read

Many formats are supported. For plain text, read tutorial.md. For HTML, open tutorial.html. If you're really old fashioned, you can print tutorial.pdf.

You should have a terminal window with Bash open and be in the top level directory of the repository (the one with the file `wotw.txt.gz`). You can ignore other files in the repository -- they're used for building various versions of the tutorial.

# Ignore below here

Stuff below here is notes to myself on building and such. It'll eventually be moved to a Makefile or removed.

```
sudo docker run --rm -v $(pwd):/data -u $(id -u):$(id -g) pandoc/core -s -H style.html --metadata pagetitle="Bash Tutorial" -o tutorial.html tutorial.md
```

```
bunzip2 -c ~/reddit/RC_2017-03/RC_2017-03.1gram.counts.bz2 | head -n 2000 | grep -v "'" | grep -v '<' | grep -v 'shit' | head -n 1000 | cut -f2 -d' ' | gzip > 1000_words.gz
```

```
gunzip -c 1000_words.gz | shuf -n 10 | tee >(shuf -n 5 | sort > words1) | shuf -n5 | sort > words2
```