# Bash Tutorial

This is a tutorial for bash by Adam Janin. It is intended for people who have a passing familiarity with bash (e.g. you know what a path is, `cd ~/git/bash_tutorial` makes sense to you, etc.). It is inspired by (Unix for Poets)[https://web.stanford.edu/class/cs124/kwc-unix-for-poets.pdf] by Ken Church from the early '90s, but has been updated for more modern sensibilities.

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