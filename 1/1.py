def FinalFrequency(frequency, inputs):
    for val in inputs:
        frequency += val
    return frequency

def RepeatedFrequency(frequency, frequencies, inputs):
    while True:
        for val in inputs:
            frequency += val
            if frequency in frequencies:
                return frequency
            frequencies.add(frequency)

inputs = [ int( line.rstrip("\n") ) for line in open("input.txt") ]

frequency = 0
frequencies = set([frequency])
print(FinalFrequency(frequency, inputs))

frequency = 0
frequencies = set([frequency])
print(RepeatedFrequency(frequency, frequencies, inputs))
        
