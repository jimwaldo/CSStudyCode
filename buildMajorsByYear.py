#!/usr/bin/env python
import sys, csv, pickle

class g_balance(object):

    def __init__(self, gender):
        if gender == 'M':
            self.male = 1
            self.female = 0
        else:
            self.male = 0
            self.female = 1

    def inc_gender(self, gender):
        if gender == 'M':
            self.male += 1
        else:
            self.female += 1

    def total_male(self):
        return self.male

    def total_female(self):
        return self.female

def main(fin, fout):
    year_dict = {}
    fin.next()
    for row in fin:
        if (row[11] == 'Computer Science') or (row[12] == 'Computer Science'):
            if row[7] in year_dict:
                year_dict[row[7]].inc_gender(row[2])
            else:
                year_dict[row[7]] = g_balance(row[2])

    pickle.dump(year_dict, fout)

    for key in sorted(year_dict):
        print key, 'males =', year_dict[key].total_male(), 'females =', year_dict[key].total_female()

if __name__ == '__main__':
    fname_in = sys.argv[1]
    fin = csv.reader(open(fname_in, 'rU'))
    fout = open(sys.argv[2], 'w')
    main(fin, fout)