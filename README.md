Vite Vite for Kivy was conceived as a kind of Bootstrap for Kivy, the phenomenal new Python GUI framework for mobile and desktop. The goal of this project is to create a toolkit of attractive, reusable components that will make Kivy app development faster and easier.  At the moment, Vite Vite is confined to Android components, but other platforms may eventually be added. 

## Installation
For convenience, I've already created a build script for Vite Vite on Linux. This script builds an installable apk package from the base Vite Vite app (main.py and its dependencies) and optionally installs the package to your Android device.  To use this script, you must first set up the Android SDK and Kivy.  Once you have this environment configured, enter the appropriate settings in the `build.cfg` file in the root directory.  Then run the `build.sh` shell script.

### Options
The script takes the following optional flags and values:

**-c**
    Pass a configuration FILE other than the default `build.cfg`.
    
**-b**  
    Takes a BUILD value of either `debug` or `release`.
    
**-a**
    This flag tells the script to install the finished package to your attached android device using `adb install`.


**Example**

`./build.sh -c myconfig.cfg -b release -a`

Builds a release Android package using the settings indicated in myconfig.cfg and installs it to the attached Android device. 

## License

This framework is licensed under the terms of the MIT license.
