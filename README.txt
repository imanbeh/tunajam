WELCOME TO TUNAJAM
This program allows the user to input a file from their working directory and listen to it as an animal of their choice.
The animal version is created using fourier analysis with varying frequency thresholds.
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Prerequisites:
Make sure flask and all other dependencies are installed on your computer.

Instructions for use:
1) Download and open the tunajam zip file
2) Open terminal and set your working directory to the tunajam folder
3) In terminal, write
>> flask --app musicscaling run
This runs the music scaling app. 
4) In the terminal output, there will be a line reading
 * Running on http://127.0.0.1:5000
Paste 'http://127.0.0.1:5000' into your browser.
5) You are now accessing a local tunajam application. 
Upload an mp3, select an animal, and click the 'Become an Animal' button. Enjoy!
6) Type ^C (control+c) in terminal to end the run.

Customization – Add an animal:
1) On line 48 in the 'sample' function of musicscaling.py, add
>> elif selected_animal == 'your_animal':
>>      threshold = x
Where 'your_animal' is the name of your animal, and 'x' is the highest integer frequency it can hear.
This allows the code to properly process the user selecting your animal.
2) On line 88 of index.html, add
>> <option value='your_animal'>Animal – x MHz</option>
Where 'your_animal' and 'Animal – x MHz' is the name of your animal and its frequency threshold (x).
This adds an option in the dropdown menu for the user to select your animal.
3) Save both files and run
>> flask --app musicscaling run
in your terminal.


