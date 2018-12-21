# To run using the command line enter a command in this format: python3 gpa_calc.py "A- A B"

import argparse

grades = ['B', 'B+', 'B-', 'B+', 'B+', 'B', 'A-', 'B+', 'B+']

gpa_scale = {
    'A': 4,
    'B': 3,
    'C': 2,
    'D': 1,
}

def gpa_calc(grades=grades, gpa_scale = gpa_scale, inc = 0.3, round_gpa = 2):
    # Calculates GPA based on UChicago grading scale
    # Input should be a list of strings 
    
    total = 0
    for grade in grades:
        letter = grade.strip('+-').upper()
        score = gpa_scale[letter]
        if "+" in grade:
            score += inc
        if "-" in grade:
            score -= inc
        total += score

    if round_gpa:
        return round((total/len(grades)), 2)
    else:
        return (total/len(grades))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get GPA')
    parser.add_argument('grades')
    args = parser.parse_args()
    print(gpa_calc(args.grades.split()))
    
