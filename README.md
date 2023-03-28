# MIDI2Matrix
A python tool that converts MIDI files to matrices

Dependencies: mido, numpy

Usage:
Call the `generate_dataset` function
```
MatrixGenerator.generate_dataset (input_path, output_path, file_count=0, max_length=0, 
note_range=(-1, 128), time_steps=(0, 0, 0), include_stops=True)
```

## Parameter:

`input_path`: *str*

 * the path to the directory contains MIDI
  
`output_path`: *str*

 * the path to the file to be created
  
`file_count`: *int, optional*

 * the total count of MIDI files

 * if not given, the program will iterate through the directory to find out

`max_length`: *int, optional*

 * the maximum length of all MIDI files, in ticks
  
 * if not given, the program will iterate through the directory to find out
  
`note_range`: *tuple, optional*

 * a tuple contains the minimum and maximum pitch of all MIDI files
  
 * if not given, the program will iterate through the directory to find out
  
`time_steps`: *tuple, optional*

 * a tuple contains (ticks_per_beat, clocks_per_click, 32nd_notes_per_beat)
  
 * if not given, the program will iterate through the directory to find out
  
`include_stops`: *bool, optional*

 * indicate whether an additional row recording 'note_on' info is needed
  
 * set to True as default
