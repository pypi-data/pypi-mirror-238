# GTNash guides:
- [Developper's guide](https://game-theory-tools-group.pages.mia.inra.fr/gtnash/main)
- User's guide: See Jupyter notebooks below.

# How to use GTNash 

## Using GTNash with [SageMath](https://www.sagemath.org/)

To be able to use GTNash with Jupyter notebook, the package must be installed in sage python.

While the file setup.py is present at the root, open a terminal in the root of the repertory a execute the following command:

```
sage -pip install -e .
```

Or if you need to use relative path:

```
"path_to_sage"/sage -pip install -e "path to repository"/gtnash/
```

If executed properly, you should be able to have the following output when using sage: 

```
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 9.4, Release Date: 2021-08-22                     │
│ Using Python 3.9.5. Type "help()" for help.                        │
└────────────────────────────────────────────────────────────────────┘
sage: import gtnash                                                             
sage: gtnash                                                                    
<module 'gtnash' from '"Path to the repository"/gtnash/gtnash/__init__.py'>
```

Another possibility, if you are using Sagemath in Jupyter, is to open a Python 3 notebook (in the gtnash/ directory) and execute a cell containing the command:
```
pip install -e .
```

## 3 ways to use Jupyter instance hosting notebooks on the GTNash library.

### The Binder way

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fforgemia.inra.fr%2Fgame-theory-tools-group%2Fgtnash/HEAD)


This repository is hosting a Dockerfile enabling binder to expose the GTNash project Notebooks.

More information on [Binder](https://mybinder.readthedocs.io/en/latest/#)

By clicking on the icon on top, you should acces to a jupyter instance hosting the notebooks.

### The SIWAA way

[SIWAA](https://siwaa.toulouse.inrae.fr/) is a web site hosting interactive tools and applications.

A direct access to the jupyter launcher --> https://siwaa.toulouse.inrae.fr/root?tool_id=interactive_nash_eq_wilson 

### Launching a Jupyter notebook on your own computer (Linux)

This is another way to use the notebooks by launching a jupyter instance on your localhost.

Copy/Paste the command line on a teminal.
```
docker run -p 8888:8888 registry.forgemia.inra.fr/game-theory-tools-group/nash-eq-wilson-to-binder/nash-eq-wilson
```
and click this link http://0.0.0.0:8888/

**To manage the container**:

* `docker container list` : to list the containers running and get the ids
* `docker stop [idOfTheContainer]` : to stop the container
* `docker pull registry.forgemia.inra.fr/game-theory-tools-group/nash-eq-wilson-to-binder/nash-eq-wilson` : to update the local image of the container.

**To install docker**:

A straightforward and simple tuto dedicated to the 20.04 of Ubuntu : [Comment installer Docker sur Ubuntu 20.04 LTS Focal Fossa
](https://linuxconfig-org.translate.goog/how-to-install-docker-on-ubuntu-20-04-lts-focal-fossa?_x_tr_sl=en&_x_tr_tl=fr&_x_tr_hl=fr&_x_tr_pto=nui,sc)

**To update the image of the container** hosted on the [registry](https://forgemia.inra.fr/game-theory-tools-group/nash-eq-wilson-to-binder/container_registry) of this repository

Follow the link:

https://forgemia.inra.fr/game-theory-tools-group/nash-eq-wilson-to-binder/-/pipelines/new





