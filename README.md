# Lund jet plane tutorial

## Requirements

To run this tutorial you can either install the necessary dependencies, which are:
 * [fastjet](http://fastjet.fr/repo/fastjet-3.3.2.tar.gz),
 * [fjcontrib-1.038](http://fastjet.hepforge.org/contrib/downloads/fjcontrib-1.038.tar.gz)
 * the keras, tensorflow, numpy, and matplotlib python3 libraries, which
   can be installed using pip.

Once these are installed and fastjet-config is in your path, you
should be able to run everything locally.

Alternatively, you can install docker and download [this docker
image](https://cernbox.cern.ch/index.php/s/ZixPL8vd8AnMsd7), which you
can start using

```
gzip -d tutorial-docker.tar.gz
docker load --input tutorial-docker.tar
docker run -it -p 8888:8888 tutorial
```

This will open a bash session with the docker image that contains all
the required files and libraries for this tutorial. To retrieve the
figures created by the python scripts, you can use

```
docker container ls
docker container cp CONTAINER:SRC_PATH DEST_PATH
```


## Data files

You can download jet samples here:
 * [Dijet sample](https://cernbox.cern.ch/index.php/s/itYr34u84nNYfvn)
 * [W sample](https://cernbox.cern.ch/index.php/s/1fIE6illqKunptQ)


## Creating declusterings with the LundPlane contrib

Using the LundGenerator class from the LundPlane FastJet contrib,
create json files containing declusterings of an example event.

```
make example
example < single-event.dat
```

This creates a json file jets.json containing the list of
declusterings for the jets in that event.
You can plot the corresponding Lund image with:

```
python3 example.py
```


## Secondary Lund planes

Using the LundWithSecondary class, look at the secondary plane of the
jets in our example event.  The secondary plane depends on the
definition of the leading emission, which is set through the family of
SecondaryLund classes. In our example, we will select the leading
emission as the first one identified by mMDT tagging with z<sub>cut</sub> =
0.025.

```
make example_secondary
example_secondary < single-event.dat
```

Do you understand the output of this program?


## Plot lund images

After creating samples in pythia 8, or having downloaded them from the
link above, you can obtain a Lund image in pyplot using

```
python3 plot_lund.py [--sig file_signal --bkg file_background --nev nevents --npxl npixels]
```


## Tagging of W jets

You can try out a CNN Lund image tagger by using the trained model
provided.

To try out the model, you can run

```
python3 test_lund.py [--sig file_signal --bkg file_background --nev nevents --threshold threshold]
```

Where threshold is a value between 0 and 1 (0.5 by default) used for the tagging.