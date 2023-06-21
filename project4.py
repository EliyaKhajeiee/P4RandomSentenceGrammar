# project4.py
#
# ICS 33 Spring 2023
# Project 4: Still Looking for Something
import file_organizer_py


def main() -> None:
    path = input()
    number_of_lines = input()
    start_var = input()
    count = 1
    while count <= int(number_of_lines):
        boo = file_organizer_py.file_organizer(start_var,path,number_of_lines)
        boo.parse_stuff()
        boo.process_each_one()
        first_gen_rule_obj = boo.printing_my_stuff()
        boo.take_given_rule(first_gen_rule_obj)
        count +=1
        print()


if __name__ == '__main__':
    main()
