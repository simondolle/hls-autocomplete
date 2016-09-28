===================
hls-autocomplete
===================

[![Build Status](https://travis-ci.org/simondolle/hls-autocomplete.svg?branch=master)](https://travis-ci.org/simondolle/hls-autocomplete)

hls_autocomplete is a tool that adds autocompletios to the `hdfs dfs -ls` and `hadoop dfs -ls` commands.

Installation
-------------

Clone the repository locally : `git clone https://github.com/simondolle/hls-autocomplete.git`.

Edit your `.bashrc` and source the `SOURCEME` file.

Configuration
-------------

Edit `.hls_autocomplete.conf`.

Replace `USER` with your username and `HTTPFS` with your httpfs server.

Copy `.hls_autocomplete.conf` to your home directory.

Usage
-----

To list files in your HDFS filesystem, use the `hls` command. (instead of `hdfs dfs -ls` or `hadoop dfs -ls`)

Press the TAB key to autocomplete the filenames, as you would do with a `ls` command.


