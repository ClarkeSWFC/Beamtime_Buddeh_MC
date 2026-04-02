 ,ggg, ,ggg,_,ggg,                                                                             
dP""Y8dP""Y88P""Y8b        ,dPYb,                                                              
Yb, `88'  `88'  `88        IP'`Yb                                                              
 `"  88    88    88   gg   I8  8I                                                              
     88    88    88   ""   I8  8bgg,                                                           
     88    88    88   gg   I8 dP" "8   ,ggg,     ,g,                                           
     88    88    88   88   I8d8bggP"  i8" "8i   ,8'8,                                          
     88    88    88   88   I8P' "Yb,  I8, ,8I  ,8'  Yb                                         
     88    88    Y8,_,88,_,d8    `Yb, `YbadP' ,8'_   8)                                        
     88    88    `Y88P""Y888P      Y8888P"Y888P' "YY8P8P                                       
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
 ,ggggggggggg,                                                                                 
dP"""88""""""Y8,                                         I8                                    
Yb,  88      `8b                                         I8                                    
 `"  88      ,8P                                      88888888 gg                              
     88aaaad8P"                                          I8    ""                              
     88""""Y8ba  ,ggg,     ,gggg,gg   ,ggg,,ggg,,ggg,    I8    gg    ,ggg,,ggg,,ggg,    ,ggg,  
     88      `8bi8" "8i   dP"  "Y8I  ,8" "8P" "8P" "8,   I8    88   ,8" "8P" "8P" "8,  i8" "8i 
     88      ,8PI8, ,8I  i8'    ,8I  I8   8I   8I   8I  ,I8,   88   I8   8I   8I   8I  I8, ,8I 
     88_____,d8'`YbadP' ,d8,   ,d8b,,dP   8I   8I   Yb,,d88b,_,88,_,dP   8I   8I   Yb, `YbadP' 
    88888888P" 888P"Y888P"Y8888P"`Y88P'   8I   8I   `Y88P""Y88P""Y88P'   8I   8I   `Y8888P"Y888
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
                                                                                               
 ,ggggggggggg,                                                                                 
dP"""88""""""Y8,                     8I          8I           ,dPYb,                           
Yb,  88      `8b                     8I          8I           IP'`Yb                           
 `"  88      ,8P                     8I          8I           I8  8I                           
     88aaaad8P"                      8I          8I           I8  8'                           
     88""""Y8ba  gg      gg    ,gggg,8I    ,gggg,8I   ,ggg,   I8 dPgg,                         
     88      `8b I8      8I   dP"  "Y8I   dP"  "Y8I  i8" "8i  I8dP" "8I                        
     88      ,8P I8,    ,8I  i8'    ,8I  i8'    ,8I  I8, ,8I  I8P    I8                        
     88_____,d8',d8b,  ,d8b,,d8,   ,d8b,,d8,   ,d8b, `YbadP' ,d8     I8,                       
    88888888P"  8P'"Y88P"`Y8P"Y8888P"`Y8P"Y8888P"`Y8888P"Y88888P     `Y8                
 
---Installation---

1.extract zip/download all from gihub into wherever
2.ensure your python has all modules installed (they are listed at the top of the various python files)
3.run main.py
4.PROFIT

Compatible Beamlines:
DIAMOND
i09 - Labbook and Spectra (backwards compatibility assured)
b07 - Labbook and Spectra
i06-2 - Labbook - no spectra are measured here
MAX IV
FLEXPES - Labbook and Spectra

~~~~~Loading and Handling Data~~~~~~
What do the buttons do?

---Select Input Folder---
This will open windows explorer and allow you to pick the directory with your data in. It should be the location with the .nxs files for DIAMOND or the .txt and .h5 files for MAX IV. Once a folder has been selected, the program will detect which beamline you are on. If you 
are getting an error saying "Beamline: Unsupported/Unknown" it means the program cannot identify the beamline. It does this by either looking at the start of the filenames of .nxs files (DIAMOND) or looking in the .txt files for "Location=" at MAX IV. You can quite easily add new beamlines by looking for some other indicator, but of course each new beamline will need new code writing for converting the data and generating the labbook.

---Select Output Folder---
This is where the program will output any produced files. It will produce a labbook into this directory, and will produce a new folder in this directory called "spectra as .txt files" for the converted spectra.

---Convert Spectra Data to .txt---
This program can turn all XPS and NEXAFS data in .nxs/h5 files into two column xy .txt files for easy processing. These can then be loaded into the program and analysed quickly, or you can load them in your own preferred manner. I find it is always useful to convert spectra into a simple xy format.

---Create labbook---
This program is also capable of generating an excel sheet labbook from the metadata available in various .nxs and gdaterminal.log at DIAMOND and .txt and .h5 files of flexpes. There is further documentation available on editing this code for your needs on the Duncan Group Unified Labbook but otherwise it should be fairly self explanatory.

---Select Spectra .txt Folder---
To load these .txt files into the program, press the select spectra folder button and navigate to the appropriate folder. It should load all the files in this folder. Once more spectra have been generated, simply run the conversion again and load the files again, they should be added to the list without duplicating.

---Spectra Search---
You can search the spectra for specific keywords/filenumbers. Bare in mind the search function does not scroll back up to the top of the list of spectra when you search, so if nothing comes up remember you have to go back up to the top.

---Deselect All-- 
Deselects all selected spectra, obviously.

---Clear All Spectra---
Will remove all loaded spectra from the program, so you have to load the spectra.txt files back in again.

--Spectrum Plotting and Processing--
To plot a spectra, click the tickbox next to it in the drop down menu which appears after loading the .txt files. The program SHOULD detect whether the x axis is kinetic or binding energy - don't plot kinetic and binding energy spectra on the same axis - it'll do it but it won't make any damn sense you IMBECILE. Up to 15 spectra can be loaded at once. Once a spectrum is selected, there are a few things you can do to it:
1. You can perform a crude normalisation the spectrum by ticking the norm box next to where the spectrum appears listed in the top right of the screen. 
2. You can apply a shift in x or y, for example to perform a binding energy calibration or shift raw spectra up or down to overlay them when the intensity is different.
3. Spectra of the same x dimensions can be summed using the sum selected spectra button. Spectra can be summed in batches as summed spectra will be added to the list of spectra to the left. If you need to sum more than 15, you can do them in batches of 15 onto - just sum 15 spectra, then sum that summed spectra with the next 14.
4. The fermi finder button will plot a labelled line showing the centre of a fermi edge. This presumes the data is a step function so is basically useless for non-fermi data.
5. The save figure button allows you to save a figure as a png or an svg. If you want a jpg screenshot it.
6. NEXAFS data has already been divided by i0 (I think).
7. I have tried to stop the program from picking up XSW and RESPES but if they pop up anyway just ignore them as they are not meaningful.


~~~Disclaimer~~~

This program is supposed to be a quick and dirty XPS/NEXAFS processor for fast comparisons of spectra while on a beamtime. If you want to process the data properly, or fit peaks and backgrounds, use another program like CASA. However, the .nxs processing that this program does will also be useful for those programs as well, as conversion to a .xy file is compatible with more or less every XPS program. If you want to do meaningful XSW analysis, this is not the program for you.

scroll down for 2pac

⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡟⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⠷⢶⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣤⡀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣍⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⠁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢩⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⠏⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣴⠏⠀⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢃⡾⢳⠀⠀⣽⡂⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⢫⣭⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣴⠏⠄⠇⠀⠰⢻⡇⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢤⣄⡿⣸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⣿⠆⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣴⠟⠁⡌⠰⠀⠀⠇⠘⣷⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣡⡄⣽⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⣸⣖⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣡⡴⠋⠁⠀⢠⠀⠃⠀⡰⠀⠀⢹⡆⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣰⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⢠⢯⢻⣆⢀⠻⢿⣿⣿⣿⣿⠿⠟⠋⣁⣴⠾⡏⢀⡤⡖⣒⣞⣹⠖⣦⡁⠀⠀⣾⣿⡄⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣡⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣀⣀⣀⣎⠏⣸⣿⣿⣄⣄⢨⠉⢩⣀⣠⣴⣾⣿⠇⠠⢱⢻⣠⣿⣹⣽⡙⢷⣄⢹⡄⢰⣿⡟⢻⣖⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢟⣡⡾⢋⣔⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡓⠻⣦⡘⡟⢠⣿⠟⠛⠛⠿⣿⣿⣿⣿⣿⣉⢻⡟⠀⡆⢸⠒⣿⣿⣿⣿⣿⠀⣿⢭⡇⣿⣿⢀⣻⣿⣿⣤⣀⠈⠛⠿⢿⣿⣿⣿⣿⣿⣿⠿⠿⠟⠋⢡⣤⠟⠋⢀⣎⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣿⢈⡇⣾⡇⢶⣿⣿⣦⣌⡙⠛⠿⢿⢟⣽⠃⠰⠀⠘⣆⡽⣿⣿⣿⣷⠾⠋⡾⣹⣿⠇⢢⣿⣿⠿⢿⣿⣷⣧⣄⣠⠀⢀⠄⠀⠀⠀⢀⣤⣴⠾⡏⠁⡜⢀⢎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡶⣁⠞⣸⣿⣷⣬⣥⣾⣿⣿⣿⣿⣿⣿⣿⡇⢀⠆⠀⠀⠈⠓⠳⠼⢤⠧⠤⠋⠀⣿⡟⢰⣿⡏⣼⣶⣄⠙⣿⣿⣿⣿⣿⣿⣶⡾⣿⠛⠋⣹⠃⡐⠀⡐⢀⢏⣾⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣩⠷⡛⡍⣠⣿⣿⣿⣿⣿⢿⠿⠿⠿⠿⠟⠛⠛⠛⠛⠿⠿⠷⠶⣶⣶⣦⣤⣤⣄⣀⣸⣿⠁⣾⣿⣿⣥⣼⣿⣷⡈⢿⣿⣿⣿⣿⠟⢓⢣⡀⣴⠃⡠⠁⣰⣠⣏⣾⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣠⣤⣶⠿⠛⠛⢉⡭⠧⢤⠖⠚⠒⠶⠚⠛⠛⠚⠋⠙⡒⠋⠙⠒⠒⠒⢤⡤⢤⣉⣉⡛⠛⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠙⢿⣿⣿⡖⡻⠊⣿⠏⣴⣿⠋⣹⣈⣩⠛⣿⣿⣿⣇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢛⣩⡴⠖⠖⠋⠉⣉⡤⣤⡤⠖⠲⠤⠖⠒⠒⠶⠚⠓⠶⠒⠓⠶⠶⠦⣤⣀⣀⡀⠈⠁⠉⠛⠚⠒⣤⣤⣉⠛⠻⠿⣿⣿⣿⣷⣦⣬⣭⢭⣤⣼⠏⣰⡧⣤⣾⣹⣽⠙⣧⠸⣿⢯⢿⡎⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢉⡠⠤⠤⠚⠋⠋⣁⣠⣀⡤⠤⠤⣤⠤⠶⠦⠤⠒⠢⡤⠖⠦⣤⠤⣄⡀⢀⡀⠉⠉⠙⠒⠒⠦⣄⣀⡀⠈⠙⠓⠦⣤⣉⡙⠻⢿⣿⣇⣴⣿⡟⠠⠙⡆⢻⣿⣿⣿⡇⣽⡇⣿⠃⠈⢿⣎⠻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠉⣀⣤⣤⠖⢒⣞⣡⣤⣬⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣀⣀⣉⠉⠉⠒⠚⠲⠤⠤⣄⡀⠀⠉⠓⠲⢤⣀⣀⠀⠛⠒⢦⣈⠙⠻⢿⣤⣁⠀⠻⣀⠻⡿⠿⢿⣋⣾⣃⣤⣄⡀⢹⣷⣬⡛⢿⣿⣿⡿⠟
⣿⣿⣿⣿⣿⣿⣿⣿⡵⠚⠉⣠⣴⡾⠿⢛⣛⣩⣭⣽⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣿⡷⢶⣦⣤⣄⣀⠉⠉⠳⠦⢤⣀⠈⠉⠳⠶⢄⡀⠉⠙⠶⣄⡈⠙⠷⣦⣼⣿⣿⣿⣿⢛⡿⢡⡿⠦⣹⣿⣿⣿⠿⢶⢦⣶⣤⣶
⣿⣿⣿⣿⣿⣿⣿⡏⢀⣴⡿⢋⣥⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣛⡿⠷⣶⣤⣀⡈⠉⠙⠦⢤⡀⠉⠙⢦⣀⡀⠉⠓⢦⣌⠙⠻⣿⣿⣣⠏⠙⢯⣱⣠⣿⠹⣿⠏⢀⡎⣾⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣣⣿⢋⣰⣿⣿⣿⣿⣿⣿⢿⡿⠋⠉⠀⠀⠀⠀⠀⡠⠂⠉⠀⠀⠀⠀⠀⠀⠀⢋⡉⠛⠛⠿⢿⣿⣿⣿⣿⣷⣶⣭⣝⡛⠿⣶⣤⣀⡉⠓⠲⣄⡀⠙⠲⢦⣀⠈⠙⠶⣌⡙⠿⣦⡀⠀⣠⣿⣿⡄⢿⢀⣮⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢡⣲⣿⣿⣿⣿⣿⢻⠕⠋⠀⠀⠀⠀⠀⠀⠀⠀⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠄⠀⠀⠀⠉⠙⠻⠿⣿⣿⣿⣿⣷⣶⣭⣽⣻⢷⣦⣌⡉⠳⠦⣄⠉⠳⢦⣀⠈⠳⢦⡈⠻⣷⣿⣿⣿⡿⡈⢾⠇⣸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢰⣿⣿⣿⣿⠻⣠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⢩⠟⣿⣿⣿⣿⣿⣿⣷⣾⣝⣻⣶⣤⡈⠛⢦⣀⡈⠳⣄⠈⠉⢷⣈⠛⣿⣏⠀⡽⣷⣾⣿⣿⣛⣛⡿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢃⡓⠰⠼⡄⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⠀⠀⠀⠀⠀⠀⠀⣠⠏⡸⢄⢢⠙⡻⢿⣿⣿⣿⣿⣿⣷⣿⠿⣷⣤⡈⠹⢤⡈⠛⢦⡀⠙⢦⡄⠻⣷⣶⣿⣿⡿⢾⣿⣭⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠫⠔⢢⠑⣌⠲⣽⡀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⢠⡞⡥⢊⡕⢊⠦⡱⡁⢦⠙⢿⣿⣿⣿⣿⣿⣷⣶⣙⠻⣶⣄⠛⢲⣄⠻⣦⡀⠻⣤⠈⢻⣿⣿⣿⢹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⡊⡜⢣⠚⠤⡛⢼⡇⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡃⠀⠀⠀⠀⠀⠈⠛⠒⠯⢔⣍⠲⣡⢑⠢⣉⠤⠚⣿⣿⣿⣿⣿⣿⣿⣿⣬⡛⣷⣄⠙⢷⡈⢷⣄⠈⢷⡄⠹⣿⣿⣧⣽⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠰⠘⡼⢡⢋⡖⣩⢺⠀⠀⠀⠀⠀⠀⠀⠀⢁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣤⢉⢦⢁⠎⡰⢈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣻⣿⣄⠻⣆⠹⣧⡀⢳⡀⠸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢙⡌⠱⣈⠓⠦⡜⣄⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢮⡒⢌⠢⡑⢠⢺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⢷⡈⣧⡈⣿⡅⡹⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢂⡌⠒⠤⣉⢎⠱⣈⢎⠩⡳⠀⠀⠀⠀⠀⠀⠀⡈⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⡠⠀⠃⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣴⣽⣦⣱⣬⣅⡚⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣄⢻⡙⣧⡆⢿⣼⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠦⢌⢡⣉⢆⡊⢖⡉⠦⣙⠃⠀⠀⠀⢀⠉⣀⣀⣈⠒⣂⣉⣀⠀⠈⡁⠒⠒⠒⠂⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣿⡌⣿⡙⣷⣦⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⡇⣌⢢⠐⠢⡙⡆⣍⢒⣉⣳⣤⣶⣮⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡬⢣⡀⠀⠀⠀⢀⣠⠖⡳⠩⢍⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⡎⣿⣤⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡧⡑⠤⣂⢍⡒⡡⢒⣬⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡹⣒⠶⡖⢯⡜⡮⡱⣉⢮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢌⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⡅⠓⢌⠒⡌⡱⢬⣿⣿⣿⣿⣿⡿⢿⣻⠭⠯⠝⢿⡻⢿⣿⣿⣿⣿⣿⣟⢲⡉⢖⣹⡆⡞⣥⡑⢢⣿⣿⣿⣿⣿⣿⢿⣻⠿⠭⠽⢶⡳⠿⢭⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡧⢜⠨⡐⢌⡰⢱⣿⣿⡟⡱⢨⣱⠚⠉⢀⣀⣀⣀⣀⣙⣦⢢⡙⡛⢟⢫⡉⢦⡝⠁⢀⡈⠳⣆⡘⣿⣿⣿⣿⣿⣏⡵⠊⠀⠀⠀⢀⣠⣼⢳⣬⢙⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡗⢌⠢⡑⢢⠒⣿⣿⡿⢣⠑⣡⣾⠶⢛⡉⡏⣀⣰⣇⣭⣝⡻⢶⣍⡒⠦⣘⣼⠀⠀⠁⠈⡄⠱⡜⣿⣿⣿⢿⡿⢋⣠⣶⣶⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠄⠣⢅⡡⠎⡔⠢⢔⢃⣷⣋⢠⣶⣶⣿⣿⣟⣻⣿⣿⡿⠻⣷⣮⣙⠊⠉⠉⠀⠀⡇⠀⢰⠀⡧⢿⣿⡟⣋⣴⡿⡟⣁⠈⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠬⢑⠢⠆⡵⣈⢓⡎⢖⣸⣷⣿⣿⡉⠉⠻⣿⣿⠿⠿⢇⠴⣿⣿⣏⡓⠀⠀⠀⠀⡇⠀⠰⠀⡟⣸⣿⣗⠤⣙⢦⡒⢆⡒⠶⢶⣠⣐⢾⣁⣿⣿⣿⣿⣿⣿⣟⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡸⢄⡎⢍⡲⢍⣣⡼⠖⠺⣘⣿⡟⣛⣒⢚⣥⠶⢖⡚⣫⡽⢛⠍⠡⠃⠀⠀⠀⠀⢁⠀⠀⡀⢳⢂⣿⣿⡎⡽⡀⠈⠑⣞⠻⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⡘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⡘⢢⢱⠋⠀⠀⠀⠀⠙⠚⢳⠶⣌⡧⢧⠾⠖⠋⢁⠔⠁⡔⠀⠀⠀⠀⠀⠀⢈⠀⠀⠆⢸⠣⢿⣿⣿⡔⡩⢷⠀⠀⠙⠒⠭⣍⠭⡙⢩⢡⡘⡌⢩⡙⠦⠸⢌⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠿⣿⢛⢿⣿⣿⢌⡱⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠠⠀⠐⠊⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠈⠀⠀⠆⠈⢧⢻⣿⣿⣿⡔⡩⢦⡀⠀⠀⠀⠘⠶⢍⠒⢢⠢⠱⢆⠱⢉⢎⣺⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⢿⣶⣍⠬⢹⣿⠏⡔⢂⢿⠀⠀⠀⠀⠀⠀⠀⠀⢆⠁⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠸⠀⠀⠆⠀⠈⢧⡛⠻⢿⣷⡱⠆⠧⠤⣀⡰⣋⠱⡌⢮⡱⣉⠗⡌⠒⠎⠆⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡾⣿⣿⣿⣦⡼⠑⡬⢌⢺⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⡀⠀⠀⠀⠀⠀⠠⠁⢀⠀⠀⠀⠀⡠⠃⠀⠀⠈⡀⠀⠀⣳⠍⣶⣟⡷⣉⢻⠰⣍⠲⣡⠣⡜⢢⡐⢱⠨⠌⡓⡘⢦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣷⠹⣿⡿⢿⣿⣯⠰⣩⠌⡳⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⠀⠠⠄⠃⢠⡞⠀⡠⠐⢁⣀⡀⠀⢀⠠⠁⢀⠴⣃⢎⠹⡉⢱⢼⣦⠓⡌⡓⡄⠓⡬⢑⠌⡆⣣⣚⣥⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣧⢹⢒⡸⣿⣿⢧⡔⢬⢡⡏⠶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢧⡀⢈⣈⣄⣀⠀⠉⢀⡠⢞⡱⢣⣭⣾⣿⣿⣿⣿⣷⡡⢎⠱⢬⡑⣤⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣧⣽⣆⠿⣿⡜⣿⣎⠱⡊⠵⣠⠋⡵⢲⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣎⢭⣿⣶⣾⣬⣋⠽⢭⡘⢦⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⢋⠒⡔⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡟⢈⣡⡾⡧⢿⣿⣧⡘⠱⡠⠏⡜⣡⢃⢦⡙⡲⢄⠀⠀⠀⠀⠀⠀⠀⠘⢾⡿⠿⡟⢛⠻⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠪⣑⠣⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣸⣗⣸⡗⢸⣿⣿⠿⢣⡑⢊⠴⣡⢚⠲⣱⠱⣉⢧⠀⠀⠀⠀⠀⠀⠀⢠⡽⣶⣥⣬⣷⡙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢫⠥⣒⠡⣇⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢛⢋⡛⣹⡿⢠⠣⣁⢎⢣⡓⢴⢩⠲⣁⠛⡌⠾⡄⠀⠀⠀⠀⠀⠀⠀⣽⣷⣿⢻⡯⠘⣕⣢⣜⣻⠒⠯⣛⠹⢿⣿⣿⣿⣷⣦⢑⢣⣢⡡⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢐⢡⠒⢥⢊⠦⢍⢢⢋⡖⣡⠛⡬⢑⢣⠀⠀⠀⠀⠀⣨⣾⣿⣿⡩⠛⢉⣿⣩⣥⣀⣠⢴⣶⣿⣷⣦⣭⣙⡛⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⢄⡋⢆⠣⢊⠵⣊⠵⡘⣤⠓⡴⡉⢦⡙⣲⣧⣶⣿⣿⢿⠿⢁⣤⢚⡿⣛⡺⣿⠆⣱⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣧⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⠢⣑⢊⡜⣡⠓⢬⡑⢎⡴⣉⢆⠹⣰⣧⣿⣿⣿⠟⣡⢧⣾⣿⡿⣜⣴⣿⣵⣶⣘⣘⣿⣿⣿⣿⡿⣿⢿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡑⠦⢊⠴⡁⢎⢡⠚⠴⢰⡡⢆⠣⢝⠫⣿⣿⣿⡮⣽⣿⢿⡿⠿⠿⠛⠻⠋⣉⡋⢻⠛⠛⢣⣀⣰⡜⢾⣳⡗⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣈⢇⠚⡌⢣⢊⠝⣈⠇⡜⢢⡡⢌⠣⢼⣿⣿⡑⢷⣦⣀⠐⣼⡦⠤⣾⣀⣠⣸⣏⣧⢰⡛⣥⣖⣿⣧⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠊⡕⣈⠆⡍⠒⠬⡘⣌⠒⡔⣊⢒⠩⢍⠩⢔⣡⣾⢿⣯⣼⣔⡿⢧⣮⡴⣿⣣⢼⣿⣞⣣⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡰⡁⢎⠰⣉⠒⡥⢊⢥⢙⠤⣃⠎⣌⠳⣌⠲⠡⠎⢿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣆⢣⢄⡓⢌⡱⢊⠬⡒⡌⠞⣤⠓⢎⡱⢉⢳⡌⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡜⣄⠲⣉⠖⡡⠜⣡⠪⢽⣂⣴⣯⠘⣿⣿⠿⣛⡛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣿⣷⣧⡌⠦⡑⢎⠴⡉⢦⡐⢢⠂⣍⢩⢂⡱⢌⡳⢍⠢⣌⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣷⣭⣌⠲⣩⣦⢹⡆⡱⢬⣇⠼⣰⣆⠼⠗⢣⣔⡨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠥⢃⠝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣽⣼⣿⣦⡹⢟⣱⣿⣿⣿⣿⣤⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⡎⢖⡡⢛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠱⡘⢢⡑⣌⠲⡩⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⠣⡘⣄⠲⠬⡰⢡⠳⢌⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠣⢜⡠⢇⠲⣄⢣⡑⢎⠱⡠⣏⢛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⡇⠍⡦⢱⡈⢣⡘⢢⠙⢢⠑⠴⣈⠛⠶⣝⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⡎⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⡛⢾⣯⠘⡜⣡⠜⠢⡜⡡⡘⢤⢛⠷⠦⢮⣵⣠⣋⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣹⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣈⣷⢉⡲⠤⣉⠧⣐⠣⡙⢢⠍⢎⠥⣃⠬⣉⢍⡻⠿⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠿⠋⠁⣿⣜⣧⠹⣧⢊⡔⢢⢁⣒⠌⢃⠍⡢⠜⢢⢒⡱⠒⡥⢆⠒⡌⢆⣩⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⣾⣇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠠⣯⢻⡟⢶⣿⠢⠜⠢⢥⢒⡜⢪⠜⣡⡙⣅⠪⡔⢩⠐⠮⠜⠬⢌⠰⣄⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣻⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⣿⢶⣿⣆⣿⢌⡙⣒⡎⡱⢚⠥⣋⠴⡱⢌⡱⢌⢣⢌⠱⢌⠣⣉⠲⣄⠆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣀⠀⠀⠀⠀⠒⠠⠀⠀⠀⠀⣿⣈⣿⡉⣿⠈⠒⠥⣸⢡⢛⣊⡑⢎⡱⠎⡴⡉⣆⢚⠒⣌⡱⣐⠦⡰⢌⡸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣷⣿⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