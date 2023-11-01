# Script for sorting an input file. Sorted result will be written to an output file. Encoding is UFT-08.
#
import csv
import os
import time
# from delimitertranslater import DelimiterTranslater


class DataSorter:
    def sort_file(self, input_file, output_file, number_of_header_lines=0, number_of_trailer_lines=0, sort_on_columns_list=None, delimiter=',', quotechar=None):
        #
        if not os.path.exists(input_file):
            raise Exception("Input file doesn't exists: ", input_file)
        #
        print("input_file: ", input_file)
        print("output_file: ", output_file)
        print("number_of_header_lines: ", number_of_header_lines)
        print("trailer _line_numbers: ", number_of_trailer_lines)
        print("sort_on_columns_list: ", sort_on_columns_list)
        print("delimiter: ", delimiter)
        print("quotechar: ", quotechar)
        #
        number_of_records_input_file = 0
        with open(input_file) as input_file_row_count:
            number_of_records_input_file = sum(1 for line in input_file_row_count)
        #
        number_of_header_lines = int(number_of_header_lines)
        number_of_trailer_lines = int(number_of_trailer_lines)
        #
        if number_of_records_input_file < number_of_header_lines + number_of_trailer_lines:
            raise Exception("The number of records in the input file is less than the declared number of header and trailer lines.")
        #
        number_of_sort_columns = 0
        #
        if sort_on_columns_list is None or sort_on_columns_list == []:
            sort_on_columns_int_list = None
        else:
            sort_on_columns_int_list = [eval(i) for i in sort_on_columns_list]
            number_of_sort_columns = len(sort_on_columns_list)
            print("number_of_sort_columns: ", number_of_sort_columns)
        #
        if number_of_header_lines == 0 and number_of_trailer_lines == 0:
            # Only data lines
            with open(input_file, mode='rt', encoding='utf-8') as input_file, open(output_file, mode='w', newline='', encoding='utf-8') as output_file:
                time.sleep(1)
                input_data = csv.reader(input_file, delimiter=delimiter, quotechar=quotechar)
                output_data = csv.writer(output_file, delimiter=delimiter, quotechar=quotechar)
                #
                if not input_data:
                    raise Exception("Input file is empty.")
                #
                # Sort all records.
                sorted_records = sorted(input_data, key=lambda elem: elem[0])
                #
                for row in sorted_records:
                    output_data.writerow(row)
            #
        else:
            # Header or/and trailer lines and data lines
            with open(input_file, mode='rt', encoding='utf-8') as input_file:
                time.sleep(1)
                if len(delimiter) == 1:
                    input_data = list(csv.reader(input_file, delimiter=delimiter, quotechar=quotechar))
                else:
                    input_data = list(csv.reader((line.replace(delimiter, chr(255)) for line in input_file), delimiter=chr(255), quotechar=quotechar))
                #
            with open(output_file, mode='w', newline='', encoding='utf-8') as output_file:
                time.sleep(1)
                if len(delimiter) == 1:
                    output_data = csv.writer(output_file, delimiter=delimiter, quotechar=quotechar)
                else:
                    translater = DelimiterTranslater(output_file, chr(255), delimiter)
                    output_data = csv.writer(translater, delimiter=chr(255), quotechar=quotechar)
                #
                if not input_data:
                    raise Exception("Input file is empty.")
                #
                # Header or trailer line present
                line_nr = 0
                data_text = []
                trailer_text = []
                #
                for row in input_data:
                    line_nr += 1
                    if number_of_header_lines != 0 and line_nr <= number_of_header_lines:
                        # A header line.
                        output_data.writerow(row)
                    elif number_of_trailer_lines != 0 and line_nr > number_of_records_input_file - number_of_trailer_lines:
                        # A trailer line.
                        trailer_text.append(row)
                    else:
                        # A data line.
                        data_text.append(row)
                #
                match number_of_sort_columns:
                    case 0:
                        sorted_data_text = sorted(data_text, key=lambda column: (column[0]))
                    case 1:
                        a = sort_on_columns_int_list[0]
                        sorted_data_text = sorted(data_text, key=lambda column: (column(a)))
                    case 2:
                        a = sort_on_columns_int_list[0]
                        b = sort_on_columns_int_list[1]
                        sorted_data_text = sorted(data_text, key=lambda column: (column[a], column[b]))
                        # sorted_data_text= data_text.sort(key=lambda row: (row[a], row[b]))
                    case 3:
                        a = sort_on_columns_int_list[0]
                        b = sort_on_columns_int_list[1]
                        c = sort_on_columns_int_list[2]
                        sorted_data_text = sorted(data_text, key=lambda column: (column[a], column[b], column[c]))
                    case 4:
                        a = sort_on_columns_int_list[0]
                        b = sort_on_columns_int_list[1]
                        c = sort_on_columns_int_list[2]
                        d = sort_on_columns_int_list[3]
                        sorted_data_text = sorted(data_text, key=lambda column: (column[a], column[b], column[c], column[d]))
                    case 5:
                        a = sort_on_columns_int_list[0]
                        b = sort_on_columns_int_list[1]
                        c = sort_on_columns_int_list[2]
                        d = sort_on_columns_int_list[3]
                        e = sort_on_columns_int_list[4]
                        sorted_data_text = sorted(data_text, key=lambda column: (column(a), column[b], column[c], column[d], column[e]))
                    case _:
                        print("Too many columns selected for sorting.")
                #
                for row in sorted_data_text:
                    output_data.writerow(row)

                for row in trailer_text:
                    output_data.writerow(row)


class DelimiterTranslater(object):
    def __init__(self, f, old, new):
        self.f = f
        self.old = old
        self.new = new

    def write(self, s):
        self.f.write(s.replace(self.old, self.new))

    def close(self):
        self.f.close()

    def flush(self):
        self.f.flush()