

import csv, sys, random, cPickle


class student_rec_14:

    def __init__(self, init_list):
        self.id = init_list[0]
        self.gender = init_list[1]
        self.course_name = init_list[2]
        self.course_id = init_list[3]
        self.grade = init_list[4]
        self.grad_date = init_list[5]
        self.acad_year = init_list[6]
        self.term = init_list[7]
        self.program = init_list[8]
        self.primary_conc = init_list[9]
        self.secondary_conc = init_list[10]
        self.faculty_name = init_list[11]
        self.faculty_second = init_list[12]
        self.relative_need = init_list[13]
        self.percent_aid = init_list[14]
        self.anon_id = ''

    def get_print_list(self):
        p_list = [self.anon_id,
                  self.gender,
                  self.primary_conc,
                  self.grad_date,
                  self.program,
                  self.course_name,
                  self.acad_year,
                  self.term,
                  self.faculty_name,
                  self.grade,
                  self.primary_conc,
                  self.secondary_conc,
                  self.relative_need,
                  self.percent_aid
                  ]
        return p_list

    def get_anon_id(self, id_dict, id_set):
        if self.id in id_dict:
            self.anon_id = id_dict[self.id]
        else:
            self.anon_id = random.randint(1,1000000)
            while self.anon_id in id_set:
                self.anon_id = random.randint(1, 1000000)
            id_dict[self.id] = self.anon_id
            id_set.add(self.anon_id)

        return None

def main(csv_in, csv_out, id_dict):
    head_in = student_rec_14(csv_in.next())
    csv_out.writerow(head_in.get_print_list())

    id_set = set()
    for l in csv_in:
        s_rec = student_rec_14(l)
        s_rec.get_anon_id(id_dict, id_set)
        csv_out.writerow(s_rec.get_print_list())

    return None

if __name__ == '__main__':
    f_in = open(sys.argv[1], 'rU')
    csv_in = csv.reader(f_in)

    id_in = open(sys.argv[3], 'r')
    id_dict = cPickle.load(id_in)
    id_in.close()

    f_out = open(sys.argv[2], 'w')
    csv_out = csv.writer(f_out)

    main(csv_in, csv_out, id_dict)

    id_out = open(sys.argv[3], 'w')
    cPickle.dump(id_dict, id_out)

    id_out.close()
    f_out.close()
    f_in.close()




