import ebcdic
import codecs
import re

import sys
import argparse
import csv
import math
from array import array
import json


class CobolPatterns:
    opt_pattern_format = "({})?"
    row_pattern_base = r"^(?P<level>\d{2})\s+(?P<name>\S+)"
    row_pattern_occurs = r"\s+OCCURS (?P<occurs>\d+) TIMES"
    row_pattern_indexed_by = r"\s+INDEXED BY\s(?P<indexed_by>\S+)"
    row_pattern_redefines = r"\s+REDEFINES\s+(?P<redefines>\S+)"
    row_pattern_pic = r"\s+PIC\s+(?P<pic>\S+)"
    row_pattern_comp = r"\s+COMP" ## new pattern for client A
    row_pattern_binary = r"\s+BINARY" ## new pattern for client A
    row_pattern_end = r"\.$"
    row_pattern = re.compile(
        row_pattern_base
        + opt_pattern_format.format(row_pattern_redefines)
        + opt_pattern_format.format(row_pattern_occurs)
        + opt_pattern_format.format(row_pattern_indexed_by)
        + opt_pattern_format.format(row_pattern_pic)
        + opt_pattern_format.format(row_pattern_comp)
        + opt_pattern_format.format(row_pattern_binary)        
        + row_pattern_end
    )
    pic_pattern_repeats = re.compile(r"(.)\((\d+)\)")
    pic_pattern_float = re.compile(r"S?[9Z]*[.V][9Z]+")
    pic_pattern_integer = re.compile(r"S?[9Z]+")


# Parse the pic string
def parse_pic_string(pic_str):
    # Expand repeating chars
    while True:
        match = CobolPatterns.pic_pattern_repeats.search(pic_str)
        if not match:
            break
        expanded_str = match.group(1) * int(match.group(2))
        pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)
    # Match to types
    if CobolPatterns.pic_pattern_float.match(pic_str):
        data_type = "Float"
    elif CobolPatterns.pic_pattern_integer.match(pic_str):
        data_type = "Integer"
    else:
        data_type = "Char"

    # Handle signed
    if pic_str[0] == "S":
        data_type = "Signed " + data_type
        pic_str = pic_str[1:]

    # Handle precision
    decimal_pos = 0

    if "V" in pic_str:
        decimal_pos = len(pic_str[pic_str.index("V") + 1 :])
        pic_str = pic_str.replace("V", "")

    return {"type": data_type, "length": len(pic_str), "precision": decimal_pos}


# Cleans the COBOL by converting the cobol informaton to single lines
def clean_cobol(lines):
    holder = []
    output = []

    for row in lines:
        row = row[6:72].rstrip()

        if row == "" or row[0] in ("*", "/"):
            continue

        holder.append(row if len(holder) == 0 else row.strip())

        if row[-1] == ".":
            output.append(" ".join(holder))

            holder = []

    if len(holder) > 0:
        print(
            "[WARNING] probably invalid COBOL - found unfinished line: ",
            " ".join(holder),
        )

    return output


