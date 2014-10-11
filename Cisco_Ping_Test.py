# $language = "python"
# $interface = "1.0"

# CiscoPingTests.py
#
# Version 1.0
# This script is built to take a given IPv4 address and run ping pattern tests.
# It will prompt the user for the IP address to ping as well as the interface to
# send pings from.
# Once the user supplies  input, it will run a 1000 count, 1500 byte ping with data pattern 0x0000.
#

def Main():

	if crt.Session.Connected == False:
		acknowledge = crt.Dialog.MessageBox("Session must be connected for this script to operate properly", "Session Not Connected", ICON_WARN | BUTTON_OK)
		if acknowledge == IDOK:
				return
	
	# Enable synchronous mode to avoid missed output while doing
	# Send/WaitForString sequences
	crt.Screen.Synchronous = True
	
	# Prompt user for IP address and interface ID
	iptarget = crt.Dialog.Prompt("Enter IP address to test:  ", "IP Address", "", False)
	# If user enters a blank IP address, terminate the script
	if iptarget == "": return
	inttarget = crt.Dialog.Prompt("Enter interface to test from, using the full interface name without spaces (E.G. Serial0/1):  ", "Interface Name", "", False)
	
	#Pattern testing
	crt.Screen.Send("ping" + chr(13))
	crt.Screen.WaitForString("Protocol [ip]: ")
	crt.Screen.Send(chr(13))
	crt.Screen.WaitForString("Target IP address: ")
	crt.Screen.Send(iptarget + chr(13))
	# Error handling for a bad IP address.
	iperror = crt.Screen.WaitForStrings(["Repeat count [5]: ", "% Bad IP address"], 10)
	if (iperror == 2):
		crt.Dialog.MessageBox("Bad IP Address!")
		return
	if (iperror == 0):
		crt.Dialog.MessageBox("Timed Out!")
		return
	crt.Screen.Send("6" + chr(13))
	crt.Screen.WaitForString("Datagram size [100]: ")
	crt.Screen.Send("1500" + chr(13))
	crt.Screen.WaitForString("Timeout in seconds [2]: ")
	crt.Screen.Send("1" + chr(13))
	crt.Screen.WaitForString("Extended commands [n]: ")
	crt.Screen.Send("y" + chr(13))
	crt.Screen.WaitForString("Source address or interface: ")	
	crt.Screen.Send(inttarget + chr(13))
	# Error handling for bad interface names. Ping will not allow for a break command at this point, so we must send the rest of the commands and not specify an interface.
	interror = crt.Screen.WaitForStrings(["Type of service [0]: ", "% Invalid source. Must use same-VRF IP address or full interface name without spaces (e.g. Serial0/1)"], 10)
	if (interror == 2):
		crt.Dialog.MessageBox("Invalid source interface.  Must use same-VRF IP address or full interface name without spaces (e.g. Serial0/1).")
		crt.Screen.Send(chr(13))
		crt.Screen.Send(chr(13))
	if (interror == 0):
		crt.Dialog.MessageBox("Timed Out!")
		return
		crt.Screen.Send(chr(13))
	crt.Screen.WaitForString("Set DF bit in IP header? [no]: ")
	crt.Screen.Send(chr(13))
	crt.Screen.WaitForString("Validate reply data? [no]: ")
	crt.Screen.Send(chr(13))
	crt.Screen.WaitForString("Data pattern [0xABCD]: ")
	crt.Screen.Send("0x0000" + chr(13))
	crt.Screen.WaitForString("Loose, Strict, Record, Timestamp, Verbose[none]: ")
	crt.Screen.Send(chr(13))
	crt.Screen.WaitForString("Sweep range of sizes [n]: ")
	crt.Screen.Send(chr(13))
	
	#Turn Synchronous mode off once script is complete.
	crt.Screen.Synchronous = False
	
Main()
