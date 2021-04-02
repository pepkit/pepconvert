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

## Write a plugin

Write a custom filter/formatter like this:
    
## 1. Add entry_points to setup.py

The [setup.py](setup.py) file uses `entry_points` to specify a mapping of refgenie hooks to functions to call.

```
    entry_points={
        "pep.filters": ["basic=pepconvert:my_basic_plugin",
                        "yaml=pepconvert:complete_yaml",
                        "csv=pepconvert:csv",
                        "yaml-samples=pepconvert:yaml_samples"]
        }
```

The format is: `'pep.filters': 'FILTER_NAME=PLUGIN_PACKAGE_NAME:FUNCTION_NAME'`.

- "FILTER_NAME" can be any unique identifier for your plugin
- "PLUGIN_PACKAGE_NAME" must be the name of python package the holds your plugin.
- "FUNCTION_NAME" must match the name of the function in your package

## 2. Write functions to call

The module contains the functions, with names corresponding to the `FUNCTION_NAME` in the entry points above. These functions **must take a peppy.Project object as sole parameter**. Example:

```
import peppy
  
def my_custom_filter(p):
    import re
    for s in p.samples:
        sys.stdout.write("- ")
        out = re.sub('\n', '\n  ', yaml.safe_dump(s.to_dict(), default_flow_style=False))
        sys.stdout.write(out + "\n")
```

That's it! Install the package and it should run your functions at the specified hook entry points.