"""
Parses the COBOL
 - converts the COBOL line into a dictionarty containing the information
 - parses the pic information into type, length, precision 
 - handles redefines
"""
def parse_cobol(lines):
    output = []

    intify = ["level", "occurs"]

    # All in 1 line now, let's parse
    for row in lines:
        # print("Processing ", row)
        # print("=====================")
        bcd_type_indicator = False
        comp_type_indicator = False
        binary_type_indicator = False        
        occurs3_indicator = False
        if " USAGE COMP-3" in row:
            row = row.replace(" USAGE COMP-3", "")
            bcd_type_indicator = True
        if " COMP" in row:
            # row = row.replace(" COMP", "")
            comp_type_indicator = True
        if "  BINARY" in row:
            # row = row.replace(" BINARY", "")
            binary_type_indicator = True
            
        # if 'OCCURS 3 TIMES' in row:
        if "OCCURS " in row and " TIMES" in row:
            # row = row.replace('OCCURS 3 TIMES', '')
            # row = row.replace('                OCCURS 3 TIMES', '')
            # occurs3_index = row.find('OCCURS 3 TIMES')
            occurs3_index = row.find("OCCURS ")
            whitespace_index = occurs3_index - 1
            while whitespace_index >= 0 and row[whitespace_index] == " ":
                whitespace_index = whitespace_index - 1

            times_index = row.find(" TIMES", occurs3_index)
            times_number = row[occurs3_index + len(" TIMES") : times_index]
            # print("times number is ", times_number)

            # string_to_replace = ' '* (occurs3_index - whitespace_index -1) + 'OCCURS 3 TIMES'
            string_to_replace = (
                " " * (occurs3_index - whitespace_index - 1)
                + row[occurs3_index : times_index + len(" TIMES")]
            )
            # print("string to replace is ", string_to_replace)

            row = row.replace(string_to_replace, "")
            # print("Found OCCURS 3 TIMES and new row is ", row)
            # occurs3_indicator = True
            occurs3_indicator = times_number

        match = CobolPatterns.row_pattern.match(row.strip())

        if not match:
            print("Found unmatched row", row.strip())
            continue

        match = match.groupdict()
        match["occurs3"] = occurs3_indicator
        for i in intify:
            match[i] = int(match[i]) if match[i] is not None else None

        if match["pic"] is not None:
            match["pic_info"] = parse_pic_string(match["pic"])
            match["pic_info"]["isBCD"] = bcd_type_indicator
            match["pic_info"]["isComp"] = comp_type_indicator
            match["pic_info"]["isBinary"] = binary_type_indicator

        if match["redefines"] is not None:
            # Find item that is being redefined.
            try:
                redefinedItemIndex, redefinedItem = [
                    (index, item)
                    for index, item in enumerate(output)
                    if item["name"] == match["redefines"]
                ][0]

                related_group = get_subgroup(
                    redefinedItem["level"], output[redefinedItemIndex + 1 :]
                )

                output = (
                    output[:redefinedItemIndex]
                    + output[redefinedItemIndex + len(related_group) + 1 :]
                )

                match["redefines"] = None
            except IndexError:
                print(
                    "Could not find the field to be redefined ({}) for row: {}".format(
                        match["redefines"], row.strip()
                    )
                )

        output.append(match)

    return output


# Helper function
# Gets all the lines that have a higher level then the parent_level until
# a line with equal or lower level then parent_level is encountered
def get_subgroup(parent_level, lines):
    output = []

    for row in lines:
        if row["level"] > parent_level:
            output.append(row)
        else:
            return output

    return output


def denormalize_cobol(lines):
    return handle_occurs(lines, 1)


# Helper function
# Will go ahead and denormalize the COBOL
# Beacuse the OCCURS are removed the INDEXED BY will also be removed
def handle_occurs(lines, occurs, level_diff=0, name_postfix=""):
    output = []

    for i in range(1, occurs + 1):

        skipTill = 0
        new_name_postfix = name_postfix if occurs == 1 else name_postfix + "-" + str(i)

        for index, row in enumerate(lines):
            if index < skipTill:
                continue

            new_row = row.copy()

            new_row["level"] += level_diff

            # Not needed when flattened
            new_row["indexed_by"] = None

            if row["occurs"] is None:
                # First time occurs is just 1, we don't want to add _1 after *every* field
                new_row["name"] = row["name"] + new_name_postfix
                # + "-" + str(i) if occurs > 1 else row['name'] + name_postfix

                output.append(new_row)

            else:
                if row["pic"] is not None:
                    # If it has occurs and pic just repeat the same line multiple times
                    new_row["occurs"] = None

                    for j in range(1, row["occurs"] + 1):
                        row_to_add = new_row.copy()

                        # First time occurs is just 1, we don't want to add _1 after *every* field
                        row_to_add["name"] = (
                            row["name"] + new_name_postfix + "-" + str(j)
                        )
                        # + "-" + str(i) + "-" + str(j) if occurs > 1 else row['name'] + name_postfix + "-" + str(j)

                        output.append(row_to_add)

                else:
                    # Get all the lines that have to occur
                    occur_lines = get_subgroup(row["level"], lines[index + 1 :])

                    # Calculate the new level difference that has to be applied
                    new_level_diff = level_diff + row["level"] - occur_lines[0]["level"]

                    output += handle_occurs(
                        occur_lines, row["occurs"], new_level_diff, new_name_postfix
                    )

                    skipTill = index + len(occur_lines) + 1

    return output


