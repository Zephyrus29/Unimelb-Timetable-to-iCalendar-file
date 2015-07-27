# Unimelb-Timetable-to-iCalendar-file

Converts your University of Melbourne timetable to an iCalendar file that can be imported into most calendar applications.

To use it, go to the timetable page on the student portal, press the expand all button and copy and paste the page into a file. (by copy and paste I mean use ctrl+a on the rendered page, not save the source). Then tell the program the location of that file and an output file name and it will make an iCal file in the same directory as the program. This can then be imported into your chosen calendar program such as Google Calendar.

Very simple program and should work for 2015 S2 by default. For other semesters, the semester start and end dates will need to be changed. These are hard coded in.

Known issues: Does not work if the subject has two words in the class type, such as a clinical placement. 
              Assumes subject runs for the whole semester.

To do: Make a GUI.
       Auto update semester times.
