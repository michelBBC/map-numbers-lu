# -*- coding: utf-8 -*-
# TODO:
# Eiffler Reegel
# Dausend not eendausend
# Gegrennt gouf de Päiperleksgaart 1989. 2011 huet Yolande Coop d\'Gestioun iwwerholl.
# 1m10

import logging

def load_number_map(path):
    units = {}
    tens = {}
    scales = {}
    with open(path) as fin:
        for line in fin.readlines():
            if line.startswith('#'): continue
            key, val = line.split()
            if len(key) < 3:
                if int(key) < 20:
                    units[key] = val
                else:
                    tens[key] = val
            else:
                scales[key] = val
    return units, tens, scales

def load_months(path):
    with open(path) as fin:
        months = [line.strip() for line in fin.readlines() if not line.startswith('#')]
    assert len(months) == 12, f"Got {len(months)} instead of 12."
    return months

def strip_punctuation(in_txt):
    return ''.join(_ for _ in filter(str.isdigit, in_txt))

def map_number(txt, units, tens, scales, months, decimal_sep=','):
    """
    Given a string of digits (with punctuation) replace the digits with
    the text version of that number.

    :param txt, str
    :returns number_in_words, str, None
    """
    logging.debug(txt)
    number_in_words = ""
    # Check if date
#     print(txt, is_date(txt, months))
    if is_date(txt, months):
        number_in_words = date2txt(txt, units, tens, scales, months)
        return number_in_words

    # Separate out decimals
    txt_split = txt.split(decimal_sep)
    # Get digits
    unit = strip_punctuation(txt_split[0])
    dec = strip_punctuation(txt_split[1]) if len(txt_split) > 1 else None


    number_in_words += int2txt(unit, units, tens, scales)
    if dec is not None:
        number_in_words += f" komma {int2txt(dec, units, tens, scales)}"

    return number_in_words

def int2txt(txt, units, tens, scales):
    """ Convert digits into written-out numbers."""
    output = ""
    triplets = [txt[::-1][i:i+3][::-1] for i in range(0, len(txt), 3)][::-1]
    logging.debug(triplets)
    trip_len = len(triplets)
    for triplet in triplets:
        if trip_len > 4:
            current_scale = str(int(1E12))
        elif trip_len > 3:
            current_scale = str(int(1E9))
        elif trip_len > 2:
            current_scale = str(int(1E6))
        elif trip_len > 1:
            current_scale = str(int(1E3))
        else:
            current_scale = None
        output += parse_triplet(triplet, units, tens, scales)
        if current_scale is not None:
            output += f"{scales[current_scale]} "
            trip_len -= 1
            current_scale = None

    return output.strip()

def is_date(txt, months):
    """ Guess if input `txt` is a date.
    """
    tokens = txt.split()
    if len(tokens) == 1: tokens = tokens[0].split('.')
    # Does the string contain a month?
    if len(set(tokens) & set(months)) == 1:
        # Attempt to parse??
        return True
    # Does it contain a year?
    elif len(tokens[-1]) == 4 and len(tokens) in [1, 3]:
        # Realistically, we'll probably talk about the last few centuries
        try:
            day = int(tokens[0].replace(".",""))
            if len(tokens) == 3 and (day < 1 or day > 30):
                return False
        except ValueError:
            logging.error(f"Cannot convert {tokens[0]} to number.")
            return False
        try:
            year = int(tokens[-1].replace(".",""))
            if year < 2300 and year > 1099:
                return True
        except ValueError:
            logging.error(f"Cannot convert {tokens[-1]} to number.")
            return False
    return False

def to_ordinal(txt, suffix_list=['d','zeg','h','n','r']):
    """ Convert written-out number from cardinal to ordinal.
    """
    if list(filter(txt.endswith, suffix_list)) != []:
        return txt+'sten'
    else:
        return txt+'ten'


