SM Manager
==========

A simple tool used to manage and load songs onto any drive to use with the karaoke machines made by Singing Machine.

It supports managing your meta data, as well as downloading and importing songs from YouTube.


Table of Contents
====================

<!--ts-->
   * [SM Manager](#sm-manager)
   * [Table of Contents](#table-of-contents)
   * [Quickstart](#quickstart)
   * [Requirements](#requirements)
   * [Usage](#usage)
     * [--doctor](#--doctor)
     * [--import \<file\>](#--import-)
     * [--disk-root \<path\>](#--disk-root-)
<!--te-->


Quickstart
==========

```
$ python smm.py --import songs.tsv
```


Requirements
============

Here is a list of things needed to run this script:
  * Python3 -- [website](https://www.python.org/about/gettingstarted/)
  * Run `pip install -r requirements.txt` to install the following dependencies:
    * pytube -- [website](https://github.com/nficano/pytube)
    * pywin32 (for Windows users) -- [website](https://pypi.org/project/pywin32/)


Usage
=====

Explained below are the supported commands you can use to manage your songs.


--import <file>
---------------

Bulk download and import songs specified in a `.tsv` file. Click [here](songs.tsv)
for an example file.

```
$ python smm.py --import songs.tsv
```


--doctor
--------

This option tells the script to only run the post-import doctor command. This command
will create missing song meta data, update existing-but-outdated meta data, and remove
extra meta data files.

In order for this command to figure out the songs meta data (read: be useful), the files
in the data directory must be named in the following format: `Genre__Artist__Title.mp4`.

```
$ python smm.py --doctor
```


--disk-root <path>
------------------

Explicitly set the path of where you want the script to run. Useful for
dry-runs, or if the script cannot detect where your disk is mounted.

```
$ python smm.py --import songs.tsv --disk-path /Volumes/SMDISK
```
