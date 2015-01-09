import audio, math, time


class Soundwave :
    """
    Construct a new SoundWave object containing a note x halftones
    from middle C with length t seconds and amplitute amp.
    """
    
    def __init__(self, x=0, t=0, amp=1) :
        self.w = []
        if isinstance(x,str) :
            self.w = audio.read_file(x)
        else :
            for i in range(int(44100*t)) :
                self.w.append(amp*math.sin(2*math.pi*440*(2**((x+3)/12))*i/44100))

    def concat(self, s2) :
        self.w.extend(s2.w)
        
    def join(self, s2) :
        return self.copy().concat(s2.copy())
    
    def copy(self) :
        neww = Soundwave()
        for i in self.w :
            neww.w.append(i)
        return neww
    
    def play(self) :
        audio.play(self.w)
        
    def plus(self, s2) :
        if len(self.w) >= len(s2.w) :
            longer = self
            shorter = s2
        else :
            longer = s2
            shorter = self
        neww = longer.copy()
        for i in range(len(shorter.w)) :
            neww.w[i] = neww.w[i] + shorter.w[i]
        return neww
        
    