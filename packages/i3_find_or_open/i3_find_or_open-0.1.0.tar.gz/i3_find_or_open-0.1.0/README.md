# i3-find-or-open
This repo provides a command-line tool: `i3-find-or-open` that can find a window by regex in your i3wm instance, and display it, or execute any command if it does not exist.

It is intended to help you bind keys that will reliably show you a program, whether or not it is open already.

Let's say I wanted to use this to bind `$mod+o` to open my Obsidian vault:
```
bindsym $mod+o exec --no-startup-id "i3-find-or-open '^.* - vault - Obsidian v([1-9]|\.)+$' 'obsidian'"
```
## Installation
i3-find-or-open is available on [pypi](https://pypi.org/), and the best way to install it (if you don't want to break your system python installation) is to use [pipx](https://pypa.github.io/pipx/installation/) (N.B. there is an Arch package `python-pipx` to install this with).
```
pipx install i3-find-or-open
```
