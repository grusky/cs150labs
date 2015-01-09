# surprise.py
# Tom Wexler
# 4/1/13
# Probably not what you least expect.
# Testing the soundwave plus operation.

import soundwave

def main() :
 
    dur = 0.3
    
    music = soundwave.Soundwave()
    c53  = soundwave.Soundwave(0,3*dur)
    db53 = soundwave.Soundwave(1,3*dur)
    eb52 = soundwave.Soundwave(3,2*dur)
    eb53 = soundwave.Soundwave(3,3*dur)
    f53  = soundwave.Soundwave(5,3*dur)
    gb52 = soundwave.Soundwave(6,2*dur)
    gb53 = soundwave.Soundwave(6,3*dur)
    ab52 = soundwave.Soundwave(8,2*dur)
    ab53 = soundwave.Soundwave(8,3*dur)
    bb63 = soundwave.Soundwave(10,3*dur)
    c63  = soundwave.Soundwave(12,3*dur)
    db63 = soundwave.Soundwave(13,3*dur)
    eb63 = soundwave.Soundwave(15,3*dur)
    f63  = soundwave.Soundwave(17,3*dur)
    f61  = soundwave.Soundwave(17,1*dur)
    gb6h = soundwave.Soundwave(18,dur/2)
    ab6h = soundwave.Soundwave(20,dur/2)
    
    ch1 = db53.plus(gb53).plus(bb63).plus(db63)
    ch2 = eb53.plus(ab53).plus(c63).plus(eb63)
    ch3 = eb52.plus(gb52).plus(ab52)
    ch4 = c53.plus(f53).plus(ab53).plus(c63).plus(eb63)
    ch5 = f53.plus(bb63).plus(db63).plus(f63)
    ch6 = db53.plus(gb53).plus(bb63).plus(db63)
    ch7 = c53.plus(eb53).plus(gb53).plus(ab53)
    
    music.concat(ch1)
    music.concat(ch2)
    music.concat(ch3)
    music.concat(ch4)
    music.concat(ch5)
    music.concat(ab6h)
    music.concat(gb6h)
    music.concat(f61)
    music.concat(ch6)
    music.concat(ch2)
    music.concat(ch7)
    
    music.play()
    
main()