"""
Check the generated assignment solution for potential errors.
""" 
class checkSolution:
    
    """
    Generate error message for all test cases.
    """ 
    def checkAll(self, specs, df):
        self.solutionOptimal(specs, df)
        error = "Warnings:\n___________\n\n"
        error = self.prio0(specs, df, error)
        error = self.studWithoutSem(specs, df, error)
        error = self.emptySem(specs, df, error)
        return error
    
    """ 
    Check whether an optimal solution was achieved.
    """
    def solutionOptimal(self, specs, df):
        # Is assumed to be a solution where everyone gets the highest priorities for all seminars needed
        # Is only a heuristic (f.e. won't be accurate if a student needs 2 seminars but only gives priority 2 to one seminar.)
        optimalSolution = [] 
        for el in [i for i in df.neededSeminars]:
            optimalSolution.append(2*el)
        optimalSolution = sum(optimalSolution)
        currentSolution = sum(df['totalGivenPriorities'])
        # Check whether solution is optimal
        if currentSolution == optimalSolution:
            print("An optimal solution to the seminar assignment problem could be determined.")
    
    
    """
    Check whether a student received a seminar with priority 0.
    """
    def prio0(self, specs, df, error):
        error += "Students who received a seminar with priority 0:\n"        
        for index, row in df.iterrows():
            for el in row['inSeminar']:
                if row[el] == 0:
                    error += "- " + row["student"] + ": " + el + "\n"
        return (error + "\n")
    
    
    """
    Checks whether a student has open seminars.
    """
    def studWithoutSem(self, specs, df, error):
        error += "Students who received less seminars than specified:\n"  
        for index, row in df.iterrows():
            if row['openSeminars'] != 0:
                error += "- " + row["student"] + "\n"
        return (error + "\n")
    
    
    """
    Checks whether a seminar has less than five participants.
    """            
    def emptySem(self, specs, df, error):
        error += "Seminars with less than five participants:\n"
        for counter, sem in enumerate(specs.studentsInSem):
            if sem < 5:
                error += "- "+ specs.seminars[counter] + "\n"
        return (error + "\n")