#@ File(style="open") filename

#@ OMEXMLService omeservice
#@ LogService logger
#@ Context context

#@OUTPUT BLURB

# Author : Thomas Pengo <tpengo@umn.edu>
# License : GPL-3

BLURB = ""

def process(filename):
	TEMPLATE_GENERAL 		= "The data was acquired on a {ID} microscope, using a {objective} {NA} NA objective. The pixel size was {pxx_microns} microns. "
	TEMPLATE_CHANNEL		= "The excitation and emission wavelengths for channel {ch} were {ex} and {em} and the {exposureTime} was {et}. "
	TEMPLATE_3D				= "A series of slices was collected with a step size of {pzz_microns} microns. "
	TEMPLATE_TIME			= "Images were acquired with a time interval of {timeInterval}. "
	
	BLURB = ""
	
	# Admin stuff
	import sys
	
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
		logger.error(sys.exc_info()[0])
		ID = None
		
	if ID == None:
		ff = str(ir.getFormat())
		if "Zeiss" in ff:
			ID="Zeiss"
		elif "Nikon" in ff:
			ID="Nikon"
	
			tID = ir.getMetadataValue("m_sMicroscopePhysFullName")
			if tID is not None:
				ID = tID
				
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
	
	objective = "UNKNOWN"
	if ninstruments == 1 and nobjectives >0:
		try:
			magnification1 	= m.getObjectiveNominalMagnification(0,0)
	
			if magnification1 != None:
				objective = "{:.0f}x".format(magnification1)
		except:
			logger.error(sys.exc_info()[0])
			msg = "Could not extract information about the objective! The image might be missing some crucial metadata."
			logger.error(msg)
	
	if objective == "UNKNOWN":
		if "Nikon" in ff:
			objective0 = str(ir.getMetadataValue("sObjective"))
			if objective0 is not None:
				objective = objective0
			
	
	NA = "UNKNOWN"
	if ninstruments == 1 and nobjectives >0:
		try:
			NA1 = m.getObjectiveLensNA(0,0)
			
			if NA1 != None:
				NA = str(NA1)
		except:
			msg = "Could not extract information about the objective! The image might be missing some crucial metadata."
			logger.error(msg)
				
	NAm = ir.getMetadataValue("Numerical Aperture")
	if NA=="UNKNOWN" and "Nikon" in ff and NAm is not None:
		NA = str(NAm)
	#else:
	#	HT=ir.getGlobalMetadata()
	#	for k in HT.keys():
	#		print "{}={}".format(k,HT.get(k))
	
	# Pixel size
	nimages = m.getImageCount()
	logger.info("Found {} images".format(nimages))
	
	from ome.units import UNITS
	
	pxx_microns = "UNKNOWN"
	if ninstruments==1 and nobjectives>0:
		try:
			pxx_microns = "{:.2f}".format(m.getPixelsPhysicalSizeX(0).value(UNITS.MICROMETER))
		except:
			logger.error(sys.exc_info()[0])
			msg = "Could not extract physical pixel size! The image might be missing some crucial metadata."
			logger.error(msg)
	
	# Is it 3D?
	is3D = ir.getSizeZ()>1
	
	pzz_microns = "UNKNOWN"
	
	if ninstruments==1 and nobjectives>0:
		try:
			pzz_microns = "{:.2f}".format(m.getPixelsPhysicalSizeZ(0).value(UNITS.MICROMETER))
		except:
			logger.error(sys.exc_info()[0])
			msg = "This image is 3D but I could not extract physical step size! The image might be missing some crucial metadata."
			logger.error(msg)
	
	
	
	# TODO Is it a time series?
	
	# GENERAL BLURB GENERATION
	BLURB += TEMPLATE_GENERAL.format(ID=ID, objective=objective, NA=NA, pxx_microns=pxx_microns)
	if is3D:
		BLURB += TEMPLATE_3D.format(pzz_microns=pzz_microns)
	
	# Extract channel information
	for ic in range(ir.getSizeC()):
		try:
			ex0 = m.getChannelExcitationWavelength(0,ic)
			
			if ex0==None:
				ex = "UNKNOWN"
			else:
				ex="{:.0f} nm".format(ex0.value(UNITS.NANOMETER))
		except:
			logger.error(sys.exc_info()[0])
			logger.error("Wasn't able to extract channel wavelength information for channel {}.".format(ic+1))
			continue
	
		try:
			em0 = m.getChannelEmissionWavelength(0,ic)
			
			if em0==None:
				em = "UNKNOWN"
			else:
				em="{:.0f} nm".format(em0.value(UNITS.NANOMETER))
		except:
			logger.error(sys.exc_info()[0])
			logger.error("Wasn't able to extract channel wavelength information for channel {}.".format(ic+1))
			continue
	
		#try:
		ix = ir.getIndex(0, ic, 0)		# NOTE : First z plane, first timepoint only
		et = m.getPlaneExposureTime(0,ix)
	
		if et==None:
			et = "UNKNOWN"
		else:
			etms = et.value(UNITS.MILLISECOND)

			if "CZI" in ff: # TODO Check if error is across other images
				logger.warn("The exposure time was divided by 1000 to account for ms mistaken as s in CZI files")
				
				etms = etms/1000
				
			if etms<1000:
				et=str("{:.2f} ms".format(etms))
			else:
				et=str("{} s".format(etms/1000))
	
				if etms/1000>600:
					logger.warn("Exposure time for channel {} is {}s. That's longer than 10m, please double check metadata to make sure it's correct".format(ic+1,etms/1000))
	
		BLURB += TEMPLATE_CHANNEL.format(ch=ic+1, ex=ex, exposureTime="exposure time", et=et, em=em)		
		#except:
		#	logger.error("Wasn't able to extract channel {} exposure time information.".format(ic+1))

	return BLURB

BLURB = process(filename)

message = '''

M&M for : {}
-----------------
{}
-----------------


'''.format(filename.getAbsolutePath(),BLURB)

print message
logger.info(message)

# REFERENCE
# https://downloads.openmicroscopy.org/bio-formats/5.1.0/api/ome/xml/meta/MetadataRetrieve.html
