'''
LINGUANA v1.2
Linguistics Analyser
Author: @037

Application designed to take apart bodies of text and do comparative linguistics analysis.
Purpose is to draw conclusions if two bodies of text share authorship.
'''
import os
import sys
import hashlib
from itertools import islice
from autocorrect import Speller

DEBUG = 0
TOP_LIST = 10
N_TERMS = 3
STYLE_FINGERPRINT = []
LOGO = '''
                                                   __
                                              _.-~`  `~-.
                  _.--~~~---,.__          _.,;; .   -=(@'`\\
               .-`              ``~~~~--~~` ';;;       ____)
            _.'            '.              ';;;;;    '`_.'
         .-~;`               `\           ' ';;;;;__.~`
       .' .'          `'.     |           /  /;''
        \\/      .---\'''``)   /'-._____.--'\  \\
  jgs  _/|    (`        /  /`              `\ \__
',    `/- \   \      __/  (_                /-\-\-`
  `;'-..___)   |     `/-\-\-`
    `-.       .'
       `~~~~``
 ██▓     ██▓ ███▄    █   ▄████  █    ██  ▄▄▄       ███▄    █  ▄▄▄      
▓██▒    ▓██▒ ██ ▀█   █  ██▒ ▀█▒ ██  ▓██▒▒████▄     ██ ▀█   █ ▒████▄    
▒██░    ▒██▒▓██  ▀█ ██▒▒██░▄▄▄░▓██  ▒██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██  ▀█▄  
▒██░    ░██░▓██▒  ▐▌██▒░▓█  ██▓▓▓█  ░██░░██▄▄▄▄██ ▓██▒  ▐▌██▒░██▄▄▄▄██ 
░██████▒░██░▒██░   ▓██░░▒▓███▀▒▒▒█████▓  ▓█   ▓██▒▒██░   ▓██░ ▓█   ▓██▒
░ ▒░▓  ░░▓  ░ ▒░   ▒ ▒  ░▒   ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░   ▒ ▒  ▒▒   ▓▒█░
░ ░ ▒  ░ ▒ ░░ ░░   ░ ▒░  ░   ░ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░░   ░ ▒░  ▒   ▒▒ ░
  ░ ░    ▒ ░   ░   ░ ░ ░ ░   ░  ░░░ ░ ░   ░   ▒      ░   ░ ░   ░   ▒   
    ░  ░ ░           ░       ░    ░           ░  ░         ░       ░  ░
                            Author: @037

'''

def wpl_analyser(body, top=10):
    '''
    Function is designed to record number of words per line
    based on number of hits
    '''
    
    wpl = {}
    for lines in body:
        word_count = len(lines)
        try:
            if(wpl[word_count] > 0):
                wpl[word_count] = wpl[word_count] + 1
        except KeyError:
            wpl[word_count] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(wpl, key=wpl.get, reverse=True):
        sorted_dict[key] = wpl[key]
    print(f"[*] Top {top} words per line hits in body:")
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        print(f"[*] {word}: {sorted_dict[word]}")
        conjoined_string += str(word) + ":"
        # We take the N-th rank word count hits
        if i == top:
            break
        else:
            i += 1
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("W_" + conjoined_checksum)
    print(f"[*] Top {top} WPL fingerprint: {conjoined_checksum}")
    print()


def cpw_analyser(body, top=10):
    '''
    Function is designed to record number of characters per word
    based on number of hits
    '''
    
    cpw = {}
    for lines in body:
        for word in lines:
            word_length = len(word)
            try:
                if(cpw[word] > 0):
                    cpw[word_length] = cpw[word_length] + 1
            except KeyError:
                cpw[word_length] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(cpw, key=cpw.get, reverse=True):
        sorted_dict[key] = cpw[key]
    print(f"[*] Top {top} char per word hits in body:")
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        print(f"[*] {word}: {sorted_dict[word]}")
        conjoined_string += str(word) + ":"
        # We take the N-th rank word frequent
        if i == top:
            break
        else:
            i += 1
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("C_" + conjoined_checksum)
    print(f"[*] Top {top} CPW fingerprint: {conjoined_checksum}")
    print()



def n_gram_analyser(body, n=3, top=10):
    '''
    Function is designed to take in an integer factorial to count from
    Enumerates N-gram word pairings in a body of text
    '''
    def chunk_list(input_list, n, shift=0):
        shifted_list = input_list[shift:] + input_list[:shift]
        return [shifted_list[i:i+n] for i in range(0, len(input_list), n)]
    
    for i in range(n, 1, -1):
        print(f"[*] Taking {i}-gram of processed word list...")
        word_frequency = {}
        for j in range(0, i):
            for lines in body:
                chunked_lines = chunk_list(lines, i, j)
                for chunk in chunked_lines:
                    words = ''
                    for word in chunk:
                        words += word + ':'
                    try:
                        if(word_frequency[words] > 0):
                            word_frequency[words] = word_frequency[words] + 1
                    except KeyError:
                        word_frequency[words] = 1
        # Sorting using a for loop
        sorted_dict = {}
        for key in sorted(word_frequency, key=word_frequency.get, reverse=True):
            sorted_dict[key] = word_frequency[key]
        print(f"[*] Top {top} {i}-gram factorial words in body:")
        x = 0
        conjoined_string = ''
        for word in sorted_dict:
            print(f"[*] {word}: {sorted_dict[word]}")
            conjoined_string += word
            # We take the N-th rank word frequent
            if x == top:
                break
            else:
                x += 1
        conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
        STYLE_FINGERPRINT.append("N_" + conjoined_checksum)
        print(f"[*] Top {top} {i}-gram factorial words fingerprint: {conjoined_checksum}")
        print()