"""
Clean the names.

Options to:
 - strip prefixes on names
 - enforce unique names
 - make database safe names by converting - to _
"""


def clean_names(
    lines, ensure_unique_names=False, strip_prefix=False, make_database_safe=False
):
    names = {}

    for row in lines:
        if strip_prefix:
            row["name"] = row["name"][row["name"].find("-") + 1 :]

            if row["indexed_by"] is not None:
                row["indexed_by"] = row["indexed_by"][row["indexed_by"].find("-") + 1 :]

        if ensure_unique_names:
            i = 1
            while (row["name"] if i == 1 else row["name"] + "-" + str(i)) in names:
                i += 1

            names[row["name"] if i == 1 else row["name"] + "-" + str(i)] = 1

            if i > 1:
                row["name"] = row["name"] + "-" + str(i)

        if make_database_safe:
            row["name"] = row["name"].replace("-", "_")

    return lines


def process_cobol(lines):
    # return clean_names(denormalize_cobol(parse_cobol(clean_cobol(lines))), True, True, True)
    return denormalize_cobol(parse_cobol(clean_cobol(lines)))


# Prints a Copybook compatible file
def print_cobol(lines):
    output = []

    default_padding = " " * 7

    levels = [0]

    for row in lines:
        row_output = []
        # print(row)
        if row["level"] > levels[-1]:
            levels.append(row["level"])
        else:
            while row["level"] < levels[-1]:
                levels.pop()

        row_output.append((len(levels) - 1) * "  ")
        row_output.append("{0:02d}  ".format(row["level"]))
        row_output.append(row["name"])

        if row["indexed_by"] is not None:
            row_output.append(" INDEXED BY " + row["indexed_by"])

        if row["occurs"] is not None:
            row_output.append(" OCCURS {0:04d} TIMES".format(row["occurs"]))

        if row["pic"] is not None:
            row_output.append(" PIC " + row["pic"])

        row_output.append(".")

        tot_length = 0
        max_data_length = 66
        outp = default_padding

        for data in row_output:

            if len(outp) + len(data) + 1 > max_data_length:
                # Makes rows 80 chars
                outp += (80 - len(outp)) * " "

                output.append(outp)

                # Start the following line with an extra padding
                outp = default_padding + (len(levels) - 1) * "  " + "    "

            outp += data

        outp += (80 - len(outp)) * " "
        output.append(outp)

    # print("Output line is ", "\n".join(output))
    return "\n".join(output)

def get_len_for_comp_binary(elem_length):
    # print('Calculate length for binary or comp. length is ' + str(elem_length))
    if elem_length>=1 and elem_length <=4:
        return 2
    elif elem_length>=5 and elem_length<=9:
        return 4
    elif elem_length>=10 and elem_length<=18:
        return 8
    else:
        return 0
    
