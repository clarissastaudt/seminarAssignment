"""
Provide all specifications made by the user.
"""

class Specifications:
    
    def __init__(self):
        self.seminars = []
        self.lecturers = []
        self.seminarTimes = []
        self.maxParticipants = []
        self.weights = [2, 1, 0]
        self.studentsInSem = []
        
    # Read in specifications from file    
    def getSpecifications(self, file):
        with open(file, 'r') as spec:
            count = 0
            for line in spec:
                line = line.split("\t")
                if count > 0:
                    self.seminars.append(line[0])
                    self.maxParticipants.append(int(line[1]))
                count += 1
            self.studentsInSem = [0] * (count-1)

