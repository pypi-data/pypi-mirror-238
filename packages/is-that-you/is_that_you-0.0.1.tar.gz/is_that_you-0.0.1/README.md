# Prerequisites

* Install Python 3.8

# Running

* `source venv/bin/activate`
* `pip install -r requirements.txt`
* `python program.py`

# Possible emotions

* anger
* disgust
* fear
* happy
* sad
* surprise
* neutral

# I'm out of energy to write all of this right now, so...

Please, just check the help message by providing the `--help` flag to the module when running it. It has some flags that will most likely be useful to you. Also, https://github.com/megahomyak/freddy\_camera is a pretty similar project, you can take some hints from it

# Adding your own files

Prepare files with names in these formats: "EMOTION\_mouth\_closed.png" and "EMOTION\_mouth\_open.png". It is not mandatory to provide every single variation, you can provide only the ones you'd want to have (except for "neutral\_mouth\_closed.png", which is the default emotion)

You might find the `--path` argument useful for specifying the path to the directory with the images
