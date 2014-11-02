# JavaScript Object GENerator

JSOGEN is a random JSON generator. The instances are generated from the supplied template. The template is a JSON file that can contain special expressions for each string wrapped in `{{` and `}}`.

The script can be executed as

```
$ python jsogen/jsogen.py [-h] [-s SEED] [-o OUTPUT] [-q] template
```
where the meaning of arguments is following:
```
template                     template file or directory
-h, --help                   show this help message and exit
-s SEED, --seed SEED         random generator seed value
-o OUTPUT, --output OUTPUT   output file or directory (if not specified std out is used)
-q, --quiet                  do not print any debug info
```

The most important parameter is `template` that contains path to the template file. If the path is a directory, all template files in the directory are recursively generated to the `OUTPUT` directory that is required in this case.

## Template file

Let's start with example:

```js
[
    "{{repeat(1, 2)}}",
    {
        "boolean": "{{boolean()}}",
        "int": "{{integer(-100, 999)}}",
        "str": "{{string(10, 20)}}",
        "float": "{{float(-10, 10, precision=4)}}"
    }
]
```
Executing `jsogen` on this template will generate array with 1 or 2 object elements. Each object will contain 4 fields with keys equal to the values in the example. The `boolean` element will be boolean element that is either `true` or `false`, the `int` will be integer in the range [-100, 999], the `str` with 10 to 20 characters and the last one float value in the range [-10, 10] with precision 4. An example result could be following:

```js
[
    {
        "int": 150,
        "str": "dasflkg asdfk ds",
        "boolean": true,
        "float": 2.4356
    }
]
```
Note that the order of columns in object does not have to be the same.
