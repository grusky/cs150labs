# vol.py
# Tom Wexler
# 4/1/13
# Middle C ramping up from 0 to 1.5 volume, and back down again.
# Testing soundwave volume.

import soundwave

def main() :
 
    dur = 0.0612
    music = soundwave.Soundwave()
    vols = []
    for i in range(30) :
        vols = vols + [soundwave.Soundwave(0,dur,i/20)]
    
    for w in range(30) :
        music.concat(vols[w])
    
    for w in range(29,-1,-1) :
        music.concat(vols[w])
    
    music.play()
    
main()