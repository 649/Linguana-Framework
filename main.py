'''
LINGUANA v1.0
Linguistics Analyzer
Author: @037

Application designed to take apart bodies of text and do comparative linguistics analysis.
Purpose is to draw conclusions if two bodies of text share authorship.
'''
import os
import sys
import hashlib
from itertools import islice
from autocorrect import Speller

def n_gram_analyzer(body, n=3, top=10):
    '''
    Function is designed to take in an integer factorial to count from
    Enumerates N-gram word pairings in a body of text
    '''
    def chunk_list(input_list, n):
        return [input_list[i:i+n] for i in range(0, len(input_list), n)]
    
    print("[*] Starting N-gram Analyzer")
    ngram = {}
    for i in range(n, 1, -1):
        print()
        print(f"[*] Taking {i}-gram of processed word list...")
        word_frequency = {}
        for lines in body:
            chunked_lines = chunk_list(lines, i)
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

def spelling_analyzer(body, top=10):
    '''
    Function that takes in a body of text
    returns a list of spelling mistakes
    '''
    print("[*] Starting Spelling Analyzer")
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

def word_frequency_analyzer(body, top=10):
    '''
    Function that takes in a body of text
    returns every word used and its frequency
    '''
    print("[*] Starting Word Frequency Analyzer")
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
    Main function for running multi threads for each analyzer
    '''
    print("[*] LINGUANA v1.0")
    print("[*] Linguistics Analyzer")
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
                    print(line)
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
                i = 0
                print("[*] Processing words... Please wait.")
                for line in target:
                    line = line.decode('utf-8')
                    print(f"[*] Line: {line}")
                    for delimiter in delimiter_list:
                        print(f"[*] Delimiter: {delimiter}")
                        line = line.replace(delimiter, ' ')
                    parsed_words.append(line.split(' '))
                    i += 1
                print("[*] Processed word list: ")
                print(parsed_words)
                for word in parsed_words:
                    print(word)
                print()
                word_frequency_analyzer(parsed_words)
                print()
                n_gram_analyzer(parsed_words)
                print()
                spelling_analyzer(parsed_words)

    else:
        print(f"[*] Scan file: {sys.argv[0]} --input PATH")