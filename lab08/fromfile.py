# fromfile.py
# Tom Wexler
# 4/1/13
# Creates a soundwave from a .wav file.
# Testing your soundwave constructor and play function.

import soundwave

def main() :
 
    snippet = soundwave.Soundwave("../Mfiles/M55.wav")
    snippet.play()
    
main()