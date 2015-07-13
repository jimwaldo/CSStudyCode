#!/usr/bin/env python
"""
Take a .csv file containing information about students, the classes they have taken, and
their grades, and produce a file with the same information that is de-identified in a most
basic way, by having the names of the students deleted and the HUID for the student replaced
by a randomly generated number.
"""
__author__ = 'waldo'

import sys, csv, random, pickle


class student_rec:
    """
    A student record object, used to read, manipulate, and write the information about an individual student

    There are three methods-- one that fills in the record from the .csv file, one that gets a random
    number (unique for each student, but consistent for the same student) for the anonymous id, and one
    that sequences the record for writing to a new .csv file
    """
    def __init__(self, init_list):
        """
        Create a student record object from the list obtained from the .csv file
        :param init_list: A line from the .csv file
        :return: None
        """
        self.id = init_list[0]
        self.s_name = init_list[1]
        self.gender = init_list[2]
        self.concen = init_list[3]
        self.end_date = init_list[4]
        self.program = init_list[5]
        self.course_name = init_list[6]
        self.acad_year = init_list[7]
        self.term = init_list[8]
        self.faculty_name = init_list[9]
        self.grade = init_list[10]
        self.primary_conc = init_list[11]
        self.secondary_conc = init_list[12]
        self.anon_id = ''

    def print_list(self):
        """
        Create a list that can be written to a .csv file of the anonymized student record
        :return: a list with the anonymized id and no name, but all other information
        """
        p_list = [self.anon_id,
                  self.gender,
                  self.concen,
                  self.end_date,
                  self.program,
                  self.course_name,
                  self.acad_year,
                  self.term,
                  self.faculty_name,
                  self.grade,
                  self.primary_conc,
                  self.secondary_conc
                  ]
        return p_list

    def get_anon_id(self, id_dict, id_set):
        """
        Add an anonymous id for a student record, using one that already exists if there is such

        Checks to see if this student already has an anonymous id, and if so returns that. If not,
        create one by generating a random number between 1 and 1,000,000 that hasn't been used before
        as an id. This value is placed in the anon_id field of the student record
        :param id_dict: a dictionary with HUID as key and anonymized ID as value
        :param id_set: a set with randomized ids to insure that the same id is not reused
        :return: None
        """
        if self.id in id_dict:
            self.anon_id = id_dict[self.id]
        else:
            self.anon_id = random.randint(1, 1000000)
            while self.anon_id in id_set:
                self.anon_id = random.randint(1, 1000000)
            id_dict[self.id] = self.anon_id
            id_set.add(self.anon_id)
        return None


def main(fname, outname):
    """
    Driver for the overall script

    Taking the names of the input and output files, generate a de-identified version of the input file
    and write to the output file. Both input and output are .csv files. The form of de-identification
    is pretty primative; all that occurs is that names are removed and the HUID is replaced by a
    random number.
    :param fname: name of a .csv file containing the student records to be de-identified
    :param outname: name of a .csv file to create and write the de-identified data to
    :return: None
    """
    fin = open(fname, 'rW')
    fout = open(outname, 'w')
    cin = csv.reader(fin)
    cout = csv.writer(fout)
    head_in = cin.next()
    head_out = head_in
    head_out.pop(1)
    cout.writerow(head_out)

    id_dict = {}
    id_set = set()

    for l in cin:
        sr = student_rec(l)
        sr.get_anon_id(id_dict, id_set)
        cout.writerow(sr.print_list())

    pout = open('idDictPickle', 'w')
    pickle.dump(id_dict, pout)

if __name__ == '__main__':
    in_name = sys.argv[1]
    out_name = sys.argv[2]
    main(in_name, out_name)
