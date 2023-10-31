# IS THAT YOU?

"IS THAT YOU?" is a vtuber software that automatically recognizes your emotions and changes your vtuber image to show the appropriate emotion. It also opens and closes the character's mouth when !

# Installation

If you have any trouble during installation, you can consult me: https://t.me/megahomyak

* Windows: Install Python 3.8 (don't forget to check the "Add to PATH" checkbox)
* macOS, Linux: Install Python 3.8
* Windows: Open the console (Google how to do it on your OS) and enter `python -m pip install is_that_you`. Get ready for this installation to take a very long time due to very big libraries being used for emotion recognition
* macOS, Linux: Open the console (Google how to do it on your OS) and enter `python3 -m pip install is_that_you`. Get ready for this installation to take a very long time due to very big libraries being used for emotion recognition

# Preparing the images

To make the program accept your own character images, place all of them into a folder of your choice. All the images should be of the same size and having the name in the format of either "{emotion name}\_mouth\_open.png" or "{emotion name}\_mouth\_closed.png" (without braces; yes, they should be PNGs). You don't have to provide the images you don't want to be shown, except for the "neutral\_mouth\_closed.png" image, which is the default one

## Possible emotions

* anger
* disgust
* fear
* happy
* sad
* surprise
* neutral

# Running the thing

* Windows: Open the console again, run `python -m is_that_you --help` to get the list of available flags
* macOS, Linux: Open the console again, run `python3 -m is_that_you --help` to get the list of available flags
* Rerun the command without the `--help` flag and with the flags you need (for example, you will almost certainly have to specify the `--path` to the directory with the images)
