## stdf tamer
This package was originally developed at DC Jona / ams-OSRAM.

It is a general purpose stdf file parser / generator / simulator / analyser and converter.

But mainly it is used for these use cases.:

 - write STDF files from robotframework test cases
 - analyse STDF file content
 - convert STDF files to other file formats

## Usage:
```
  stdfconvert --help
  stdfanalyse --help
  stdfrenamer --help
  stdfrerunwithnewlimits --help
```


## Source.:
https://gittf.ams-osram.info/labor-rapperswil-jona/ams-tamer

## API Documentation.:
https://labor-rapperswil-jona.git-pages.ams-osram.info/ams-tamer/index.html


# Tips and tricks

## Conversion Speed

In order to speed up conversion of STDF files to other file formats use 2 stdf-tamer installations,
one in pypy for the actuall parsing of hte STDF files, and one in CPython to perform the acutall
converison using polars. For this please use a /etc/stdf-tamer.toml config file like this

[converter]
stdf_to_pickle_cmd   = "/path2pypywithstdf-tamer/bin/pypy -m  ams_rw_stdf.convert stdf2pickle"
