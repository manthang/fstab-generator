# fstab-generator

fstab-generator is a Python tool for generating Linux [fstab](https://man7.org/linux/man-pages/man5/fstab.5.html) files from YAML configuration files.

## A brief on the approach used to solve this problem

The main program starts from lines(77-80) in which using PyYAML as the parser for the input file.
 
Line(85), the outer `for` loop, is to extract the main content which the list of devices and their properties (e.g. mount, type, options as key-pair dictionaries) to be processed later.

We have two support functions to help validate the input content (see more details below).

Only once all the validation constraints meet, the inner `for` loop (lines 88 to 116) can be run to construct the `fstab` records:

- Line(86) for NFS type: join the device name (parent key) and mount (child key) to form the network-based device identity.
- Without `options` key, the `defaults` is implicitly appended to the end of the record.


**1. validate_input(list_of_dicts)**

Line(43): check if the device is NFS type which having `export` key, so, call the `validate_address()` function to check if its name is a valid IPv4 address.

Line(58): else if the devices have another filesystems, we expect them to be block devices by calling `stat.S_ISBLK()` function.

Lines(51 and 66): require the mount points exist before mounting the devices.

Lines(49 and 64): require the mount points are unique in the `fstab` file. In other words, two or more devices have the same mount point is not accepted.

**2. validate_address(address)**

Line(11): try to separate the address into a list of multiple elements (octets) with dot (.) as the delimiter. Then check if it meets all the following requirements to be a valid IPv4 address:

- Line(13): the number of elements is equal to 4 or not.
- Line(18): the elements are integer numbers or not.
- Line(21): each element needs to be in range >=1 and <=255.


## Installation

Pulling this repository or download the file [fstab-gen.py](https://raw.githubusercontent.com/manthang/fstab-generator/main/fstab-gen.py)

## Requirements
- Tested with Python version 3.x.
- Need to install [PyYAML](https://pypi.org/project/PyYAML) package.
```python
pip install PyYAML
```

## Usage

```
python fstab-gen.py <yaml_file_path>
```

* The default output file name is `fstab` saved in the current working directory.
* The errors such as invalid syntax, if any, will be printed out to the terminal console.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache License 2.0 ](https://www.apache.org/licenses/LICENSE-2.0)
