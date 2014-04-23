rkillr router rebooter
==============

Currently a pet thinger for my home router. 
Sometimes my router acts up and to set it straight it requires a reboot. 
This script checks for connectivity and reboots the router. It also notifies when the reboot is done (and times it!).

To run, install the following python packages:
`beatifulsoup4
requests`

you should also have a text file 'creds.txt' that has your user+pass for the router in json formatting, like so:

`{
	"user" : "Admin",
	"pass" : "pook"
}`