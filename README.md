These are (semi)automatic processing / analysis scripts for the CP project.

Two stages:
    
-cp_do_autoproc attempts to process the data using Nexus
-cp_do_analysis attempts to extract numerical data into an Excel sheet


Workflow:

-move data to fast local disk
-edit cp_common, specify rootdir containing data
-edit cp_do_autoproc to specify subjects to process
-run cp_do_autoproc (may take a day)
-check results (how?)
-edit cp_do_analysis, specify filenames etc.
-run cp_do_analysis
-take xls file and run






