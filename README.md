# pepconvert

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