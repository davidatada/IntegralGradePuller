import integral_scraper
import grades_reporter
import pandas as pd

course = 'course_AS_PURE'
group = 'ma2022'
modules = ['PS1','PS2', 'S1', 'S2', 'Q1', 'Q2', 'D1']
grades_table = grades_reporter.get_grade_report(course, group, modules)
course_table = integral_scraper.get_course_info(course)
#print(tb['PS1']['nneka.nonyelson@ada.ac.uk'])
print(grades_reporter.missing_grades_table(grades_table, course_table))
print(grades_reporter.all_missing_grades_report(grades_table, course_table))
# print(grades_reporter.missing_grades_table(tb, integral_scraper.get_course_info('course_AS_PURE')))
