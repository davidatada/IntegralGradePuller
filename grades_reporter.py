import pandas as pd
import integral_scraper
import io
import numpy as np

# relabels a column in table to use the code rather than full name
def get_test_code(label, topics):
  if label[:11]=='Quiz: Test ':
    code = label[11:-7]
    return code
  return label

# turns the grade report from integral into a nicely formatted dataframe
def get_grade_report(course_name, group_name, modules):
    grades=pd.read_csv(io.StringIO(integral_scraper.download_grades(course_name,group_name,modules).decode('utf-8')), index_col='Username', na_values=['-'])
    grades.drop(['Last downloaded from this course'], axis=1, inplace=True)
    grades.rename(columns=lambda x: get_test_code(x,integral_scraper.get_course_info(course_name)), inplace=True)
    #print(grades.dtypes)
    return grades

# generate a list of the test grades a student is missing
def missing_grades_from_uname(uname, grade_table):
    return missing_grades_from_row(grade_table.loc[uname], grade_table)

def missing_grades_from_row(row, grade_table):
    return [code for code in grade_table.columns if pd.isna(row[code])]


def missing_grades_report(missing, course_lookup, separator='\n'):
    return separator.join([course_lookup['Topic'][code] for code in missing])


# def all_missing_grades_report(grade_table, course_lookup, separator='\n'):
#     report = ''
#     for row in grade_table:
#         report += str(row)
#         # report.append()
#     return report

def missing_grades_table(grade_table, course_lookup, text=True, separator='<br>'):
    mgrades = grade_table.copy()
    mgrades['missing'] = mgrades.apply(lambda x: missing_grades_from_row(x,mgrades), axis=1)
    if text:
        mgrades['missing'] = mgrades['missing'].apply(lambda x: missing_grades_report(x, course_lookup, separator=separator))

    return mgrades[['First name', 'Surname', 'missing']]

def formatted_missing_grades(row, grade_table):
    return '{} {}\n\t{}'.format(row['First name'], row['Surname'], row['missing'])

def all_missing_grades_report(grade_table, course_lookup):
    t = missing_grades_table(grade_table, course_lookup, separator='\n\t')
    return '\n\n'.join(t.apply(lambda r: formatted_missing_grades(r, grade_table), axis=1).tolist())
