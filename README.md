# Math-Hotkey
**Supports: 64-Bit Machines, Windows 10**

Ever been writing in a document or playing a game and have a math problem that you already had typed out and so didn't wanna pull out your calculator to type it in again?<br>
Using the keys `control`+`shift`+`e` will take any selected text and attempt to evaluate it as a math problem.<br>
This program I made will check text you have selected, and evaluate it as a math problem. It emulates the hotkey `control`+`x` cut hotkey to copy text, so wherever you can use that, you can use this!  

Worried about the fact it uses the computer's cliboard? Don't be! Anything you have copied before you run the hotkey will be saved and then put back into your pc's clipboard after the math is done.

## Installation
Download the .zip folder from the [releases page](https://github.com/JesseBS2/Math-Hotkey/releases/latest) to your PC. Move file to desired location and unzip. You can then run the MathHotkey.exe.
Run the file and a new icon will be added to your system tray, from then you can use your hotkey combination wherever it is available.

### Auto run
I'm sure there are many ways to run a program at Windows startup, I prefer the following way:
1) Find the MathHotkey.exe and create a shortcut
2) Open Run Command box by pressing (Windows + R)
3) Type **shell:startup** and press enter to open the windows Startup folder
4) Move the exe shortcut into the to Startup folder

## Customization
To customize your hotkeys, navigate to the program folder and into the `_internal` folder, then into `settings` folder.
The customization settings are in the `config.json` and acceptable keys for the hotkey are in the `readme.txt`
<br><br>

## Usage Examples
### Document
![Literally Math](https://github.com/JesseBS2/Math-Hotkey/blob/master/examples/document_use_gif.gif)<br>
An example of math that is already typed out, but normally can't be calculated unless using some external application


### Minecraft
![Wall Count Calcs](https://github.com/JesseBS2/Math-Hotkey/blob/master/examples/mc_use_gif.gif)<br>
This is one I've come across quite a few times myself, needing to know how many blocks to get to fill in a given space. This is actually the issue that gave me the idea of this program
