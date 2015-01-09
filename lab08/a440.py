# a440.py
# Tom Wexler
# 4/1/13
# Creates and plays a soundwave containing a two second A note.

import soundwave

def main() :
 
    note = soundwave.Soundwave(-3, 2, 1)
 
    note.play()
    
main()