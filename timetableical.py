import re;
import random,string;
import time;

def dayoffset(day):
	offset={
		'MO': 0,
		'TU': 1,
		'WE': 2,
		'TH': 3,
		'FR': 4,
		'SA': 5,
		'SU': 6
		}[day]
	return offset;
	
def idgen(size):
	out=""
	for x in range(0,size):
		out=out+random.SystemRandom().choice(string.ascii_uppercase + string.digits)
	return out;
	
inputfilename=raw_input("Enter the input file name: ")
outfilename=raw_input("Enter the output file name: ") +".ics"
semesterstartdate="201602"
semesterenddate="20160531T220000Z"
semesterstartday=22
classtypes=['Workshop','Lecture','Tutorial','Seminar','Practical','Bump-in','Bump-out','Problem-based','Filmmaking','Performance','Rehearsal','Screening','Studio']
input =open (inputfilename, "r")
var = input.readline()
subject = input.readline().rstrip()
#below is a bunch of information for ical, like timezones and daylight saving
output= "BEGIN:VCALENDAR\nPRODID:-//zephyrus//unitime v1.2//EN\nVERSION:2.0\nMETHOD:PUBLISH\nX-X-WR-CALDESC:University Timetable\nX-LIC-LOCATION:Australia/Sydney\nTZOFFSETFROM:+1100\nDTSTART:19700405T030000\nBEGIN:DAYLIGHT\nTZOFFSETFROM:+1000\nTZOFFSETTO:+1100\nTZNAME:AEDT\nDTSTART:19701004T020000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=1SU\nEND:DAYLIGHT\nBEGIN:VTIMEZONE\nTZID:Australia/Melbourne\nX-LIC-LOCATION:Australia/Melbourne\nBEGIN:DAYLIGHT\nTZOFFSETFROM:+1000\nTZOFFSETTO:+1100\nTZNAME:AEDT\nDTSTART:19701004T020000\nRRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=1SU\nEND:DAYLIGHT\nBEGIN:STANDARD\nTZOFFSETFROM:+1100\nTZOFFSETTO:+1000\nTZNAME:AEST\nDTSTART:19700405T030000\nRRULE:FREQ=YEARLY;BYMONTH=4;BYDAY=1SU\nEND:STANDARD\nEND:VTIMEZONE"
while var:
	if var=='Collapse\n': #uses the word collapse to separate subjects
		var = input.readline()
		subject = input.readline().rstrip()
	var=input.readline()
	for x in range(0,len(classtypes)): #checks if this tells you what the class type is
		if re.match(classtypes[x],var):
			var=var.split(" ",3) #This splitting is needed for the case of streamed subjects
			lesson=" ".join(var[0:1]).rstrip()
			if len(var)>=3:
				var=" ".join(var[2:len(var)])
			else:
				var=" ".join(var) #If this doesn't occur, then there's a crash on the next cycle through the classtypes
	if re.match("Registered Class \d Time: ",var):
		event="\nBEGIN:VEVENT"
		match=re.split("  ",var);
		event=event+"\nSUMMARY:"+subject+" "+lesson
		match[1]=re.findall("[\w']+",match[1])
		# Changes the date to the needed upper case and front two characters
		day=match[1][0][0:2].upper()
		# adjusts to the needed 24 hour time
		if match[1][3] == 'pm':
			if(int(match[1][1]))!=12:
				match[1][1]=int(match[1][1])+12;
		if match[1][6] == 'pm':
			if(int(match[1][4]))!=12:
				match[1][4]=int(match[1][4])+12;
		event=event+"\nDTSTART;TZID=Australia/Melbourne:" + semesterstartdate +str(semesterstartday+dayoffset(day))+ "T" + str(match[1][1]).zfill(2) +str(match[1][2]).zfill(2)+"00Z"
		duration=(int(match[1][4])*60+int(match[1][5]))-(int(match[1][1])*60+int(match[1][2]))
		event=event+"\nDTEND;TZID=Australia/Melbourne:" + semesterstartdate + str(semesterstartday+dayoffset(day)) + "T" + str(int(match[1][1])+duration/60).zfill(2)+str(int(match[1][2])+duration%60).zfill(2)+"00Z"
		event=event+"\nRRULE:FREQ=WEEKLY;BYDAY=" + day +";UNTIL=" + semesterenddate
		event=event+"\nDTSTAMP:"+time.strftime("%Y%m%dT%H%M%SZ")
		event=event+"\nCREATED:"+time.strftime("%Y%m%dT%H%M%SZ")
		event=event+"\nLAST-MODIFIED:"+time.strftime("%Y%m%dT%H%M%SZ")
		event=event+"\nLOCATION:"+match[3].rstrip("\n")
		event=event+"\nUID:" + idgen(64)
		event=event+"\nSEQUENCE:0\nSTATUS:CONFIRMED\nTRANSP:OPAQUE"
		event=event+"\nEND:VEVENT"
		output=output+ event
output=output+ "\nEND:VCALENDAR"
target=open(outfilename,'w')
target.write(output)
