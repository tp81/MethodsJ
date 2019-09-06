#@ File(style="open") filename
#@ OMEXMLService omeservice

# Author : Thomas Pengo <tpengo@umn.edu>
# License : GPL-3

TEMPLATE_GENERAL 		= "The data was acquired on a {ID} microscope, using a {magnification}x {NA} NA objective. The pixel size is {pxx_microns:.2f} microns. "
TEMPLATE_CHANNEL		= "The excitation wavelength for channel {ch} is {ex} and the {exposureTime} is {} milliseconds. "
TEMPLATE_3D				= "The step size is {pzz_microns:.2f} microns. "
TEMPLATE_TIME			= "Images were acquired with a time interval of {timeInterval}. "

BLURB = ""

# Get a BioFormats reader
from loci.formats import ImageReader
ir = ImageReader()

# Adapted from https://github.com/ome/bioformats/blob/develop/components/formats-gpl/utils/GetPhysicalMetadata.java
m = omeservice.createOMEXMLMetadata()

ir.setMetadataStore(m)
ir.setId(filename.getAbsolutePath())

# Some checks
ninstruments 	= m.getInstrumentCount()
if ninstruments > 1:
	error("More than one instrument found. Automatic generation will not work...")
nobjectives		= m.getObjectiveCount(0)
if nobjectives > 1:
	error("More than one objective found. Automatic generation will not work...")

# TODO ADD MODALITY
ID		 		= m.getMicroscopeManufacturer(0)
if ID == None:
	ff = str(ir.getFormat())
	if "Zeiss" in ff:
		ID="Zeiss"
	elif "Nikon" in ff:
		ID="Nikon"
	elif "Olympus" in ff:
		ID="Olympus"
		
magnification 	= str(m.getObjectiveNominalMagnification(0,0))
NA 				= str(m.getObjectiveLensNA(0,0))

# Pixel size
nimages = m.getImageCount()
print "Found {} images".format(nimages)

from ome.units import UNITS
pxx_microns = m.getPixelsPhysicalSizeX(0).value(UNITS.MICROMETER)

# Is it 3D?
is3D = ir.getSizeZ()>1
pzz_microns = m.getPixelsPhysicalSizeZ(0).value(UNITS.MICROMETER)

# TODO Is it a time series?

# BLURB GENERATION
BLURB += TEMPLATE_GENERAL.format(ID=ID, magnification=magnification, NA=NA, pxx_microns=pxx_microns)
if is3D:
	BLURB += TEMPLATE_3D.format(pzz_microns=pzz_microns)

# TODO Extract channel information
#for ic in ir.getSizeC():
#	ex = m.getChannelExcitationWavelength(0,ic)
#	et = m.getPlaneExposureTime(0,0)
	
print "\n\n\n-----------------"
print BLURB
print "-----------------\n\n\n"
