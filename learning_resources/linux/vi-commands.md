```markdown
# vi Editor Command Reference Guide

The `vi` editor is a powerful text editor widely used in Unix-based systems. It has a modal interface, meaning it operates in different modes, such as command mode and insert mode, to distinguish between editing text and issuing commands. This guide covers the most useful and commonly used `vi` commands to help you get started and efficiently edit text files.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Modes](#basic-modes)
3. [Navigation](#navigation)
4. [Editing](#editing)
5. [Copy, Cut, and Paste](#copy-cut-and-paste)
6. [Search and Replace](#search-and-replace)
7. [File Operations](#file-operations)
8. [Undo and Redo](#undo-and-redo)
9. [Exiting vi](#exiting-vi)
10. [Advanced Commands](#advanced-commands)
11. [Customization](#customization)

## Getting Started

To start `vi`, type `vi filename` in the terminal, where `filename` is the file you want to edit.

```sh
vi myfile.txt
```

## Basic Modes

- **Command Mode**: The default mode for issuing commands. Press `Esc` to ensure you are in this mode.
- **Insert Mode**: For inserting text. Enter this mode by pressing `i`, `a`, `o`, etc. Exit back to command mode with `Esc`.

## Navigation

### Moving the Cursor
- `h` - Move left
- `j` - Move down
- `k` - Move up
- `l` - Move right
- `0` - Move to the beginning of the line
- `$` - Move to the end of the line
- `w` - Jump forward to the start of the next word
- `b` - Jump backward to the start of the previous word
- `gg` - Go to the beginning of the file
- `G` - Go to the end of the file
- `:n` - Go to line `n`

### Scrolling
- `Ctrl+f` - Scroll forward one screen
- `Ctrl+b` - Scroll backward one screen
- `Ctrl+d` - Scroll down half a screen
- `Ctrl+u` - Scroll up half a screen

## Editing

### Inserting Text
- `i` - Insert before the cursor
- `I` - Insert at the beginning of the line
- `a` - Append after the cursor
- `A` - Append at the end of the line
- `o` - Open a new line below the current line
- `O` - Open a new line above the current line

### Deleting Text
- `x` - Delete the character under the cursor
- `dw` - Delete the word starting at the cursor
- `dd` - Delete the current line
- `d$` - Delete from the cursor to the end of the line
- `d0` - Delete from the cursor to the beginning of the line

### Changing Text
- `cw` - Change the word from the cursor
- `cc` - Change the entire line
- `C` - Change from the cursor to the end of the line
- `r` - Replace a single character under the cursor
- `R` - Enter replace mode, replacing existing text as you type

## Copy, Cut, and Paste

### Copying (Yanking)
- `yw` - Yank (copy) a word
- `yy` - Yank a line
- `y$` - Yank to the end of the line

### Cutting
- `dw` - Cut a word
- `dd` - Cut a line
- `d$` - Cut to the end of the line

### Pasting
- `p` - Paste after the cursor
- `P` - Paste before the cursor

## Search and Replace

### Searching
- `/pattern` - Search forward for `pattern`
- `?pattern` - Search backward for `pattern`
- `n` - Repeat the last search in the same direction
- `N` - Repeat the last search in the opposite direction

### Replacing
- `:s/old/new/g` - Replace all occurrences of `old` with `new` in the current line
- `:%s/old/new/g` - Replace all occurrences in the entire file
- `:%s/old/new/gc` - Replace all occurrences with confirmation

## File Operations

### Saving
- `:w` - Write (save) the file
- `:wq` - Write and quit
- `:x` - Write and quit (similar to `:wq`)
- `:q!` - Quit without saving

### Reading and Writing
- `:e filename` - Edit (open) another file
- `:r filename` - Read a file and insert it at the cursor position

## Undo and Redo

- `u` - Undo the last change
- `U` - Undo all changes on the current line
- `Ctrl+r` - Redo undone changes

## Exiting vi

- `:q` - Quit if no changes have been made
- `:q!` - Quit without saving changes
- `:wq` or `:x` - Write changes and quit

## Advanced Commands

### Visual Mode
- `v` - Start visual mode (for selecting text)
- `V` - Start visual line mode
- `Ctrl+v` - Start visual block mode

### Macros
- `q<register>` - Start recording macro to register `<register>`
- `q` - Stop recording
- `@<register>` - Play macro from register `<register>`

### Indentation
- `>>` - Indent the current line
- `<<` - Unindent the current line
- `=` - Automatically indent the current line

## Customization

### Set Options
- `:set number` - Show line numbers
- `:set nonumber` - Hide line numbers
- `:set autoindent` - Enable automatic indentation
- `:set noautoindent` - Disable automatic indentation
- `:set tabstop=4` - Set tab width to 4 spaces
- `:set shiftwidth=4` - Set indentation width to 4 spaces
- `:set expandtab` - Convert tabs to spaces
- `:set noexpandtab` - Keep tabs as tabs
