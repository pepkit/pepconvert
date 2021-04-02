# pepconvert

Provides a CLI to convert a PEP into different output formats. These include some built-in formats, like `csv` (which takes your spits out a *processed* `csv` file, with project/sample modified), `yaml`, and a few others. It also provides a plugin system so that you can write your own Python functions to provide custom output formats, which can then be used with pepconvert.

## Install

Install with: `pip install .`

## Run

Run with:

```
# view available formats
pepconvert list
```


```
# Convert a PEP into a different format
pepconvert convert config.yaml -f basic
running plugin pep
Project 'pepconvert' (/home/nsheff/code/pepconvert/config.yaml)
5 samples: WT_REP1, WT_REP2, RAP1_UNINDUCED_REP1, RAP1_UNINDUCED_REP2, RAP1_IAA_30M_REP1
Sections: pep_version, sample_table, subsample_table
```

Format 'basic' is built in. You can write your own plugins to output whatever format you want.


You can use `-f yaml` to get a yaml representation of the samples in your project:

```
pepconvert convert config.yaml -f yaml
```
