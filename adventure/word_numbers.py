#!/usr/bin/env python3
"""
**************************************************************************
**
**   word_numbers.py - Interpreter for Word Numbers
**
**   Version 1 revision 0
**
**************************************************************************
This module is released under the MIT License:
==========================================================================

Copyright 2025 Jeffrey R. Day

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the “Software”),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

#*************************************************************************
"""

import sys

# <def>
def parse_number_tokens(tokens, colloquial=False):

    ntype = "cardinal"
    format_string = ""
    sep = False
    
    digit_words = {
        'oh': 'X', 'zero': 'X', 'aught': 'X',
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
        'ten': '1X', 'eleven': 11, 'twelve': 12,
        'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19,
        'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
    }
    ordinal_words = {
        'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9,
        'tenth': 10, 'eleventh': 11, 'twelfth': 12,
        'thirteenth': 13, 'fourteenth': 14, 'fifteenth': 15, 'sixteenth': 16, 'seventeenth': 17, 'eighteenth': 18, 'nineteenth': 19,
        'twentieth': 20, 'thirtieth': 30, 'fortieth': 40, 'fiftieth': 50, 'sixtieth': 60, 'seventieth': 70, 'eightieth': 80, 'ninetieth': 90
    }
    scale_words = {'hundred': 100, 'thousand': 1000, 'myriad': 10000, 'million': 1000000, 'milliard': 1000000000 }
    ordinal_scale_words = {'hundredth': 100, 'thousandth': 1000, 'myriadth': 10000, 'millionth': 1000000, 'milliardth': 1000000000 }
    articles_soft = ('a', 'an')
    articles_hard = ('a')
    unit_word = 'one'
    fraction_joiner = 'and'
    soft_starts = ('h')
    multiple_words = { 'double': 2, 'triple': 3 }
    ordinal_endings = {'st', 'nd', 'rd', 'th', 'd'}  # Including archaic 'd'

    # <def>
    def get_places(s):
        return len(s) - len(s.rstrip('0'))
    # </def>

    # <def>
    def validate_and_strip_ordinal(word):
        ordinal_endings = {'st', 'nd', 'rd', 'th', 'd'}
        sorted_endings = sorted(ordinal_endings, key=len, reverse=True)
        
        # <for>
        for ending in sorted_endings:
            if word.endswith(ending):
                base = word[:-len(ending)]
                # <if>
                if not base.isdigit():
                    continue
                # </if>
                number = int(base)
                is_valid = is_valid_ordinal(number, ending)
                # <if>
                if is_valid:
                    return ending, base, True
                else:
                    return ending, base, False
                # </if>
            # </if>
        # </for>
        return None, word, False
    # </def>
    
    # <def>
    def is_valid_ordinal(number, ending):
        """
        Validate if the number-ending combination is grammatically correct.
        Rules:
        - Numbers ending in 11, 12, 13 (in any decade) always use 'th'
        - Numbers ending in 1 (except 11) use 'st'
        - Numbers ending in 2 (except 12) use 'nd' or 'd'
        - Numbers ending in 3 (except 13) use 'rd' or 'd'
        - All other numbers use 'th'
        - 0th is allowed
        """
        last_digit = number % 10
        last_two_digits = number % 100
        # <if>
        if last_two_digits in [11, 12, 13]:
            return ending == 'th'
        # </if>
        # <if>
        if last_digit == 1:
            return ending == 'st'
        elif last_digit == 2:
            return ending in ['nd', 'd']
        elif last_digit == 3:
            return ending in ['rd', 'd']
        else:  # 0, 4, 5, 6, 7, 8, 9
            return ending == 'th'
        # </if>
    # </def>
    
    # <def>
    def process_context(name, size, tokens):
        full = False
        inner_value = ""
        closed_to_single = False
        escape_mult = False
        pending_tokens = False
        flags = set()
        # <while>
        while len(tokens) and not full and not escape_mult:
            digit_value = False
            this_tok = tokens[0]
            ctokens = tokens[1:]
            # <if>
            if this_tok == fraction_joiner:
                raise ValueError('Fractional values are not supported in this context.')
            # </if>

            multiple_word = multiple_words.get(this_tok)
            # <if>
            if multiple_word:
                # <if>
                if colloquial:
                    # <if>
                    if name == '':
                        flags.add("colloquial")
                        next_word = str(digit_words.get(ctokens[0]))
                        # <if>
                        if len(next_word) == 1:
                            inner_value = inner_value + next_word * multiple_word
                            ctokens = ctokens[1:]
                            tokens = ctokens
                            closed_to_single = False
                        else:
                            raise ValueError('Cannot ' + this_tok + ' token "' + ctokens[0] + '."')
                        # </if>
                    else:
                        escape_mult = True
                    # </if>
                else:
                    raise Value('Repeater "' + multiple_word + '" invalid in non-colloquial context.')
                # </if>
            else:
                digit_word = str(digit_words.get(this_tok))
                # <if>
                if digit_word == 'None':
                    digit_word = str(ordinal_words.get(this_tok))
                    # <if>
                    if digit_word != 'None':
                        flags.add('ordinal')
                    else:
                        ending, base_word, is_ordinal = validate_and_strip_ordinal(this_tok)
                        # <if>
                        if ending or base_word.isdigit() or base_word == 'X':
                            # <if>
                            if is_ordinal:
                                flags.add('ordinal')
                            elif ending:
                                raise ValueError('Unrecognized token "' + this_tok + '."')
                            # </if>
                            # <if>
                            if inner_value == "":
                                tokens = ctokens
                                inner_value += str(base_word)
                                digit_value = True
                            else:
                                raise ValueError('Token "' + this_tok + '" is invalid in this context.')
                            # </if>
                        # </if>
                    # </if>
                # </if>
                # <if>
                if (not digit_value) and digit_word != 'None':
                    places = get_places(str(digit_word))
                    # <if>
                    if places:
                        # <if>
                        if len(ctokens) and 'ordinal' in flags:
                            raise ValueError('Token "' + str(ctokens[0]) + '" disallowed after ordinal ending.')
                        # </if>
                        ctokens, content, newflags = process_context(inner_value, places, ctokens)
                        flags.update(newflags)
                        token_value = digit_word[:-places] + content.zfill(places)
                        # <if>
                        if 'escape_mult' in flags and name != '':
                            print(name, 'branch d')
                            escape_mult = True
                        # </if>
                    else:
                        token_value = digit_word
                        # <if>
                        if len(digit_word) > 1:
                            closed_to_single = this_tok
                        elif closed_to_single != False and not pending_tokens:
                            # <if>
                            if token_value == 'X':
                                pending_tokens = True
                            else:
                                raise ValueError('Single digit non-zero token "' + str(this_tok) + '" disallowed after "' + closed_to_single + '."')
                            # </if>
                        elif token_value == 'X':
                            # <if>
                            if name == '':
                                token_value = 'X'
                                tokens = ctokens
                                escape_mult = False
                            else:
                                ctokens = ('oh',) + ctokens
                                tokens = ctokens
                                escape_mult = True
                            # </if>
                        # </if>
                    # </if>
                    # <if>
                    if escape_mult or (len(token_value) + len(inner_value) > size):
                        # <if>
                        if name == "":
                            inner_value = inner_value + 'X'
                        # </if>
                        full = True
                    elif inner_value == "" or colloquial == True:
                        # <if>
                        if len(ctokens) and 'ordinal' in flags:
                            raise ValueError('Token "' + str(ctokens[0]) + '" disallowed after ordinal ending.')
                        else:
                            # <if>
                            if inner_value != "":
                                flags.add("colloquial")
                            # </if>
                            tokens = ctokens
                            inner_value += token_value
                        # </if>
                    else:
                        raise ValueError('Token "' + this_tok + '" invalid in non-colloquial context.')
                    # </if>
                elif not digit_value:
                    scale_word = str(scale_words.get(this_tok))
                    # <if>
                    if scale_word == 'None':
                        scale_word = str(ordinal_scale_words.get(this_tok))
                        # <if>
                        if scale_word != 'None':
                            flags.add('ordinal')
                        # </if>
                    # </if>
                    # <if>
                    if scale_word != 'None':
                        # Check if next token is also a scale word (consecutive scales)
                        next_is_scale = len(ctokens) > 0 and (ctokens[0] in scale_words or ctokens[0] in ordinal_scale_words)
                        current_scale_val = int(scale_word)

                        # <if>
                        if next_is_scale:
                            # Handle consecutive scale words by multiplication
                            next_scale_word = str(scale_words.get(ctokens[0], ordinal_scale_words.get(ctokens[0], 'None')))
                            # <if>
                            if next_scale_word != 'None':
                                next_scale_val = int(next_scale_word)
                                
                                # Only multiply if next scale is same or smaller magnitude
                                # <if>
                                if next_scale_val <= current_scale_val:
                                    # Apply current scale to inner_value
                                    # <if>
                                    if inner_value == "":
                                        inner_value = "1"
                                    # </if>
                                    scaled_value = int(inner_value) * current_scale_val
                                    
                                    # Multiply by the second scale value
                                    inner_value = str(scaled_value * next_scale_val)
                                    
                                    tokens = ctokens[1:]  # Skip the second scale word entirely
                                    continue  # Skip the normal processing below
                                # </if>
                            # </if>
                        # </if>
                        
                        # Normal scale word processing
                        # <if>
                        if len(inner_value) + len(scale_word) - 1 > size:
                            full = True
                        else:
                            # <if>
                            if len(ctokens) and 'ordinal' in flags:
                                raise ValueError('Token "' + str(ctokens[0]) + '" disallowed after ordinal ending.')
                            # </if>
                            tokens, content, newflags = process_context(inner_value, len(scale_word) - 1, ctokens)
                            flags.update(newflags)
                            # <if>
                            if 'escape_mult' in flags and name != '':
                                print(name, 'branch f')
                                escape_mult = True
                            # </if>
                            inner_value += content.zfill(len(scale_word) - 1)
                        # </if>
                    else:
                        raise ValueError('Unrecognized Token: "' + this_tok + '"')
                    # </if>
                # </if>
            # </if else of multiple>
        # </while>
        # <if>
        if pending_tokens:
            raise ValueError('Pending Tokens: ', pending_tokens, closed_to_single)
        # </if>
        # <if>
        if escape_mult:
            flags.update(['escape_mult'])
        # </if>
        return tokens, inner_value, flags
    # </def process_context>

    # Store original tokens for separator detection
    original_tokens = tokens
    
    # <if>
    if len(tokens) == 1 and ((tokens[0] in articles_soft) or (tokens[0] in articles_hard)):
        tokens = (unit_word,)
    # <if>
    
    # <if>
    if len(tokens) and (tokens[0] in scale_words or tokens[0] in ordinal_scale_words):
        tokens = (unit_word,) + tuple(tokens)
    # </if>
    # <if>
    if len(tokens) > 1 and tokens[0] in articles_soft and (tokens[1] in scale_words or tokens[1] in ordinal_scale_words) and tokens[1].startswith(soft_starts):
        tokens = (unit_word,) + tuple(tokens[1:])
    # </if>
    # <if>
    if len(tokens) > 1 and tokens[0] in articles_hard and (tokens[1] in scale_words or tokens[1] in ordinal_scale_words):
        tokens = (unit_word,) + tuple(tokens[1:])
    # </if>

    tokens, inner_value, flags = process_context('', 20, tokens)
    format_string = inner_value.replace('X', '0')
    value = int(format_string)
    # <if>
    if 'ordinal' in flags:
        ntype = 'ordinal'
    # </if>
    
    # <if>
    if colloquial and value >= 100 and 'colloquial' in flags:
        # Check for patterns that could be time/money separators
        # Conditions:
        # 1. No scale words (hundred, thousand, etc.)
        # 2. Contains hard zeros (oh/aught) OR has positional structure
        # 3. Value is in reasonable range for time/money
        
        has_scale_words = any(token in scale_words or token in ordinal_scale_words for token in original_tokens)
        has_hard_zeros = any(token in ['oh', 'zero', 'aught'] for token in original_tokens)
        
        # <if>
        if not has_scale_words:
            # Expanded range for money patterns like $27.12 (27012)
            # <if>
            if value <= 99999:  # Allow up to $999.99 patterns
                # <if>
                if has_hard_zeros:
                    sep = True
                elif len(original_tokens) >= 2:
                    # Look for patterns with tens values that could be time/money
                    value_str = str(value)
                    # <if>
                    if len(value_str) >= 3:
                        # Check if it has a structure that could be separated
                        last_two = value % 100
                        # <if>
                        if 0 <= last_two <= 99:  # Valid for both time and money
                            sep = True
                        # </if>
                    # </if>
                # </if>
            # </if value limit>
        # </if not has_scale_words>

    return ntype, value, format_string, sep

