import re
import sys
import os
import datetime
import time
import traceback
import commands
import xml.etree.ElementTree as ET

########################### FUNCTIONS ###########################
def systemExit():
	try:
		print(RESET)
		input("\nPress enter to close the program...\n>>>")
	except SyntaxError:
		sys.exit()
	
def timeStamp():
	now = datetime.datetime.now()
	now = now.strftime("%m/%d/%Y/%I:%M:%S %p")
	return now

def checkIllegalChars(name):
	illegal_chars = ["~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "{", "}", "[", "]", "|", "\\", ";", ":", "'", "\"", ",", "<", ".", ">", "?", " "]
	nameChanged = False
	for iChar in illegal_chars:
		if iChar in name:
			name = name.replace(iChar, "_")
			nameChanged = True
		else:
			continue
	if nameChanged == True:
		print(COMPUTEROUTPUT + "Illegal characters were found in your filename so I took the liberty of fixing it for you. The new filename is: " + name + "\nYour Welcome." + RESET)
	return name

def checkStartFrame0(root):
	recordIn = root.find(".Outputs/Output/Video/Track/Shot/Record/In").text
	if recordIn != '0':
		CONTINUE = raw_input(ERROR + "The source XML does not start at frame zero. Do you wish to continue anyway? (Y/N), then press [ENTER]: "  + RESET + USERINPUT)
		print(RESET)
		if CONTINUE == "Y" or CONTINUE == "y":
			print(COMPUTEROUTPUT + "OK...continuing the program...\n" + RESET)
		else:
			systemExit()

def getBitDepth():
	while True:
		pattern = "^\d{1,2}$"
		bitDepth = raw_input(COMPUTEROUTPUT + "\nType the bit depth number you would like, then hit [ENTER]:(Ex. '10', '12', '16', etc.)\n" + RESET + USERINPUT)
		if re.findall(pattern, bitDepth):
			changeValue = raw_input(COMPUTEROUTPUT + "\nYou entered " + bitDepth + ". Would you like to change your value? (Y/N), then hit [ENTER]: " + RESET + USERINPUT)
			print(RESET)
			if changeValue == "N" or changeValue == "n":
				break
			else:
				continue
		else:
			print(COMPUTEROUTPUT+"YOU ENTERED AN INCORRECT VALUE: '"+USERINPUT+bitDepth+COMPUTEROUTPUT+"'. Please only enter a one or two digit number value...")
			continue
	return bitDepth

def checkBitDepth(root):
	sourceBitDepth = root.find(".Outputs/Output/Video/Track/ColorEncoding/BitDepth")
	if sourceBitDepth is None:
#		sourceBitDepth = root.find(".Outputs/Output/Video/Track/ColorEncoding/BitDepth").text
#	else:
		print(ERROR+"THE SOURCE XML FILE DOES NOT HAVE A BIT DEPTH TAG IN THE COLOR ENCODING SECTION"+RESET)
		CONTINUE = raw_input(COMPUTEROUTPUT+"Therefore, this script will not be able to update the value, since no value exists to update. Would you like to continue anyway? (Y/N) then press [ENTER]: "+ USERINPUT)
		if CONTINUE == "Y" or CONTINUE == "y":
			bitDepthCommand = ""
			return bitDepthCommand
		else:
			systemExit()
	print(RESET)
#	print(COMPUTEROUTPUT + "\nLocate the bit depth of the delivery file that the XML needs to reference...i.e. Disney+ delivers a Rec2020 ProRes XQ file, whose bit depth is 12bits. Therefore you would enter the value '12'.\nFor reference:\nProRes HQ is 10bit\nProRes XQ is 12bit\n")
	bitDepth = getBitDepth()
	bitDepthCommand = "u" + str(bitDepth)
	while sourceBitDepth == bitDepth:
		print(COMPUTEROUTPUT + "\nThe Bit Depth found in the source XML ("+USERINPUT+sourceBitDepth+COMPUTEROUTPUT+"), matches the Bit Depth you typed ("+USERINPUT+bitDepth+COMPUTEROUTPUT+")." + RESET)
		changeValue = raw_input(COMPUTEROUTPUT + "\nWould you like to change your value? (Y/N), then hit [ENTER]: " + RESET + USERINPUT)
		print(RESET)
		if changeValue == "Y" or changeValue == "y":
			bitDepth = getBitDepth()
			bitDepthCommand = "u" + str(bitDepth)
		else:
			print(COMPUTEROUTPUT+"XML Bit Depth will stay the same. Moving on..."+RESET)
			bitDepthCommand = "u" + str(bitDepth)
	return bitDepthCommand

def edendaleBitDepth(root):
	bitDepthCommand = ""
	sourceBitDepth = root.find(".Outputs/Output/Video/Track/ColorEncoding/BitDepth")
	if sourceBitDepth is None:
		print("\n"+ERROR+"THE SOURCE XML FILE DOES NOT HAVE A BIT DEPTH TAG IN THE COLOR ENCODING SECTION. PROGRAM CANNOT CONTINUE FURTHER UNTIL THIS IS RESOLVED."+RESET)
		systemExit()
	elif sourceBitDepth.text != "16":
		bitDepthCommand = "--color-encoding 'u16' "
	return bitDepthCommand

def edendale2TrimsCheck(root):
	notMatchingList = []
	for shot in root.findall('.Outputs/Output/Video/Track/Shot'):
		trims = shot.findall('PluginNode/DolbyEDR/TID')
		recordIn = shot.find('Record/In').text
#		print("Record In="+recordIn)
#		for item in trims:
#			print("Trims="+item.text)
		report = False
		text = "RECORD IN FRAME: " + recordIn + "---->TRIM ID'S: "
		if len(trims) == 2:
			for trim in trims:
				if trim.text != '1':
					if trim.text != '27':
						text += "ID-"+trim.text+"{VALUE NOT EXPECTED} "
						report = True
		else:
			text += "[EXACTLY TWO TRIMS NOT PRESENT. REPORTING ALL TRIMS FOR THIS SHOT]="
			report = True
			for trim in trims:
				if trim.text == '1':
					text += "ID-"+trim.text+" "
				elif trim.text == '27':
					text += "ID-"+trim.text+" "
				else:
					text += "ID-"+trim.text+"{VALUE NOT EXPECTED} "
		if report == True:
			notMatchingList.append(text)
	return notMatchingList

def validateXML(inPath):
	print("\n" + COMPUTEROUTPUT + "VALIDATING FILE: " + inPath)
	print(RESET)
	validate = "metafier --validate '" + inPath + "'"
	os.system(validate)

def validateContinue():
	CONTINUE = raw_input(COMPUTEROUTPUT + "\nDo you want to continue to convert the XML? (Y/N), then hit [ENTER]: " + RESET + USERINPUT)
	print(RESET)
	if CONTINUE == "Y" or CONTINUE == "y":
		return
	else:
		print(COMPUTEROUTPUT + "You have chosen not to continue. Program is exiting...")
		systemExit()

def getData():
	inPath = raw_input(COMPUTEROUTPUT + "\nPlease drag & drop the source XML into this window, then hit ENTER:\n" + RESET + USERINPUT)
	inPath = inPath[1:-2]
	directory = os.path.dirname(inPath)
	while True:
		print(COMPUTEROUTPUT+"Here is a list of the type of XML delivery files this script can make.\nEnter the number value of the selection you want:\n\t1) DISNEY PLUS WORKFLOW\n\t2) RAY DONOVAN HDR WORKFLOW\n\t3) APPLE PRORES WORKFLOW\n\t4) EDENDALE FOX IMF WORKFLOW\n\t5) TRIM NIT CHECK ONLY")
		XMLType = raw_input(COMPUTEROUTPUT+"Type a number, then press [ENTER]: "+USERINPUT)
		print(RESET)
		pattern = "^\d$"
		testPattern = re.findall(pattern, XMLType)
		if testPattern:
			if XMLType == "1":
				XMLworkflow = "DISNEY PLUS WORKFLOW"
				outFilePath = outXMLFile(directory)
			elif XMLType == "2":
				outFilename = raw_input(COMPUTEROUTPUT + "\nType the name of the new XML file WITHOUT the file extension, then hit ENTER:\n" + RESET + USERINPUT)
				outFilename = checkIllegalChars(outFilename)
				outFilePath = directory + os.sep + outFilename + ".xml"
				XMLworkflow = "RAY DONOVAN HDR WORKFLOW"
				outFilePath = directory + os.sep + "DoVi4-0_" + outFilename + ".xml"
			elif XMLType == "3":
				XMLworkflow = "APPLE TV EDENDALE PRORES & TIFF WORKFLOW"
				outFilePath = outXMLFile(directory)
			elif XMLType == "4":
				XMLworkflow = "EDENDALE FOX IMF WORKFLOW"
				outFilePath = outXMLFile(directory)
			elif XMLType == "5":
				XMLworkflow = "CHECK FOR 100-NIT & 600-NIT TRIM ONLY"
				outFilePath = ""
			else:
				XMLworkflow = "VALUE NOT CODED"
			return inPath, outFilePath, XMLType, XMLworkflow
		else:
			print(COMPUTEROUTPUT+"YOU DID NOT ENTER A PROPER VALUE. PLEASE TRY AGAIN."+RESET)
			continue

def outXMLFile(directory):
	outFilename = raw_input(COMPUTEROUTPUT + "\nType the name of the new XML file WITHOUT the file extension, then hit ENTER:\n" + RESET + USERINPUT)
	outFilename = checkIllegalChars(outFilename)
	outFilePath = directory + os.sep + outFilename + ".xml"
	return outFilePath


def disneyDelivery(inPath, outFilePath, root):
	validateXML(inPath)
	validateContinue()
	bitDepthCommand = checkBitDepth(root)
	checkStartFrame0(root)
	command = "metafier --color-encoding 'bthdrfull " + bitDepthCommand + "' --max-fall-cll 0 0 -o '" + outFilePath + "' '" + inPath + "'"
	os.system(command)
	validateXML(outFilePath)

def rayDonovanDelivery(inPath, outFilePath40):
	validateXML(inPath)
	validateContinue()
	command40 = "metafier --color-encoding 'bthdrfull' -o '" + outFilePath40 + "' '" + inPath + "'"
	os.system(command40)
	validateXML(outFilePath40)
	outFilePath29 = outFilePath.replace("DoVi4-0_", "DoVi2-9_")
	command29 = "metafier --save-version 2.0.5 -o '" + outFilePath29 + "' '" + outFilePath40 + "'"
	os.system(command29)
	validateXML(outFilePath29)
	
def AppleProResDelivery(inPath, outFilePath, root):
	trimList = edendale2TrimsCheck(root)
	if len(trimList) > 0:
		print("\n"+ERROR+"DISCREPENCIES FOUND IN THE TRIM VALUES. THIS NEEDS TO BE ADDRESSED. BELOW ARE THE DISCREPENCIES ALONG WITH THE FRAME NUMBER IT CAN BE FOUND AT IN THE XML. THEN THE PROGRAM WILL EXIT..."+RESET)
		for item in trimList:
			print(COMPUTEROUTPUT+item)
		BitDepth = edendaleBitDepth(root)
		systemExit()
	BitDepth=''
#	BitDepth = edendaleBitDepth(root)
#	if BitDepth != "":
#		BitDepth = "--color-encoding "+BitDepth+" "
	validateXML(inPath)
	validateContinue()
	command = "metafier "+BitDepth+"--max-fall-cll 0 0 -o '" + outFilePath + "' '" + inPath + "'"
	os.system(command)
	validateXML(outFilePath)

def edendaleFoxIMFDelivery(inPath, outFilePath, root):
	trimList = edendale2TrimsCheck(root)
	if len(trimList) > 0:
		print("\n"+ERROR+"DISCREPENCIES FOUND IN THE TRIM VALUES. THIS NEEDS TO BE ADDRESSED. BELOW ARE THE DISCREPENCIES ALONG WITH THE FRAME NUMBER IT CAN BE FOUND AT IN THE XML. THEN THE PROGRAM WILL EXIT..."+RESET)
		for item in trimList:
			print(COMPUTEROUTPUT+item)
		BitDepth = edendaleBitDepth(root)
		systemExit()
	BitDepth = edendaleBitDepth(root)
	validateXML(inPath)
	validateContinue()
	command = "metafier --color-encoding 'bthdrfull' "+BitDepth+" --max-fall-cll 0 0 -o '" + outFilePath + "' '" + inPath + "'"
	os.system(command)
	validateXML(outFilePath)

def twoTrim(inPath, outFilePath, root):
	trimList = edendale2TrimsCheck(root)
	if len(trimList) > 0:
		print("\n"+ERROR+"DISCREPENCIES FOUND IN THE TRIM VALUES. THIS NEEDS TO BE ADDRESSED. BELOW ARE THE DISCREPENCIES ALONG WITH THE FRAME NUMBER IT CAN BE FOUND AT IN THE XML. THEN THE PROGRAM WILL EXIT..."+RESET)
		for item in trimList:
			print(COMPUTEROUTPUT+item)
		BitDepth = edendaleBitDepth(root)
		systemExit()
	else:
		print(SUCCESS+"\nEVERY SHOT HAS EXACTLY 2 TRIM VALUES; THE 100-NIT & 600-NIT TRIM PASS.\n"+RESET)
		print(COMPUTEROUTPUT+"VALIDATING THE XML. STANDBY..."+RESET)
		validateXML(inPath)
		print(COMPUTEROUTPUT+"\nVALIDATION COMPLETE. PROGRAM IS EXITING\n\n"+RESET)
		systemExit()
	

########################### PROGRAM ###########################
ERROR = "\033[1;37;101m"
SUCCESS = "\033[1;92m"
RESET = "\033[0m"
USERINPUT = "\033[1;34m"
COMPUTEROUTPUT = "\033[1;37;40m"

print COMPUTEROUTPUT 
print "\t|||-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-|||"
print "\t|||                                                    			          |||"
print "\t||| METAFY 2.0 DOES VARIOUS XML CONVERSIONS PER THE THE BELOW LISTED PRESETS.     |||"
print "\t||| IF YOU NEED SOMETHING DIFFERENT, CONTACT ENGINEERING SO THEY CAN MAKE         |||"
print "\t||| ADJUSTMENTS OR CREATE NEW PRESETS. FOLLOW THE PROMPTS.			  |||"
print "\t|||                                                     			  |||"
print "\t||| PRESETS: 									  |||"
print "\t||| 1) DISNEY PLUS WORKFLOW [converts to Rec2020 and zeros MaxFALL & MaxCLL]      |||"
print "\t||| 2) RAY DONOVAN HDR WORKFLOW [Creates 2 XML's in Rec2020; as DoVi 2.9 & 4.0]   |||"
print "\t||| 3) APPLE TV EDENDALE PRORES & TIFF WORKFLOW [zeros MaxFALL & MaxCLL]          |||"
print "\t||| 	**ALSO CHECKS EACH SHOT FOR THE 100-NIT & 600-NIT TRIM PASS** 	       	  |||"
print "\t||| 	**THIS PRESET EXPECTS A DOLBY VISION 4.0 VERSION XML**    	       	  |||"
print "\t||| 4) EDENDALE FOX IMF WORKFLOW [converts to Rec2020 and zeros MaxFALL & MaxCLL] |||"
print "\t||| 	**ALSO CHECKS EACH SHOT FOR THE 100-NIT & 600-NIT TRIM PASS** 	       	  |||"
print "\t||| 5) CHECKS FOR 100-NIT & 600-NIT TRIM PASSES FOR EACH SHOT. NO CONVERSION.     |||"
print "\t|||                                                     			  |||"
print "\t|||_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_|||"
print(RESET)


while True:
	inPath, outFilePath, XMLType, XMLworkflow = getData()
	print(COMPUTEROUTPUT+"Below are the values you have input."+RESET)
	print(COMPUTEROUTPUT+"SOURCE XML:\n"+USERINPUT+inPath)
	if XMLType != "5":
		print(COMPUTEROUTPUT+"DELIVERY XML:\n"+USERINPUT+outFilePath)
		if XMLType == "2":
			outFilePath29 = outFilePath.replace("DoVi4-0_", "DoVi2-9_")
			print(COMPUTEROUTPUT+"DELIVERY XML:\n"+USERINPUT+outFilePath29)
	print(COMPUTEROUTPUT+"XML TYPE:"+USERINPUT+XMLworkflow)
	CORRECT = raw_input(COMPUTEROUTPUT+"ARE THESE CORRECT? (Y/N) THEN HIT [ENTER]: "+USERINPUT)
	print(RESET)
	if CORRECT == "Y" or CORRECT == "y":
		break
	else:
		continue

tree = ET.parse(inPath)
root = tree.getroot()
print(COMPUTEROUTPUT+"PROCEEDING WITH "+USERINPUT+XMLworkflow+RESET+".")

if XMLType == "1":
	disneyDelivery(inPath, outFilePath, root)
elif XMLType == "2":
	rayDonovanDelivery(inPath, outFilePath)
elif XMLType == "3":
	AppleProResDelivery(inPath, outFilePath, root)
elif XMLType == "4":
	edendaleFoxIMFDelivery(inPath, outFilePath, root)
elif XMLType == "5":
	twoTrim(inPath, outFilePath, root)


if os.path.isfile(outFilePath):
	print "\n\n" + SUCCESS + "File has been created successfully and can be found here:\n" + USERINPUT + outFilePath
	if XMLType == "2":
		print USERINPUT + outFilePath29
	print(RESET) + "\n\n"
else:
	print ERROR + "ERROR: File was not created.\n"  + RESET
	
systemExit()
