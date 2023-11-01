# Space Telescope Product Downsampling

[![Powered by STScI Badge](https://img.shields.io/badge/powered%20by-STScI-blue.svg?colorA=707170&colorB=3e8ddd&style=flat)](http://www.stsci.edu)
[![Powered by Astropy Badge](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![build](https://github.com/spacetelescope/stpreview/actions/workflows/build.yml/badge.svg)](https://github.com/spacetelescope/stpreview/actions/workflows/build.yml)
[![test](https://github.com/spacetelescope/stpreview/actions/workflows/tests.yml/badge.svg)](https://github.com/spacetelescope/stpreview/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/spacetelescope/stpreview/graph/badge.svg?token=tSEFJ5vwgH)](https://codecov.io/gh/spacetelescope/stpreview)

```
pip install stpreview
```

### Usage

#### `stpreview by`

```
❯ stpreview by --help
Usage: stpreview by [OPTIONS] INPUT OUTPUT FACTOR... [OBSERVATORY]

  downsample the given ASDF image by the given factor

Arguments:
  INPUT          path to ASDF file with 2D image data  [required]
  OUTPUT         path to output image file  [required]
  FACTOR...      block size by which to downsample image data  [required]
  [OBSERVATORY]  observatory, one of ['roman', 'jwst']

Options:
  --compass / --no-compass  whether to draw a north arrow on the image
                            [default: no-compass]
  --help                    Show this message and exit.
```

#### `stpreview to`

```
❯ stpreview to --help
Usage: stpreview to [OPTIONS] INPUT OUTPUT SHAPE... [OBSERVATORY]

  downsample the given ASDF image to the desired shape

  the output image may be smaller than the desired shape, if no even factor
  exists

Arguments:
  INPUT          path to ASDF file with 2D image data  [required]
  OUTPUT         path to output image file  [required]
  SHAPE...       desired pixel resolution of output image  [required]
  [OBSERVATORY]  observatory, one of ['roman', 'jwst']

Options:
  --compass / --no-compass  whether to draw a north arrow on the image
                            [default: no-compass]
  --help                    Show this message and exit.
```

### Examples

##### downsample a sample Roman image by a factor of 10, and add a compass rose

```shell
stpreview by /grp/roman/TEST_DATA/23Q4_B11/aligntest/r0000501001001001001_01101_0001_WFI01_cal.asdf docs/images/by.png 10 10 --compass
```

![by](./docs/images/by.png)

##### downsample a sample Roman image to within 300x300 pixels

```shell
stpreview to /grp/roman/TEST_DATA/23Q4_B11/aligntest/r0000501001001001001_01101_0001_WFI01_cal.asdf docs/images/to.png 300 300 roman
```

![to](./docs/images/to.png)
