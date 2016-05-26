#!/usr/bin/env python
import sys

def aminoconv(code_list=[],frm=0,to=0):
    name_list =['arginine','histidine','lysine','aspartic acid','glutamic acid',
                'serine','threonine','asparagine','glutamine','cysteine',
                'selenocysteine','glycine','proline','alanine','valine',
                'isoleucine','leucine','methionine','phenylalanine','tyrosine',
                'tryptophan']
    three_list =['arg','his','lys','asp','glu','ser','thr','asn','gln','cys',
                 'sec','gly','pro','ala','val','ile','leu','met','phe','tyr',
                 'trp']
    one_list = ['r','h','k','d','e','s','t','n','q','c','u','g','p','a','v','i',
                'l','m','f','y','w']
    from_list = []
    to_list = []
    output = []
    usr_input = ''
    while code_list == [] or usr_input != '':
        usr_input = input('Please enter the next item of the sequence:')
        if usr_input != '':
            code_list.append(usr_input)
    while from_list == []:
        if str(frm) == '1':
            from_list = one_list
        elif str(frm) == '3':
            from_list = three_list
        elif str(frm) == 'name':
            from_list = name_list
        else:
            frm = input("PLease enter what you want to convert from (1"+
                        ",3 or name):")
    while to_list == []:
        if str(to) == str(frm):
            print('Trying to convert the input to it\'s own type')
            to = input("Please enter what you want to convert to (1,3 or name):")
        elif str(to) == '1':
            to_list = one_list
        elif str(to) == '3':
            to_list = three_list
        elif str(to) == 'name':
            to_list = name_list
        else:
            to = input("Please enter what you want to conver to (1,3 or name):")

    for i in code_list:
        if (str(frm) == '1' and len(i) !=1) or (str(frm) == '3' and len(i) != 3):
            print('Input does not contain a list of '+str(frm)+' letter from!')
            return 1
        if i.lower() in from_list:
            output.append(to_list[from_list.index(i.lower())])
        else:
            output.append('?')
    output = [element.capitalize() for element in output]
    return output

if __name__ == '__main__':
    print(aminoconv())