def date2txt(txt, units, tens, scales, months):
    """ Convert a date into fully written-out format.
    """
    output = ""
    tokens = txt.split()
    if len(tokens) == 1: tokens = tokens[0].split('.')
    if len(tokens) == 1:
        # Could be just the years
        return parse_quartet(tokens[0], units, tens, scales).strip()
    if len(tokens) != 3:
        raise ValueError(f"'{txt}' does not convert to correct format.")
    # day
    if '.' in tokens[0]:
        tokens[0] = strip_punctuation(tokens[0])
    output = parse_triplet(tokens[0], units, tens, scales)
    # Now add cardinal suffix to last token
    tmp = output.split()
    try:
        output = " ".join(_ for _ in
                          tmp[:-1] + [to_ordinal(tmp[-1])]
                          ) + " "
    except IndexError as e:
        print(tmp, output)
        raise(e)
    # month: convert if number, otherwise just copy
    try:
        output += f"{months[int(tokens[1])-1]} "
    except ValueError:
        output += f"{tokens[1]} "
    except IndexError as e:
        print(f"Failed to convert ''{txt}''")
        return txt

    # year
    logging.debug(tokens[2])
    output += parse_quartet(tokens[2], units, tens, scales)

    return output.strip()

def parse_triplet(triplet, units, tens, scales):
    output = ""
    triplet_len = len(triplet)
    logging.debug(triplet_len)
    for digit in triplet:
        if triplet_len == 0:
            break
        if digit == '0':
            triplet_len -= 1
        elif triplet_len > 2:
            output += f"{units[digit]} {scales['100']} "
            triplet_len -= 1
        elif triplet_len == 2:
            if int(digit) < 2:
                output += f"{units[triplet[-2:]]} "
                triplet_len -= 2
            else:
                output += f"{tens[digit+'0']} "
                triplet_len -= 1
        else:
            # Annoying exception to deal with one and twenty in lux
            tmp = output.split()
            if len(tmp) == 0:
                output += f"{units[digit]}"
            else:
                output = " ".join(_ for _ in
                                  tmp[:-1] + [f"{units[digit]} a"] + tmp[-1:]
                                  ) + " "
            triplet_len -= 1
    return output

def parse_quartet(txt, units, tens, scales):
    """ Parse quartet of numbers (useful for years).
    """
    output = ""
    if int(txt) < 1100 or int(txt) > 1999:
        current_scale = str(int(1E3))
        doublets = [txt[0], txt[1:]]
        # output += parse_triplet(doublet, units, tens, scales)
    else:
    # Special case:
        doublets = [txt[::-1][i:i+2][::-1] for i in range(0, len(txt), 2)][::-1]
        current_scale = None
    logging.debug(doublets)
    logging.debug(doublets, current_scale)
    d_len = len(doublets)
    for doublet in doublets:
        if d_len > 1 and current_scale is None:
            current_scale = str(int(1E2))
        output += parse_triplet(doublet, units, tens, scales)

        if current_scale is not None:
            output += f"{scales[current_scale]} "
            d_len -= 1
            current_scale = None
    return output

def pandas_map_numbers(match, units, tens, scales, months, decimal_sep=','):
    """ Pandas apply function wrapper for 'map_numbers' function.
    """
    logging.debug(match.groups())
    txt = match.group(1)
    out = map_number(txt, units, tens, scales, months, decimal_sep=',')
    return out.strip() + ' '


def pandas_int2txt(match, units, tens, scales):
    """ Pandas apply function wrapper for 'int2txt' function.
    """
    logging.debug(match.groups())
    txt = match.group(1)
    out = int2txt(txt, units, tens, scales)
    return out.strip() + ' '


if __name__ == '__main__':
    print("Number mapping utility.\n\nSome examples:\n")
    units, tens, scales = load_number_map('../constants/cardinal.txt')
    print(f"302,450 --> {int2txt(strip_punctuation('302,450'), units, tens, scales)}")

    months = load_months('../constants/months.txt')
    test_date = '2. Juli 1999'
    print(f"Is '{test_date}' a date?  {is_date(test_date, months)}")
    print(f"Fully written out: {date2txt(test_date, units, tens, scales, months)}")
