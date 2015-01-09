# middlec.py
# Tom Wexler
# 4/1/13
# Creates and plays a soundwave containing a two-second Middle C note.
# Testing your soundwave constructor and play function.

import soundwave

def main() :
 
    note = soundwave.Soundwave(0, 2, 1)
    note.play()
    
main()