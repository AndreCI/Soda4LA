WINDOWS
Install fluidsynth by copy pasting the dll to system32. 


Adding dlls to path seems to work but ends up with weird errors and no sounds:
ImportError: Couldn't find the FluidSynth library.
OSError: [WinError 193] %1 is not a valid Win32 application fluidsynth -> check if versions are 64 bits (python, fluidsynth)
After fixing those, I got:

pyfluidsynth fluidsynth: error: not enough MIDI in devices found expected 1 found 0
fluidsynth: error: Device "default" does not exists
fluidsynth: warning: sequencer: Usage of the system timer has been deprecated!
----------------------------------------------

Also build from source using https://github.com/FluidSynth/fluidsynth/wiki/BuildingWithCMake#building-with-msys2-on-windows
Did it help?