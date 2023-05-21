import time
import matplotlib.pyplot as plt

#HTML TO TEXT
def htmlToText(file):
    string_with_spaces = file.readlines() #Reads all lines includes html tags like body, html, any kind of it.
    string_with_spaces = ' '.join(string_with_spaces)
    text =""
    for element in range(0,len(string_with_spaces)):
        if(string_with_spaces[element] != " "):
            text = string_with_spaces[element:-1]
            break

    return text

#Creating Bad Match Table
def badSymbolTable(pattern, size):
    badChar = [-9]*256

    #Define utf-8 value of symbols in pattern
    for i in range(size-1):
        badChar[ord(pattern[i])] = size -i -1

    #Define last symbol of pattern according to Horspool Algorithm
    if badChar[ord(pattern[size-1])]>0: 
        pass
    else:
        badChar[ord(pattern[size-1])] = size

    #Define non-existent symbols in pattern to size of pattern
    for k in range(256):
        if badChar[k]<0:
            badChar[k] = size
    return badChar

#This function create good suffix table by looking at substrings of the pattern which begins at the end of the pattern.
def goodSuffixTable(shift, position, pattern, pattern_length):
    pt_length = pattern_length
    pt_length_plus = pattern_length + 1
    position[pt_length] = pt_length_plus
    
    #This loop continues until the beginning of the pattern from the end of the pattern to create good suffix table according to rightmost occurence.
    while pt_length > 0:
        while pt_length_plus <= pattern_length and pattern[pt_length - 1] != pattern[pt_length_plus - 1]:
              
            if shift[pt_length_plus] == 0:
                shift[pt_length_plus] = pt_length_plus - pt_length
            pt_length_plus = position[pt_length_plus]
        pt_length -= 1
        pt_length_plus -= 1
        position[pt_length] = pt_length_plus

    position2 = position[0]
    for i in range(pattern_length + 1):

        if shift[i] == 0:
            shift[i] = position2

        if i == position2:
            position2 = position[position2]



def brute_force_search(text, pattern):
    #To measure runtime
    start_time = time.time()
    n = len(text)
    m = len(pattern)
    comparisons = 0
    matches = []
    found_index_start = []
    found_index_end = []
    match_count = 0
    
    #Check every letter of the pattern starting from 0th index and shift by one.
    for i in range(n - m + 1):
        j = 0

        while j < m and text[i + j] == pattern[j]:
            j += 1
            comparisons += 1

        #if comparison count in the while loop equals to pattern lenght increase match count by one.
        if j == m:
            matches.append(i)
            found_index_start.append(i)
            found_index_end.append(i+len(pattern)-1)
            comparisons += 1
            match_count += 1
        comparisons += 1
    brute_force_time = (time.time() - start_time) * 1000
    markText(found_index_start,found_index_end,text,match_count,comparisons,"bruteforce")
    return brute_force_time, comparisons




def boyerMoore(pattern, text, badChar, goodSuffix,patternIndex, textIndex):
    
    start_time = time.time()
    i = patternIndex -1 #i = lenght of pattern - 1 
    never_match = True #At the beginning there is not one match. If there is one we will use this later.
    found_index_start = []
    found_index_end = []
    comparison_count = 0
    match_count = 0

    #While index of text is less than or equal to lenght of text.
    while i <= textIndex -1:
        temp_i = i
        j = len(pattern) - 1
        any_match = False
        
        shift = 0
        
        #While chars of pattern and text is equal and their indexes are more than zero.
        while pattern[j] == text[i] and j >= 0 and i >= 0:

            any_match = True
            i -= 1 
            j -= 1
            

        #If there is complete match of pattern to text.
        if(j==-1):

            found_index_start.append(temp_i +1- len(pattern)) #Noting start of the match index to use later.
            found_index_end.append(temp_i) #Noting end of the match index to use later.
            never_match = False #In this if condition there is complete match so never_match becomes false.
            shift = 1 #To check overlapping matches we shift text index by 1.
            i = temp_i + shift
            comparison_count += len(pattern) #Since there is complete match our comparison_count will be equal to lenght of pattern.
            match_count += 1

        #When there is partial match we do shift by the first match letter's value in bad symbol table.
        elif(any_match):

            bad_char_shift = badChar[ord(text[i])] - (temp_i - i)
            good_suffix_shift = goodSuffix[temp_i-i]
            shift = 0
            #Compare the shift values of bad symbol table and good suffix table get the greater one.
            if bad_char_shift >= good_suffix_shift:
                shift = bad_char_shift
            else:
                shift = good_suffix_shift
            
            comparison_count += temp_i - i
            i = temp_i + shift
            
        #When there is not any match we do shift by the lenght of the pattern due to bad symbol table.
        else:
            #shift = length of pattern
            shift = badChar[ord(text[temp_i])]
            i = temp_i + shift
            comparison_count += 1
            
    #When pattern is not found in text. 
    if(never_match == True):
        print("Pattern not found in text!")
    boyer_moore_time = (time.time() - start_time) * 1000
    markText(found_index_start,found_index_end,text,match_count,comparison_count,"boyermoore")
    return boyer_moore_time, comparison_count