def decode_copybook_file(filename):
    # output_filename = filename + '_process.cbl'
    # with open(output_filename,"a", encoding="utf-8") as output:
    cobol_struc = []
    row_length = 0
    # name_prefix = NameStack()
    previous_occurs3 = 0
    previous_level = 0
    with open(filename, "r") as f:
        # rows = process_cobol(f.readlines())
        # print(rows)
        for row in process_cobol(f.readlines()):

            if row["level"] >= previous_level:
                # name_prefix.push(row["name"])
                previous_level = row["level"]
            else:
                previous_occurs3 = 0  # reset to False if it is not a child node
            if row["level"] < previous_level:
                # name_prefix.pop()
                previous_level = row["level"]

            if (
                "occurs3" in row and row["occurs3"]
            ):  ### repeat for all items in the same group as the group is repeated!!!!
                previous_occurs3 = row["occurs3"]  # True
            if "pic" in row and row["pic"] != None:
                # print("Current row")
                # print(row)

                if previous_occurs3:
                    # print(previous_occurs3)
                    for index in range(int(previous_occurs3)):
                        # element = {'name': str(name_prefix) + '.' + row['name'] + '_' + str(index+1), 'type': row['pic_info']['type']}
                        element = {
                            "name": row["name"] + "_" + str(index + 1),
                            "type": row["pic_info"]["type"],
                        }
                        element["occurs3"] = previous_occurs3  # True
                        ### calculation should consider COMP3 and occur3
                        elem_length = row["pic_info"]["length"]
                        if "isBCD" in row["pic_info"] and row["pic_info"]["isBCD"]:
                            elem_length = int(math.ceil((elem_length + 1) / 2))
                        elif "isComp" in row["pic_info"] and row["pic_info"]["isComp"]:
                            # print('Process Comp')
                            elem_length = get_len_for_comp_binary(elem_length)

                        elif "isBinary" in row["pic_info"] and row["pic_info"]["isBinary"]:
                            # print('Process Binary')
                            elem_length = get_len_for_comp_binary(elem_length)
                            
                        # if 'occurs3' in element and element['occurs3']:
                        #     elem_length = elem_length *3
                        # element['occurs_times'] = element['occurs3']
                        element["length"] = elem_length
                        if "Signed Float" in row["pic_info"]["type"]:
                            element["precision"] = row["pic_info"]["precision"]
                        # row_length = row_length + row['pic_info']['length']
                        row_length = row_length + elem_length
                        cobol_struc.append(element)
                else:
                    # element = {'name': str(name_prefix) + '.' + row['name'], 'type': row['pic_info']['type']}
                    element = {"name": row["name"], "type": row["pic_info"]["type"]}
                    ### calculation should consider COMP3 and occur3
                    elem_length = row["pic_info"]["length"]
                    if "isBCD" in row["pic_info"] and row["pic_info"]["isBCD"]:
                        elem_length = int(math.ceil((elem_length + 1) / 2))
                    elif "isComp" in row["pic_info"] and row["pic_info"]["isComp"]:
                        # print('Process Comp')
                        element["tag"] = 'Comp'
                        elem_length = get_len_for_comp_binary(elem_length)
                    elif "isBinary" in row["pic_info"] and row["pic_info"]["isBinary"]:
                        # print('Process Binary')
                        element["tag"] = 'Binary'
                        elem_length = get_len_for_comp_binary(elem_length)                        
                    # if 'occurs3' in element and element['occurs3']:
                    #     elem_length = elem_length *3
                    # element['occurs_times'] = element['occurs3']
                    element["length"] = elem_length
                    if "Signed Float" in row["pic_info"]["type"]:
                        element["precision"] = row["pic_info"]["precision"]
                    # row_length = row_length + row['pic_info']['length']
                    row_length = row_length + elem_length
                    cobol_struc.append(element)

        # print('total length per row is ')
        # print (row_length)
        return row_length, cobol_struc


def convert_copybook_file(filename, output_filename):
    # output_filename = filename + '_process.cbl'
    with open(output_filename, "a", encoding="utf-8") as output:
        with open(filename, "r") as f:
            output_string = print_cobol(parse_cobol(clean_cobol(f.readlines())))
            output.write(output_string)

