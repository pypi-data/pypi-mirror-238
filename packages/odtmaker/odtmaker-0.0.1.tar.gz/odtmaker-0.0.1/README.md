# ODTMaker 

Generator for small documents in ODT format. For now just the parser for contents is working.


## Installing

`sudo python setup.py install`


## Running

`python -m odtmaker`


## Creating contents

All following examples should be passed to `odtmaker/contentParser.ContentParser.parse` method as `raw_data` parameter.

For string:

```
region_name:{region contents}
```

will return a dict with `region_name` key and `region contents` value.


Contents can have line breaks:

```
region_name:{region
contents}
```


*"Garbage" between regions are ignored:*

```
region1:{contents}
comments, or something else
region2:{contents of region 2}
```

generates two regions (`region1` and `region2`), with respective contents.



*Its possible create "consecutive" regions*

```
'region1,region2,region3:{contents 1|contents 2|contents 3}'
```

generates:

`region1`, `region2` and `region3`.