def horspool(pattern, text, badChar, patternIndex, textIndex):
    start_time = time.time()
    i = patternIndex -1 #i = lenght of pattern - 1 
    never_match = True  #At the beginning there is not one match. If there is one we will use this later.
    found_index_start = []
    found_index_end = []
    comparison_count = 0
    match_count = 0

    #While index of text is less than or equal to lenght of text.
    while i <= textIndex -1:
        temp_i = i
        j = len(pattern) - 1
        any_match = False
        
        shift = 0

        #While chars of pattern and text is equal and their indexes are more than zero.
        while pattern[j] == text[i] and j >= 0 and i >= 0:

            any_match = True
            i -= 1 
            j -= 1
            
        #If there is complete match of pattern to text.
        if(j==-1):
            
            found_index_start.append(temp_i +1- len(pattern)) #Noting start of the match index to use later.
            found_index_end.append(temp_i) #Noting end of the match index to use later.
            never_match = False #In this if condition there is complete match so never_match becomes false.
            shift = 1   #To check overlapping matches we shift text index by 1.
            i = temp_i + shift
            comparison_count += len(pattern) #Since there is complete match our comparison_count will be equal to lenght of pattern.
            match_count += 1
            
        #When there is partial match we do shift by the first match letter's value in bad symbol table.
        elif(any_match):
            #shift = first matches' bad symbol value
            shift = badChar[ord(text[temp_i])]
            comparison_count += temp_i - i
            i = temp_i + shift
            

        #When there is not any match we do shift by the lenght of the pattern due to bad symbol table.
        else:
            #shift = length of pattern
            shift = badChar[ord(text[temp_i])]
            i = temp_i + shift
            comparison_count += 1
            

    #When pattern is not found in text.        
    if(never_match == True):
        print("Pattern not found in text!")
    horspool_time = (time.time() - start_time) * 1000
    markText(found_index_start,found_index_end,text,match_count,comparison_count,"horspool")

    return horspool_time, comparison_count
    

def markText(found_index_start,found_index_end,text,match_count,comparison_count,algorithm_name):
    
    j= 1
    overlap = []
    
    for i in range(0,len(found_index_end)):
        
        #if end index of the match is more than the start of the other match index there is overlap.
        if j<len(found_index_start) and found_index_end[i] > found_index_start[j] :

            overlap.append([found_index_end[i+1],found_index_start[j-1]])
            j+=1
        #When there is no overlap add - to understand there is no overlap.
        else:
            overlap.append("-")
            j+=1
            continue
    

    overlap_items = []
    marked_text = text
    isFirst = 0
    overlap_number = 0
    overlap_adjustment = []
    for element in overlap:
        
        #While there is no - sign add overlap elements to overlap_items.
        if element != "-":
            overlap_items.append(element[0])
            overlap_items.append(element[1])
    
        else:
            temp = overlap_items
            overlap_items = []
            
            #Create overlap_adjustment and add min-max values of overlap_items then use it to mark accordingly.
            if temp:
                start_mark = min(temp)
                end_mark = max(temp)+1
                overlap_adjustment.append([start_mark,end_mark])

            #Every time we use <mark> and </mark> shift next indexes by the lenght of them (13).
            if(isFirst == 1):
                for x in range(len(temp)):
                    temp[x] += 13 * overlap_number
            
            #Add 13 to starting point and end point of the overlap and create text that is marked (marked_text)
            if temp:
                start_mark = min(temp)

                end_mark = max(temp)+1
                
                
                marked_text = marked_text[:start_mark] + '<mark>' + marked_text[start_mark:end_mark] + '</mark>' + marked_text[end_mark:]
 
                overlap_number +=1
            isFirst = 1
            
    #Start index of the overlap 
    list_start = []
    #End index of the overlap
    list_end = []
    #Start index of the not overlap
    not_overlap_start = []
    #End index of the not overlap
    not_overlap_end = []
    for i in overlap_adjustment:
        for j in range(len(found_index_end)):
            if i[0] <= found_index_start[j] and i[1] >= found_index_end[j]:
                list_start.append(found_index_start[j])
                list_end.append(found_index_end[j])

    
    s = set(list_start)
    not_overlap_start = [x for x in found_index_start if x not in s]


    s = set(list_end)
    not_overlap_end = [x for x in found_index_end if x not in s]

    #Shifting indexes 13 by the iteration number.
    j = 0
    for i in range(len(overlap_adjustment)):
        while j < len(not_overlap_end):
            if not_overlap_end[j] < overlap_adjustment[i][0]:
                shift = i * 13
                not_overlap_start[j] += shift
                not_overlap_end[j] += shift
                j+=1
            else:
                break
    #Marking the single matches.
    for i in range(len(not_overlap_start)-1, -1, -1):
        marked_text = marked_text[:not_overlap_end[i]+1] + "</mark>" + marked_text[not_overlap_end[i]+1:]
        marked_text = marked_text[:not_overlap_start[i]] + "<mark>" + marked_text[not_overlap_start[i]:]

    #Open the correct files according to algorithm_name given.
    if(algorithm_name == "bruteforce"):
        file = open("brute_force_result.html",mode="w")


    elif(algorithm_name == "horspool"):
        file = open("horspool_result.html",mode="w")

    elif(algorithm_name == "boyermoore"):
        file = open("boyermoore_result.html",mode="w")

    
    file.write(marked_text)
    
    print("Match Count:",match_count)
    print("Comparison Count:",comparison_count)

