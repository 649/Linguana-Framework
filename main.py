'''
LINGUANA v1.1
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

def n_gram_analyser(body, n=3, top=10):
    '''
    Function is designed to take in an integer factorial to count from
    Enumerates N-gram word pairings in a body of text
    '''
    def chunk_list(input_list, n, shift=0):
        shifted_list = input_list[shift:] + input_list[:shift]
        return [shifted_list[i:i+n] for i in range(0, len(input_list), n)]
    
    ngram = {}
    for i in range(n, 1, -1):
        print()
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
    print(f"[*] Top {top} used words fingerprint: {conjoined_checksum}")
    print()


if __name__ == "__main__":
    '''
    Main function for running multi threads for each analyser
    '''
    print("[*] LINGUANA v1.1")
    print("[*] Linguistics Analyser")
    spell = Speller(lang='en')
    if(len(sys.argv) > 2 and sys.argv[1] == '--input'):
        fn = sys.argv[2]
        if os.path.exists(fn):
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
                print("------[BEGIN WORD FREQUENCY ANALYSER]------")
                word_frequency_analyser(parsed_words)
                print("------[BEGIN N-GRAM ANALYSER]------")
                n_gram_analyser(parsed_words)
                print("------[BEGIN SPELLING ANALYSER]------")
                spelling_analyser(parsed_words)

    else:
        print(f"[*] Scan file: {sys.argv[0]} --input PATH")