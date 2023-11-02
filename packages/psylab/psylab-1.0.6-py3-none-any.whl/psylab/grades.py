import sys

def get_letter_grade(score, grade_lookup=None):
    """Given a percent correct score, return a corresponding letter grade

        Parameters
        ----------
        score: float
            The score to use
        grade_lookup: dict
            The grade lookup table to use. The default uses standard grade scheme 
            with rounding, eg., 89.5 or greater is an A-, 87 - 89 is a B+, 
            83 - 86 is a B, 80-82 is a B-, etc. You can look at the default 
            grade_lookup dict below to see how it should be structured

        Returns
        -------
        grade: str
            The letter grade, as a str

    """
    if not grade_lookup:
        grade_lookup = { 
            score<=100.: "A",
            score<92.5: "A-",
            score<89.5: "B+",
            score<86.5: "B",
            score<82.5: "B-",
            score<79.5: "C+",
            score<76.5: "C",
            score<72.5: "C-",
            score<69.5: "D+",
            score<66.5: "D",
            score<62.5: "D-",
            score<59.5: "F",
        }

    return grade_lookup.get(True, "Invalid Score")


if __name__ == "__main__":


    if len(sys.argv)>1:
        args = sys.argv[1:]
        letter_grades = []

        for arg in args:
            letter_grades.append(get_letter_grade(float(arg)))

        print(" ".join(letter_grades))

    else:
        while True:
            try:
                score = float(input("Enter Score: "))
                break
            except ValueError:
                print("Invalid number entered; try again.")

        get_letter_grade(score)
