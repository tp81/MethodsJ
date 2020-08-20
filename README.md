# MethodsJ
MethodsJ helps to write the material and methods section of a scientific article, by automatically generating a description of the imaging parameters.

MethodsJ works by inspecting the metadata of an image acquired on a scientific microscope and generates some boilerplate text you can use in the paper. Make sure you double-check the text to make sure it is accurate. Note that for best accuracy, you need to point it to a file in the original microscope manufacturer's format, or one of the open OME file formats (OME-TIFF, OME-XML, ...).

**DISCLAIMER** : Just in case. This is not meant to be applied blindly, but rather to be used as a starting point. Metadata is recorded by the microscope driving software, so at best it reflects the way the microscope's software was configured. In addition, this script uses the fantastic BioFormats library. It has been designed to extract as much information as possible from the image data, but formats are changing constantly so don't be surprised if the text doesn't completely reflect what you expect. If you do find some discrepancy, check with your facility staff (if the microscope is part of an imaging facility) for help on the appropriate wording or to check the configuration, and then with the BioFormats community to see if the metadata was not read correctly. If you believe there is an error in the script (not unlikely), feel free to reach out (see Feedback section below).

## How to use it
You need to install Fiji first, download it from [fiji.sc/download](https://fiji.sc/download) and install it. Then, open Fiji and drag the script (download the [latest version](https://github.com/tp81/mm_helper/releases/latest/download/mm_blurb_generator.py) from the Release page) onto the status menu. The script editor will appear. Press 'Run'. It will ask you for a file to examine. Select your image of interest and press 'Open'. The script will inspect the file and generate some text in the "output" section of the script. It will look something like this:

```
-----------------
The data was acquired on a Zeiss TIRF microscope, using a 100x 1.46 NA objective. The 
pixel size was 0.16 microns. The excitation and emission wavelengths for channel 1 
were 587 nm and 610 nm and the exposure time was 30.0 ms. 
-----------------
```

## Motivation
The motivation for this work comes from a survey conducted at the [University of Minnesota Imaging Centers](http://uic.umn.edu) on published scientific articles that relied on imaging as a key component of their findings. The survey discovered that an extraordinary proportion of scientific publications lacked the necessary information in the material and methods to be able to reproduce the imaging experiment, despite the guidelines from the publisher. Please refer to our manuscript on [eLife](https://elifesciences.org/articles/55133).

## Feedback
Feel free to send feedback to tpengo@umn.edu, or open an issue. For more information about the survey, contact marques@umn.edu and msanders@umn.edu.

## Author information
[Thomas Pengo](mailto:tpengo@umn.edu), [University of Minnesota Informatics Institute](https://research.umn.edu/units/umii)

