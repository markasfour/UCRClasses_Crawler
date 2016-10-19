# UCR Classes Web Crawler
This python script retrieves UCR class information from http://classes.ucr.edu and stores it into a Firebase database.

## Usage
### Arguments
* **-r** : Reverses the subject list to iterate through
* **-h** : Halves the subject list
* Two more arguments can be passed to indicate the starting subject and/or the ending subject (subjects are 4 characters each. Use '' to include spaces)
#### Example
```
python retrieve_classes.py -r 'CS  ' 'BIOL' 
```
This will reverse the subject list to iterate through and will cause the script to start at CS and end at BIOL.
```
python retrieve_classes.py -h 'ECON'
```
This will cut the subject list in half and will cause the script to start at 'ECON'.