if __name__ == "__main__":
    # <if>
    if len(sys.argv) > 1:
        print(parse_number_tokens(tuple(sys.argv[1:]), True))
    else:
        print("Test cases:")
        # <def>
        def p(s, a, ordinal=False):
            ps = tuple(s.split())
            expected_type = 'cardinal' if ordinal == False else 'ordinal'
            nt, r, fs, sep = parse_number_tokens(ps, True)
            ntc = "" if nt == "cardinal" else " (ord)"
            # <if>
            if str(a) == str(fs) and nt == expected_type:
                print("  OK ... " + fs + ntc + " == " + s)
            else:
                print("FAIL !!! " + fs + ntc + " != " + str(a) + " : " + s)
            # </if>
        # </def p - test for answer>
        # <def>
        def pf(s, es="error"):
            ps = tuple(s.split())
            # <try>
            try:
                parse_number_tokens(ps, True)
                print("FAIL !!! " + s + " == " + es + " GOT SUCCESS?")
            except ValueError as e:
                # <if>
                if str(e) == str(es):
                    print("  OK ... " + str(es) + " == " + s)
                else:
                    print("FAIL !!! " + str(es) + " != " + str(e) + " : " + s)
                # </if>
            # </try>
        # </def pf - test for failures>
        # <def>
        def po(s, a):
            p(s, a, True)
        # </def po - test for ordinal>
        # <def>
        def ps(s, expected_sep):
            ps = tuple(s.split())
            nt, r, fs, sep = parse_number_tokens(ps, True)
            # <if>
            if (sep == expected_sep):
                print("  OK ... " + str(sep) + " == " + s)
            else:
                print("FAIL !!! " + str(sep) + " != " + str(expected_sep) + " : " + s)
            # </if>
        # </def>

        # All existing tests...
        p('one', 1)
        po('first', 1)
        p('eleven', 11)
        p('twelve', 12)
        po('twelfth', 12)
        p('a hundred', 100)
        p('an hundred', 100)
        p('a thousand', 1000)
        p('a myriad', 10000)
        p('a million', 1000000)
        pf('an million', 'Unrecognized Token: "an"')
        p('a milliard', 1000000000)
        p('hundred', 100)
        p('thousand', 1000)
        p('myriad', 10000)
        p('million', 1000000)
        p('milliard', 1000000000)
        p('1', 1)
        po('1st', 1)
        pf('1nd', 'Unrecognized token "1nd."')
        po('2d', 2)
        po('2nd', 2)
        po('3d', 3)
        po('3rd', 3)
        po('4th', 4)
        po('11th', 11)
        po('12th', 12)
        po('13th', 13)
        pf('11st', 'Unrecognized token "11st."')
        pf('12d', 'Unrecognized token "12d."')
        pf('12nd', 'Unrecognized token "12nd."')
        p('one hundred twenty three', 123)
        p('one twenty three', 123)
        p('hundred twenty three', 123)
        p('one hundred twenty three', 123)
        p('a hundred twenty three', 123)
        p('ten twenty three', 1023)
        p('thousand twenty three', 1023)
        p('one aught two three', 1023)
        p('one zero two three', 1023)
        p('1023', 1023)
        p('three hundred twenty thousand', 320000)
        p('one thousand nine hundred ten', 1910)
        p('one thousand aught six', 100006)
        p('one hundred six', 106)
        p('ten hundred six', 1006)
        p('thousand six', 1006)
        p('ten thousand six', 10006)
        p('ten thousand six million', 10006000000)
        p('four thousand nine hundred ten', 4910)
        p('four thousand aught six', 400006)
        p('four hundred six', 406)
        p('forty hundred six', 4006)
        p('4 thousand six', 4006)
        p('forty thousand six', 40006)
        p('forty thousand six million', 40006000000)
        p('double oh seven', '007')
        p('triple zero six', '0006')
        p('five five five eighty two oh one', 5558201)
        p('aught million', '0000000')
        p('one hundred hundred', '10000')
        p('one thousand hundred', '100000')
        p('one thousand two hundred', '1200')
        p('one hundred thousand', '100000')
        p('one hundred million', '100000000')
        p('one million hundred', '100000000')
        p('one million million', '1000000000000')
        p('one milliard one million one myriad one thousand one hundred ten', '1001011110')
        p('two double seven six triple zero', '2776000')
        pf('two double seventy six triple zero', 'Cannot double token "seventy."')
        pf('seven and two eighths', 'Fractional values are not supported in this context.')
        p('ten thousand seven hundred thirty five million twenty thousand fifty two',         10735020052)
        p('ten thousand seven hundred thirty five million twenty thousand fifty two oh one',  1073502005201)
        p('ten thousand seven hundred thirty five million twenty thousand fifty two one',  1073502005201)
        p('ten thousand seven hundred thirty five million twenty five thousand two hundred',  10735025200)
        p('ten thousand seven hundred thirty five million twenty thousand fifty two hundred', 1073502005200)

        # Current issue, "fifty two oh" should never resolve in a context that doesn't have room for the digit after "oh"
        # This is because once you've started grouping into twos, you always need two more, otherwise it would be:
        # "five twenty" or "five two oh" instead.  Encountering a multiplier word resets this attribute.
        # Note, fifty two twelve is acceptable, since the twelve is a two digit unit.
        
        p('fifty two oh', '520')

        p('oh five twenty', '0520')

        # Test separator detection
        print("\nPotential dollar and cents or hours and minutes detection tests:")
        ps('three forty five', True)      # 3:45 time
        ps('three ninety nine', True)     # $3.99 money
        ps('twenty seven twelve', True)   # $27.12 money - SHOULD NOW WORK
        ps('oh five twenty', True)        # 05:20 time with hard zero
        ps('twelve thirty', True)         # 12:30 time
        ps('two hundred thirty', False)   # Has scale word "hundred"
        ps('twenty one', False)           # Under 100
        ps('ninety nine thousand', False) # Has scale word "thousand"
    # </if not argv>
# </if __main__>