def spelling_analyser(body, top=10):
    '''
    Function that takes in a body of text
    returns a list of spelling mistakes
    '''
    
    misspelling_frequency = {}
    for lines in body:
        for word in lines:
            correction = spell(word)
            if correction != word:
                try:
                    if(misspelling_frequency[word] > 0):
                        misspelling_frequency[word] = misspelling_frequency[word] + 1
                except KeyError:
                    misspelling_frequency[word] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(misspelling_frequency, key=misspelling_frequency.get, reverse=True):
        sorted_dict[key] = misspelling_frequency[key]
    print(f"[*] Top {top} misspelled words in body:")
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        print(f"[*] {word}: {sorted_dict[word]}")
        conjoined_string += word
        # We take the N-th rank word frequent
        if i == top:
            break
        else:
            i += 1
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("S_" + conjoined_checksum)
    print(f"[*] Top {top} misspelled words fingerprint: {conjoined_checksum}")
    print()

def word_frequency_analyser(body, top=10):
    '''
    Function that takes in a body of text
    returns every word used and its frequency
    '''
    
    word_frequency = {}
    for lines in body:
        for word in lines:
            try:
                if(word_frequency[word] > 0):
                    word_frequency[word] = word_frequency[word] + 1
            except KeyError:
                word_frequency[word] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(word_frequency, key=word_frequency.get, reverse=True):
        sorted_dict[key] = word_frequency[key]
    print(f"[*] Top {top} encountered words in body:")
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        print(f"[*] {word}: {sorted_dict[word]}")
        conjoined_string += word
        # We take the N-th rank word frequent
        if i == top:
            break
        else:
            i += 1
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("F_" + conjoined_checksum)
    print(f"[*] Top {top} used words fingerprint: {conjoined_checksum}")
    print()


if __name__ == "__main__":
    '''
    Main function for running multi threads for each analyser
    '''
    print(LOGO)
    print("[*] LINGUANA v1.2 - Linguistics Analyser")
    spell = Speller(lang='en')
    if(len(sys.argv) > 2 and sys.argv[1] == '--input'):
        fn = sys.argv[2]
        if os.path.exists(fn):
            if(DEBUG == 1):
                print(os.path.basename(fn))
            # file exists
            with open(fn, "rb") as target:
                # Using this area to show a preview of the file being taken apart
                i = 0
                print("------[BEGIN FILE PREVIEW]------")
                for line in target:
                    print(line.decode('utf-8').rstrip())
                    if(i == 10):
                        break
                    else:
                        i += 1
                print("------[END FILE PREVIEW]------")
            with open(fn, "rb") as target:
                delimiter_list = input("[*] List characters to split words by (default is space): ")
                delimiter_list = delimiter_list.split(" ")
                if(len(delimiter_list) == 1 and delimiter_list[0] == ''):
                    delimiter_list = [' ']
                parsed_words = []
                print("[*] Processing words... Please wait.")
                for line in target:
                    line = line.decode('utf-8').rstrip()
                    if(line == ''):
                        pass
                    else:
                        if(DEBUG == 1):
                            print(f"[*] Line: {line}")
                        for delimiter in delimiter_list:
                            if(DEBUG == 1):
                                print(f"[*] Delimiter: {delimiter}")
                            line = line.replace(delimiter, ' ')
                        parsed_words.append(line.split(' '))
                if(DEBUG == 1):
                    print("[*] Processed word list: ")
                    print(parsed_words)
                    for word in parsed_words:
                        print(word)
                print()
                print("------[BEGIN WPL HITS ANALYSER]------")
                wpl_analyser(parsed_words, top=10)
                print("------[BEGIN CPW HITS ANALYSER]------")
                cpw_analyser(parsed_words, top=10)
                print("------[BEGIN WORD FREQUENCY ANALYSER]------")
                word_frequency_analyser(parsed_words, TOP_LIST)
                print("------[BEGIN N-GRAM ANALYSER]------")
                n_gram_analyser(parsed_words, N_TERMS, TOP_LIST)
                print("------[BEGIN SPELLING ANALYSER]------")
                spelling_analyser(parsed_words, TOP_LIST)
                print("------[BEGIN LINGUANA FINGERPRINT]------")
                STYLE_FINGERPRINT.sort()
                for fp in STYLE_FINGERPRINT:
                    print(fp)
                print("------[END LINGUANA FINGERPRINT]------")
                if(len(sys.argv) > 4 and sys.argv[3] == '--output'):
                    fo = sys.argv[4]
                    with open(fo, 'w') as file_output:
                        # write variables using repr() function
                        file_output.write("------[BEGIN LINGUANA FINGERPRINT]------" + '\n')
                        STYLE_FINGERPRINT.sort()
                        for fp in STYLE_FINGERPRINT:
                            file_output.write(fp + '\n')
                        file_output.write("------[END LINGUANA FINGERPRINT]------" + '\n')
    else:
        print(f"[*] Scan file: {sys.argv[0]} --input PATH")
        print(f"[*] Save results: {sys.argv[0]} --input PATH --output PATH")