#Creating time plot function to compare efficiency of the 3 different algorithms.
def time_plot(brute_force_time, horspool_time,boyer_moore_time):
    algorithm_names = ['Brute‑force', 'Horspool', 'Boyer‑Moore']
    times = [brute_force_time,horspool_time,boyer_moore_time]
    plt.bar(range(len(algorithm_names)), times)
    plt.xticks(range(len(algorithm_names)), algorithm_names)
    plt.xlabel('Algorithm')
    plt.ylabel('Running Time in Miliseconds')
    plt.title('Running Times Plot')
    plt.show()

#Creating comparison plot to compare efficiency of the 3 different algorithms.
def comparison_plot(brute_force_comparison, horspool_comparison,boyer_moore_comparison):
    algorithm_names = ['Brute‑force', 'Horspool', 'Boyer‑Moore']
    comparison = [brute_force_comparison,horspool_comparison,boyer_moore_comparison]
    plt.bar(range(len(algorithm_names)), comparison)
    plt.xticks(range(len(algorithm_names)), algorithm_names)
    plt.xlabel('Algorithm')
    plt.ylabel('Comparison Count')
    plt.title('Comparison Plot')
    plt.show()



def main():
    file = open("at_that_example.html",mode="r",encoding="utf8")
    text = htmlToText(file)

    pattern = "AT_THAT"
    patternIndex = len(pattern)
    textIndex = len(text)

    #Creating bad symbol table.
    badChar = badSymbolTable(pattern, len(pattern))
    chars = []
    for i in range(256):
        chars.append(chr(i))
    
    bad_char_table = {chars[i]: badChar[i] for i in range(len(chars))}
    print("Bad Symbol Table:",bad_char_table)


    #Creating good suffix table.
    position = [0] * (len(pattern) + 1)
    goodSuffix = [0] * (len(pattern) + 1)
    print()

    goodSuffixTable(goodSuffix, position, pattern, len(pattern))
    goodSuffix.reverse()
    keys_of_good_suffix = []

    #Creating list of substrings.
    for i in range(len(pattern)-1,-1,-1):
        keys_of_good_suffix.append(pattern[i:])

    goodSuffix2 = goodSuffix[1:]
    good_suffix_table = {keys_of_good_suffix[i]: goodSuffix2[i] for i in range(len(keys_of_good_suffix))}

    print("Good Suffix Table:",good_suffix_table)


    #Calling algorithms.
    print()
    print("----------BRUTE-FORCE ALGORITHM:-----------")
    print("Pattern:",pattern)
    brute_force_time, brute_force_comparison = brute_force_search(text, pattern)
    print("Brute Force Running Time: %s miliseconds." % (brute_force_time))

    print()
    print("----------HORSPOOL ALGORITHM:-----------")
    print("Pattern:",pattern)
    horspool_time, horspool_comparison = horspool(pattern, text, badChar, patternIndex, textIndex)
    print("Horspool Running Time: %s miliseconds." % (horspool_time))

    print()
    print("------------------------------------------------------------")

    print()
    print("----------BOYER MOORE ALGORITHM:-----------")
    print("Pattern:",pattern)
    boyer_moore_time, boyer_moore_comparison = boyerMoore(pattern, text, badChar, goodSuffix, patternIndex, textIndex)
    print("Boyer Moore Running Time: %s miliseconds." % (boyer_moore_time))
    
    #Calling time plot and comparison plot.
    time_plot(brute_force_time,horspool_time,boyer_moore_time)
    comparison_plot(brute_force_comparison,horspool_comparison,boyer_moore_comparison)

    file.close()

main()