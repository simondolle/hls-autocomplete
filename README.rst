===================
hls-autocomplete
===================

.. image:: https://travis-ci.org/simondolle/hls-autocomplete.svg?branch=master
        :target: https://travis-ci.org/simondolle/hls-autocomplete

hls_autocomplete is a tool that adds autocompletios to the `hdfs dfs -ls` and `hadoop dfs -ls` commands.

Installation
-------------

Clone the repository locally : `git clone https://github.com/simondolle/hls-autocomplete.git`.

Edit your `.bashrc` and source the `SOURCEME` file.

Usage
-----

To list files in your HDFS filesystem, use the `hls` command. (instead of `hdfs dfs -ls` or `hadoop dfs -ls`)

Press the TAB key to autocomplete the filenames, as you would do with a `ls` command.

Internals
---------
hls_autocomplete uses a cache file  - stored in ~/.hls_cache - to find completion.

Each time you run `hls`, the cache is updated.


If `hls` does not suggest the right completions, the cache is probably outdated.

Run `hls`on the desired directory, it will update the cache and should solve your issue.

