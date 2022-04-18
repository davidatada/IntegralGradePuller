import integral_scraper
import grades_reporter
import pandas as pd

course = 'course_AS_STATISTICS'
group = 'ma2123'
stats_modules = ['D2','D3','P1', 'P2', 'B1','H1','H2']
mech_modules = ['K1','K2','K3','V1']
pure_modules = ['PS1','PS2','S1','S2','Q1','Q2','E1','E2','C1','C2','T1','T2','T3','P1','P2','D1','D2','D4','I1','I2','G1']
#modules = ['T1','T2','F1','F2','F3','D1','D2','D3','TF1','A2','TI1','TI2','FD1','FD2','FD3','I1','I2', 'I3', 'I4']
grades_table = grades_reporter.get_grade_report(course, group, stats_modules)
course_table = integral_scraper.get_course_info(course)
#print(tb['PS1']['nneka.nonyelson@ada.ac.uk'])
missing = grades_reporter.missing_grades_table(grades_table, course_table)
#missing.to_csv('puregrades.csv')
print(grades_reporter.all_missing_grades_report(grades_table, course_table))
# print(grades_reporter.missing_grades_table(tb, integral_scraper.get_course_info('course_AS_PURE')))
