# furelise.py
# Tom Wexler
# 4/1/13
# Beethoven's Fur Elise.
# Testing the soundwave concat operation.

import soundwave

def main() :
 
    dur = 0.3
    music = soundwave.Soundwave()
    a = soundwave.Soundwave(9,dur)
    b = soundwave.Soundwave(11,dur)
    c = soundwave.Soundwave(12,dur)
    d = soundwave.Soundwave(14,dur)
    ds = soundwave.Soundwave(15,dur)
    e = soundwave.Soundwave(16,dur)
    
    music.concat(e)
    music.concat(ds)
    music.concat(e)
    music.concat(ds)
    music.concat(e)
    music.concat(b)
    music.concat(d)
    music.concat(c)
    music.concat(a)
    music.concat(a)
    music.concat(a)
    music.play()
    
main()