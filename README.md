# M&M Helper
Helps to write the material and methods section of a scientific article, by automatically generating a description of the imaging parameters.

This little script will help you write the materials and methods section of your scientific article. It works by inspecting the metadata of an image acquired on a scientific microscope and generates some boilerplate text you can use in the paper. Make sure you double-check the text to make sure it is accurate. Note that for best accuracy, you need to point it to a file in the original microscope manufacturer's format, or one of the open OME file formats (OME-TIFF, OME-XML, ...).

DISCLAIMER : Just in case. This is not meant to be applied blindly, but rather to be used as a starting point. Metadata is recorded by the microscope driving software, so at best it reflects the way the microscope's software was configured. In addition, this script uses the fantastic BioFormats library. It has been designed to extract as much information as possible from the image data, but formats are changing constantly so don't be surprised if the text doesn't completely reflect what you expect. If you do find some discrepancy, check with your facility staff (if the microscope is part of an imaging facility) for help on the appropriate wording or to check the configuration, and then with the BioFormats community to see if the metadata was not read correctly. If you believe there is an error in the script (not unlikely), feel free to reach out (see Feedback section below).

## How to use it
You need to install Fiji first, download it from fiji.sc/download and install it. Then, open Fiji and drag the script (download the latest version from the Release page) onto the status menu. The script editor will appear. Press 'Run'. It will ask you for a file to examine. Select your image of interest and press 'Open'. The script will inspect the file and generate some text in the "output" section of the script. It will look something like this:

```
-----------------
The data was acquired on a Zeiss microscope, using a 63.0x 1.4 NA objective. The 
pixel size is 0.21 microns. The step size is 0.24 microns. 
-----------------
```

## Feedback
Feel free to send feedback to tpengo@umn.edu, or open an issue.
