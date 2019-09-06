#@ File(style="open") filename

#@ OMEXMLService omeservice
#@ LogService logger
#@ Context context

# Author : Thomas Pengo <tpengo@umn.edu>
# License : GPL-3

TEMPLATE_GENERAL 		= "The data was acquired on a {ID} microscope, using a {magnification}x {NA} NA objective. The pixel size is {pxx_microns} microns. "
TEMPLATE_CHANNEL		= "The excitation wavelength for channel {ch} is {ex} and the {exposureTime} is {} milliseconds. "
TEMPLATE_3D				= "A series of slices was collected with a step size of {pzz_microns} microns. "
TEMPLATE_TIME			= "Images were acquired with a time interval of {timeInterval}. "

BLURB = ""

# Admin stuff
from org.scijava.ui.swing.console import LoggingPanel
logger.addLogListener( LoggingPanel(context) );

logger.info(filename.getAbsolutePath())

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
	logger.error("More than one instrument found. Automatic generation will not work...")
if ninstruments == 0:
	logger.error("No instrument metadata found! Automatic generation will not work...")

# Manufacturer and modalities
try:
	ID = m.getMicroscopeManufacturer(0)
except:
	ID = None
	
if ID == None:
	ff = str(ir.getFormat())
	if "Zeiss" in ff:
		ID="Zeiss"
	elif "Nikon" in ff:
		ID="Nikon"
	elif "Olympus" in ff:
		ID="Olympus"
	else:
		ID=""

for ic in range(ir.getSizeC()):
	mode = m.getChannelAcquisitionMode(0,ic)

	if ic>0 and mode != mode0:
		logger.warn("WARNING : Not all channels were acquired with the same modality..")
	else:
		mode0=mode

if mode == None:
	mode_with_spaces = "UNKNOWN"
else:
	mode_with_spaces = ""
	if str(mode) == "TIRF":
		mode_with_spaces = str(mode)
	else:
		for letter in str(mode):
			if letter.isupper():
				mode_with_spaces += " "+letter.lower()
			else:
				mode_with_spaces += letter

ID+=" "+str(mode_with_spaces.strip())

if ninstruments == 1:
	nobjectives		= m.getObjectiveCount(0)
	if nobjectives > 1:
		logger.error("More than one objective found. Automatic generation will generate information for the first objective only.")

magnification = "UNKNOWN"
if ninstruments == 1 and nobjectives >0:
	try:
		magnification1 	= m.getObjectiveNominalMagnification(0,0)

		if magnification1 != None:
			magnification = str(magnification1)
	except:
		msg = "Could not extract information about the objective! The image might be missing some crucial metadata."
		logger.error(msg)

NA = "UNKNOWN"
if ninstruments == 1 and nobjectives >0:
	try:
		NA1 = m.getObjectiveLensNA(0,0)
		
		if NA1 != None:
			NA = str(NA1)
	except:
		msg = "Could not extract information about the objective! The image might be missing some crucial metadata."
		logger.error(msg)

# Pixel size
nimages = m.getImageCount()
logger.info("Found {} images".format(nimages))

from ome.units import UNITS

pxx_microns = "UNKNOWN"
if ninstruments==1 and nobjectives>0:
	try:
		pxx_microns = "{:.2f}".format(m.getPixelsPhysicalSizeX(0).value(UNITS.MICROMETER))
	except:
		msg = "Could not extract physical pixel size! The image might be missing some crucial metadata."
		logger.error(msg)

# Is it 3D?
is3D = ir.getSizeZ()>1

pzz_microns = "UNKNOWN"

if ninstruments==1 and nobjectives>0:
	try:
		pzz_microns = "{:.2f}".format(m.getPixelsPhysicalSizeZ(0).value(UNITS.MICROMETER))
	except:
		msg = "This image is 3D but I could not extract physical step size! The image might be missing some crucial metadata."
		logger.error(msg)


# TODO Is it a time series?

# BLURB GENERATION
BLURB += TEMPLATE_GENERAL.format(ID=ID, magnification=magnification, NA=NA, pxx_microns=pxx_microns)
if is3D:
	BLURB += TEMPLATE_3D.format(pzz_microns=pzz_microns)

# TODO Extract channel information
#for ic in ir.getSizeC():
#	ex = m.getChannelExcitationWavelength(0,ic)
#	et = m.getPlaneExposureTime(0,0)

message = '''

M&M for : {}
-----------------
{}
-----------------


'''.format(filename.getAbsolutePath(),BLURB)

print message
logger.info(message)
