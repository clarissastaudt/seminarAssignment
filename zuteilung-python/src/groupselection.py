import pandas as pd
import numpy as np
import specifications as spe
import checkSolution


"""
Generate a dictionary containing the assignment info sorted by seminar.
"""
def generateSeminarDict(overviewSeminars, specs, df):
    for sem in specs.seminars:
        overviewSeminars[sem] = []
        for index, row in df.iterrows():
            if sem in row["inSeminar"]:
                overviewSeminars[sem].append({'student': row['student'], 'mail': row['mail'], 'comments': row['comments']})
    return overviewSeminars

"""
Create a file with the assigned students for each seminar.
"""
def createFileForEachSem(overviewSeminars):
    for sem in overviewSeminars:
        with open('../data/results/results_by_seminar'+ sem + '.csv', 'w') as f:
            f.write("student\tmail\tcomments\n")
            for d in overviewSeminars[sem]:
                f.write(d["student"] + "\t" + d["mail"] + "\t" + d["comments"] + "\n")


"""
Find a greedy solution for the seminar assignment problem.
"""
def basicSolution(specs, df):
    
    # Look at highest weights first
    for weight in specs.weights:
        # Fill seminar by seminar
        count = 0
        for sem in specs.seminars:
            # Gives higher priority to students who didn't receive a seminar yet
            df = df.sort_values(by=['openSeminars'], ascending=False) 
            for index, row in df.iterrows():
                # Check if there is a space in the current seminar left
                if specs.studentsInSem[count] < specs.maxParticipants[count]:
                    # If the student still needs a seminar 
                    if len(row['inSeminar']) < int(row['neededSeminars']):
                        if row[sem] == weight:
                            # Update the number of open seminars for the student
                            df.at[index,'openSeminars'] -= 1
                            # Add the new seminar for the student
                            copy = df.loc[index, 'inSeminar'].copy()
                            copy.append(sem)   
                            df.at[index, 'inSeminar'] = copy
                            # Add a new student to the total number of students in this seminar
                            specs.studentsInSem[count] += 1
                            # Update priorities for this student
                            df.at[index, 'totalGivenPriorities'] += df.at[index, sem]   
            count += 1
    #calcTotalWeight(df)
    return df
   
    
"""
Prints data that can be used to understand the result achieved by the assignment. Use this function for debugging and to evaluate potential improvements.
"""
def calcTotalWeight(df):
    totalWeightStudents = []
    for index, row in df.iterrows():
        totalWeightStudents.append([row[sem] for sem in row['inSeminar']])
    print(totalWeightStudents)
    
    averageWeight = sum([sum(p) for p in totalWeightStudents])/len(totalWeightStudents)
    print("Average weight per student: {}".format(averageWeight))
    
    stdWeight = np.std([sum(el) for el in totalWeightStudents])
    print("Std weight per student: {}".format(stdWeight))    

    
def main():
    
    # Get specifications for offered seminars
    specs = spe.Specifications()
    specs.getSpecifications('../data/input/specifications.csv')

    df = pd.read_json("../data/input/seminarwahl-export.json").T

    # Get student data and initialize attributes
    df["inSeminar"] = [list()]*df.shape[0]
    df["openSeminars"] = df.neededSeminars
    df["totalGivenPriorities"] = [0]*df.shape[0]
    
    # Calculate a basic solution (some students might receive a seminar with priority 0)
    df = basicSolution(specs, df)
    
    checkSolu = checkSolution.checkSolution()
    error = checkSolu.checkAll(specs, df)
    print(error)
    
    # Generate a seminar dictionary
    overviewSeminars = generateSeminarDict(dict(), specs, df)
    
    # Create a file with the current state of the program
    # Mainly for debugging and error detection purposes
    df.to_csv('../data/results/results_by_student.csv', sep='\t')
    
    # Create a file with the assigned students for each seminar
    createFileForEachSem(overviewSeminars)     
        
main()
