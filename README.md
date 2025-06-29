# !!! THIS IS A WORK IN PROGRESS !!!

# Bash Tutorial

This is a tutorial for bash by Adam Janin. It is intended for people who have a passing familiarity with bash (e.g. you know what a path is, `cd ~/git/bash_tutorial` makes sense to you, etc.). It is inspired by [Unix for Poets](https://www.cs.upc.edu/~padro/Unixforpoets.pdf) by Ken Church (probably from the early '90s), but has been updated for more modern sensibilities.

# Installation

```
mkdir -p ~/git
cd ~/git
git clone https://github.com/ajanin/bash_tutorial.git
cd bash_tutorial
```

# How to Read

Many formats are supported. For plain text, read tutorial.md. For HTML, open tutorial.html in your browser. If you're really old fashioned, you can print tutorial.pdf.

You should have a terminal window with Bash open and be in the top level directory of the repository (the one with the file `wotw.txt.gz`), as the tutorial expects you to be interacting with Bash and using the files in this repo as you're reading.

You can read the HTML on github: [README.hmtl](https://ajanin.github.io/bash_tutorial) [tutorial.html](https://ajanin.github.io/bash_tutorial/tutorial.html)

# Notes

This section contains notes on how the tutorial was assembled and how to regenerate some of the files (e.g. if you fork). Most readers needn't continue.

The source for the tutorial is `tutorial.md`. It's written in [Pandoc's markdown format](https://pandoc.org/MANUAL.html#pandocs-markdown). This is reasonably easy to read as plain text, but other formats are easy to generate with [Pandoc](https://pandoc.org). I generate the various format with the commands:
```
docker run --rm -v $(pwd):/data -u $(id -u):$(id -g) pandoc/core -s -H style.html --metadata pagetitle="Bash Tutorial" -o tutorial.html tutorial.md
```

The file `1000_words.gz` is an extract of word counts I had lying around from a web
scrape. I removed words with apostrophes for pedagogic reasons.

The files `words1` and `words2` were generated with:
```
gunzip -c 1000_words.gz | shuf -n 10 | tee >(shuf -n 5 | sort > words1) | shuf -n5 | sort > words2
```

Yes, I really do write one-liners like that routinely!
