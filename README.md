# BML converters

Start a BML converter using a GUI.

See also the [Bridge Markup Language](https://github.com/gpaulissen/bml) project.

# Installation

This utility needs Python 3. You can install it using the Microsoft Store
(accessible via the Windows 10 start button) or just Google `download Python 3`.

## Start a command prompt

Please Google it if you don't know how.

## Install required Python libraries

Go to the src folder and install them from the command line using pip:

```
$ cd src
$ pip install -r requirements.txt
```

First please note that the dollar sign is the prompt sign and not a character you have to type.
Next, please do move into src first, since the root also contains a (different) `requirements.txt`.

You may need to use pip3 instead of pip if pip does not point to a Python 3 installation.

## Install LaTeX

In order to create PDFs you need to install LaTeX. There are several
distributions available. On Windows [MiKTeX](https://miktex.org/) is a good
option. The executable latexmk must be in the PATH otherwise the GUI will not
display the option to convert BML to PDF.

### Latex packages

The following packages are needed for BML: dirtree, listliketab, parskip, pbox and txfonts.

Install them like this:

```
$ tlmgr install dirtree listliketab parskip pbox txfonts
```

### Perl

Since latexmk will usually need Perl, please install Perl. On Unix and Mac OS X this won't be necessary since Perl should already have been installed. On Windows you can download [Strawberry Perl](https://strawberryperl.com/).

On Unix or Mac OS X you can verify that Perl is installed with:

```
$ which perl
```

On Windows:

```
$ where perl
```

# Usage

## Launch the Python script src/bml-converter.py

This can be done directory from a command prompt or by creating a (Windows)
shortcut on your Desktop (right mouse click, choose New) or an alias on Unix/Mac OS X.

Using the command prompt:

```
$ cd src
$ python bml-converter.py
```

## Help

In the left top corner of the GUI screen there is a Help button.
