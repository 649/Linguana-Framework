'''
LINGUANA v1.4
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
from _thread import start_new_thread

DEBUG = 1
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

def wpl_analyser(status, thread_id):
    '''
    Function is designed to record number of words per line
    based on number of hits
    '''
    thread_print = "------[BEGIN WPL HITS ANALYSER]------" + '\n'
    wpl = {}
    for lines in parsed_words:
        word_count = len(lines)
        try:
            if(wpl[word_count] > 0):
                wpl[word_count] += 1
        except KeyError:
            wpl[word_count] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(wpl, key=wpl.get, reverse=True):
        sorted_dict[key] = wpl[key]
    thread_print += f"[*] Top {TOP_LIST} words per line hits in body:" + '\n'
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        thread_print += f"[*] {word}-word lines: {sorted_dict[word]} hits" + '\n'
        conjoined_string += str(word) + "|"
        # We take the N-th rank word count hits
        if i == TOP_LIST:
            break
        else:
            i += 1
    if(DEBUG == 1):
        thread_print += f"[*] Plaintext top WPL fingerprint: {conjoined_string}" + '\n'
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("W_" + conjoined_checksum)
    thread_print += f"[*] Top {TOP_LIST} WPL fingerprint: {conjoined_checksum}" + '\n'
    print(thread_print + '\n')
    status[thread_id] = 1

def cpw_analyser(status, thread_id):
    '''
    Function is designed to record number of characters per word
    based on number of hits
    '''
    thread_print = "------[BEGIN CPW HITS ANALYSER]------" + '\n'
    cpw = {}
    for lines in parsed_words:
        for word in lines:
            word_length = len(word)
            try:
                if(cpw[word_length] > 0):
                    cpw[word_length] += 1
            except KeyError:
                cpw[word_length] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(cpw, key=cpw.get, reverse=True):
        sorted_dict[key] = cpw[key]
    thread_print += f"[*] Top {TOP_LIST} char per word hits in body:" + '\n'
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        thread_print += f"[*] {word}-char words: {sorted_dict[word]} hits" + '\n'
        conjoined_string += str(word) + "|"
        # We take the N-th rank char count hits
        if i == TOP_LIST:
            break
        else:
            i += 1
    if(DEBUG == 1):
        thread_print += f"[*] Plaintext top CPW fingerprint: {conjoined_string}" + '\n'
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("C_" + conjoined_checksum)
    thread_print += f"[*] Top {TOP_LIST} CPW fingerprint: {conjoined_checksum}" + '\n'
    print(thread_print + '\n')
    status[thread_id] = 1

def n_gram_analyser(status, thread_id):
    '''
    Function is designed to take in an integer factorial to count from
    Enumerates N-gram word pairings in a body of text
    '''
    def chunk_list(input_list, n, shift=0):
        shifted_list = input_list[shift:] + input_list[:shift]
        return [shifted_list[i:i+n] for i in range(0, len(input_list), n)]
    thread_print = "------[BEGIN N-GRAM ANALYSER]------" + '\n'
    for i in range(N_TERMS, 1, -1):
        thread_print += f"[*] Taking {i}-gram of processed word list..." + '\n'
        word_frequency = {}
        for j in range(0, i):
            for lines in parsed_words:
                chunked_lines = chunk_list(lines, i, j)
                for chunk in chunked_lines:
                    words = ''
                    for word in chunk:
                        words += word + '|'
                    try:
                        if(word_frequency[words] > 0):
                            word_frequency[words] += 1
                    except KeyError:
                        word_frequency[words] = 1
        # Sorting using a for loop
        sorted_dict = {}
        for key in sorted(word_frequency, key=word_frequency.get, reverse=True):
            sorted_dict[key] = word_frequency[key]
        thread_print += f"[*] Top {TOP_LIST} {i}-gram factorial words in body:" + '\n'
        x = 0
        conjoined_string = ''
        for word in sorted_dict:
            thread_print += f"[*] {word}: {sorted_dict[word]}" + '\n'
            conjoined_string += word + '|'
            # We take the N-th rank word frequent
            if x == TOP_LIST:
                break
            else:
                x += 1
        if(DEBUG == 1):
            thread_print += f"[*] Plaintext top {i}-gram factorial words fingerprint: {conjoined_string}" + '\n'
        conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
        STYLE_FINGERPRINT.append("N_" + conjoined_checksum)
        thread_print += f"[*] Top {TOP_LIST} {i}-gram factorial words fingerprint: {conjoined_checksum}" + '\n'
    print(thread_print + '\n')
    status[thread_id] = 1

def spelling_analyser(status, thread_id):
    '''
    Function that takes in a body of text
    returns a list of spelling mistakes
    '''
    thread_print = "------[BEGIN SPELLING ANALYSER]------" + '\n'
    misspelling_frequency = {}
    for lines in parsed_words:
        for word in lines:
            correction = spell(word)
            if correction != word:
                try:
                    if(misspelling_frequency[word] > 0):
                        misspelling_frequency[word] += 1
                except KeyError:
                    misspelling_frequency[word] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(misspelling_frequency, key=misspelling_frequency.get, reverse=True):
        sorted_dict[key] = misspelling_frequency[key]
    thread_print += f"[*] Top {TOP_LIST} misspelled words in body:" + '\n'
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        thread_print += f"[*] {word}: {sorted_dict[word]}" + '\n'
        conjoined_string += word + '|'
        # We take the N-th rank word frequent
        if i == TOP_LIST:
            break
        else:
            i += 1
    if(DEBUG == 1):
        thread_print += f"[*] Plaintext top misspelled words fingerprint: {conjoined_string}" + '\n'
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("S_" + conjoined_checksum)
    thread_print += f"[*] Top {TOP_LIST} misspelled words fingerprint: {conjoined_checksum}" + '\n'
    print(thread_print + '\n')
    status[thread_id] = 1

def word_frequency_analyser(status, thread_id):
    '''
    Function that takes in a body of text
    returns every word used and its frequency
    '''
    thread_print = "------[BEGIN WORD FREQUENCY ANALYSER]------" + '\n'
    word_frequency = {}
    for lines in parsed_words:
        for word in lines:
            try:
                if(word_frequency[word] > 0):
                    word_frequency[word] += 1
            except KeyError:
                word_frequency[word] = 1
    # Sorting using a for loop
    sorted_dict = {}
    for key in sorted(word_frequency, key=word_frequency.get, reverse=True):
        sorted_dict[key] = word_frequency[key]
    thread_print += f"[*] Top {TOP_LIST} encountered words in body:" + '\n'
    i = 0
    conjoined_string = ''
    for word in sorted_dict:
        thread_print += f"[*] {word}: {sorted_dict[word]}" + '\n'
        conjoined_string += word + '|'
        # We take the N-th rank word frequent
        if i == TOP_LIST:
            break
        else:
            i += 1
    if(DEBUG == 1):
        thread_print += f"[*] Plaintext top used words fingerprint: {conjoined_string}" + '\n'
    conjoined_checksum = hashlib.sha256(conjoined_string.encode()).hexdigest()
    STYLE_FINGERPRINT.append("F_" + conjoined_checksum)
    thread_print += f"[*] Top {TOP_LIST} used words fingerprint: {conjoined_checksum}" + '\n'
    print(thread_print + '\n')
    status[thread_id] = 1
    
def thread_waiter(status):
    waiter = 0
    while(waiter == 0):
        for x in status:
            if x != 0:
                waiter = 1
            else:
                waiter = 0
                break

def thread_creator(func, tupl, status, thread_id):
    try:
        # (row, query, status, threadid, config, )
        start_new_thread(func, tupl)
    except:
        status.pop(len(status)-1)
        thread_waiter(status)
        status.extend([0]*1)
        thread_creator(func, tupl, status, thread_id)

if __name__ == "__main__":
    '''
    Main function for running multi threads for each analyser
    '''
    print(LOGO)
    print("[*] LINGUANA v1.4 - Linguistics Fingerprint Analyser")
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
                    # No new lines and lower case per line
                    line = line.decode('utf-8').rstrip().lower()
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
                status = []
                thread_id = 0
                threads = [wpl_analyser, cpw_analyser, word_frequency_analyser, n_gram_analyser, spelling_analyser]
                for thread in threads:
                    status.extend([0]*1)
                    thread_creator(thread, (status, thread_id, ), status, thread_id)
                    thread_id += 1
                thread_waiter(status)
                
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