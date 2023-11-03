# 👁 Voight-Kampff

This repository contains a small Python package, `voight-kampff`, which provides a
command line application, `vk`, which can be used to run the following linters
(including some spell checkers):

- [Bandit](https://github.com/PyCQA/bandit)
- [Black](https://github.com/psf/black)
- [cspell](https://github.com/streetsidesoftware/cspell)
- [isort](https://github.com/PyCQA/isort)
- [Flake8](https://github.com/PyCQA/flake8)
- [Markdownlint](https://github.com/DavidAnson/markdownlint)
- [Pydocstyle](https://github.com/PyCQA/pydocstyle)
- [Pylint](https://github.com/PyCQA/pylint) (including
  [spelling](https://docs.pylint.org/en/1.6.0/features.html#spelling-checker))
- [Pyright](https://github.com/microsoft/pyright)

This can be useful to check your entire repository before pushing the code to the
remote.

In case you are wondering about the name, it was inspired by a device used to determine
whether an individual is a replicant in the 1982 movie, [Blade
Runner](https://en.wikipedia.org/wiki/Blade_Runner#Voight-Kampff_machine).

## Prerequisites

Before you can use Voight-Kampff to run the linters, they need be installed. Some of the
linters are written in Python and can be installed through `pip`. These are specified as
dependencies of Voight-Kampff and will be installed automatically when you install the
`voight-kampff` package. However, a few of the linters are
[Node.js](https://nodejs.org/en/)-based and need to be installed using `npm`. Finally
for the spell checking feature in Pylint to work, you need to have
[Enchant](https://abiword.github.io/enchant/) installed. That can be done through
[Homebrew](https://formulae.brew.sh) or `apt` depending on your OS. Installation
instructions for all dependencies on macOS as well as Debian, Ubuntu and similar are
provided below.

### Installing prerequisites on macOS

This section briefly describes how you can install the prerequisites on macOS. These
instructions assume you already have [Homebrew](https://formulae.brew.sh) installed.

First you should install the prerequisites that are installed through Homebrew as
follows:

```shell
brew install enchant
brew install node
```

The above lines will install Enchant and Node.js. Now that you have Node.js installed,
you can install the linters that are based on Node.js:

```shell
npm install --global cspell
npm install --global markdownlint-cli2
npm install --global pyright
```

### Installing prerequisites on Linux - Debian / Ubuntu

First you should install the prerequisites that are installed through `apt` as follows:

```shell
sudo apt install enchant-2
sudo apt install npm
```

The above lines will install Enchant and Node.js. Now that you have Node.js installed,
you can install the linters that are based on Node.js:

```shell
sudo npm install --global cspell
sudo npm install --global markdownlint-cli2
sudo npm install --global pyright
```

## Installation

Assuming you have the prerequisites installed as described above, you can install
Voight-Kampff as follows:

```shell
pip3 install voight-kampff
```

## Usage

To run all of the above linters on the current directory, simply run:

```shell
vk
```

If you want to run only one or a few specific linters, say Black and Pylint, you can do
that as follows:

```shell
vk black pylint
```

By default, Voight-Kampff will keep running the subsequent linters if the current one
fails the check. If you prefer that Voight-Kampff stops as soon as any linter fails, you
can specify the `--break-on-error` flag -- or the short version, `-B`:

```shell
vk -B
```