def unpack_hex_array(p):
    v = float(0)
    # print('p[0] = ')
    # print(p[0])
    # print(type(p[0]))
    if p[0] == '0xff': ### this is a negative number to process in a special way
        for hex in p:
            v = v*256 + 255 - int(hex, 0)
        v = v + 1
        v = -v
        return int(v)
    else:
        for hex in p:
            v = v*256 + int(hex, 0)
        return int(v)

def unpack_number(p):
    """Unpack a COMP-3 number."""
    a = array("B", p)
    v = float(0)

    # For all but last digit (half byte)
    for i in a[:-1]:
        v = (v * 100) + (((i & 0xF0) >> 4) * 10) + (i & 0xF)

    # Last digit
    i = a[-1]
    v = (v * 10) + ((i & 0xF0) >> 4)

    # Negative/Positve check.
    if (i & 0xF) == 0xD:
        v = -v

    # Decimal points are determined by a COBOL program's PICtrue clauses, not
    # the data on disk.
    return int(v)


def custom_encoder(my_string):
    return "".join([i if ord(i) < 128 else " " for i in my_string])

def sanitize_col_name_for_database(name):
    """
    Column names in database:
    Must contain only letters (a-z, A-Z), numbers (0-9), or underscores (_)
    Must begin with a letter or underscore
    Must be less than the maximum length of 251 characters. 

    """
    new_name = name.replace("-", "_")[:251]
    return new_name


def convert_cobol_file(
    copybook_filename, data_filename, output_filename, config_filename, codepage, debug=False
):
    # decode_ebcdic_file(datafile, processed_data_file)
    (row_length, cobol_struc) = decode_copybook_file(copybook_filename)
    headers = [sanitize_col_name_for_database(item["name"]) for item in cobol_struc]
    if debug:
        print("total length per row is ")
        print(row_length)
        print("Cobol strucuture to consume is ")
        print(cobol_struc)
    with open(output_filename, "w", newline="") as csvfile, open(
        config_filename
    ) as json_file, open(data_filename, "rb") as data_file:
        config = json.load(json_file)
        if debug:
            print(config)

        csvwriter = csv.writer(
            csvfile,
            delimiter=config["csv_config"]["delimiter"],
            quoting=config["csv_config"]["quoting_level"],
            quotechar=config["csv_config"]["quote_char"],
        )
        csvwriter.writerow(headers)

        current_pos = 0
        eof = False
        while not eof:
            data_row = []
            for item in cobol_struc:
                data_read = data_file.read(item["length"])
                if not data_read:
                    eof = True
                    break
##Enhancements
                if "tag" in item and item["tag"] == "Binary":
                    integer_array = [hex(data_read[i]) for i in range(item["length"])]
                    int_val = unpack_hex_array(integer_array)
                    data_row.append(int_val)                    
                elif "tag" in item and item["tag"] == "Comp":
                    integer_array = [hex(data_read[i]) for i in range(item["length"])]
                    int_val = unpack_hex_array(integer_array)
                    float_val = float(int_val) / pow(10, item["precision"])
                    data_row.append(float_val)
## END TEST
                # if "Signed Integer" in item["type"]:
                elif "Signed Integer" in item["type"]:                    
                    data_row.append(unpack_number(data_read))
                elif "Signed Float" in item["type"]:
                    # print("Processing float ", item)
                    integer_array = [hex(data_read[i]) for i in range(item["length"])]
                    # print(item["type"], item["name"], integer_array)
                    int_val = unpack_number(data_read)
                    float_val = float(int_val) / pow(10, item["precision"])
                    data_row.append(float_val)
                    # print(int_val, float_val)
                else:
                    original_str = codecs.decode(data_read, codepage).strip()
                    new_str = "".join(custom_encoder(original_str))
                    data_row.append(new_str)
                current_pos = current_pos + item["length"]
            if debug:
                print(data_row)
            if len(data_row) > 2:
                csvwriter.writerow(data_row)
