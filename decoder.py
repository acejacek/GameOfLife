# RLE-strings decoder

def decode_object(input_string):
    
    result = []
    row = []
    repeat = 0
    
    dict = {'o': 1, 'b': 0}
    
    for character in input_string:
        try:
            value = int(character)  # this will trigger exception
            repeat *= 10
            repeat += value

        except Exception as e:   
            # character is not a number!
            if repeat == 0:  # only single character read
                repeat = 1
            for i in range(repeat):
                if character == '$':   # end of line
                    # print(i, character)
                    if len(row) == 0:
                        row.append(0)
                        
                    result.append(row)
                    row = []
                    
                elif character == '!':  # end of file
                    result.append(row)
                    
                    row = []
                    max_length = 0
                    for row in result:
                        if len(row) > max_length:
                            max_length = len(row)
                    for row in result:
                        for i in range(len(row),max_length):
                            row.append(0)
                    
                    print('object size: {} by {}').format(len(result),max_length)
                    
                    return result
                else:
                    row.append(dict[character])          
            repeat = 0
    print('End of file marker "!" missing?')
    
    return result

def load_object(name=''):
    
    lines = loadStrings(name)
    row_index = 1  # skip first line
    result = ''
    while row_index < len(lines):
        if lines[row_index].find('#',0,1) == -1:       # ignore comments
            if lines[row_index].find('x',0,1) == -1:   # ignore description
                result += lines[row_index]

        row_index += 1
    return result
        
    
    
