# ci_fstcomp

compares fst files like fstcomp with ajustable thresholds and returns a value for ci use 

## Getting started

``` sh
ci_fstcomp --c-cor-thr 0.0001 --e-max-thr 0.1 -a file1 -b file2
```
<!-- ci_fstcomp --query "nomvar in ['TT','UU','VV']" --ignore "etiket,dateo" --c-cor-thr 0.0001 --e-rel-thr 0.1 -a file1 -b file2 -->

## Requirements
<!-- - python 2.7 + -->
- make sure to load rmnlib

- U1
``` sh
. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
```

- U2
``` sh
. r.load.dot eccc/mrd/rpn/MIG/ENV/rpnpy/2.1-u2.3 eccc/mrd/rpn/MIG/ENV/migdep/5.1-u2.2 eccc/cmd/cmda/libs/20220216/inteloneapi-2022.1.2
```

## Install

``` sh
python -m pip install git+http://gitlab.science.gc.ca/CMDS/ci_fstcomp

```

### Development

We clone the repository and use the `-e` option when `pip`-intalling. This way
pip installs a link to our repository so that changes to the code take effect
without the need for reinstalling.

We also use the `-v` option to see where things are placed by `pip`.  In this
case, we want to look at where the `ci_fstcomp` script is put and make sure that
this directory is in our `PATH`.

``` sh
git clone git@gitlab.science.gc.ca:CMDS/ci_fstcomp.git
```

<!-- #### With python2

``` sh
python2 -m pip install -ve ./ci_fstcomp
```

    [...]
    Creating /fs/homeu1/eccc/cmd/cmds/phc001/.local/lib/python2.7/site-packages/ci_fstcomp.egg-link (link to .)
    Adding ci_fstcomp 1.0.0 to easy-install.pth file
    Installing ci_fstcomp script to /home/phc001/.local/bin
    [...] -->

#### With python3

``` sh
python3 -m pip install -ve ./ci_fstcomp
```

    [...]
    Creating /fs/homeu1/eccc/cmd/ords/cmds/phc001/miniconda3/lib/python3.8/site-packages/ci_fstcomp.egg-link (link to .)
    Adding ci_fstcomp 1.0.0 to easy-install.pth file
    Installing ci_fstcomp script to /home/phc001/miniconda3/bin
    [...]
