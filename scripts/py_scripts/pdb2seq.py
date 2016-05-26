#!/usr/bin/env python
import sys
from aminoconv import aminoconv as aminoconv

# Function to generate a sequence file(.seq) from a given .pdb file.
def main():
    # Checks if a and only a .pdb file is given.
    if len(sys.argv) != 2 or sys.argv[1].endswith('.pdb') is False:
        print("No pdb file given")
        return 1

    # Opens the .pdb file to read and the .seq to write.
    pdb_file = open(sys.argv[1], 'r')
    file_name = sys.argv[1].rsplit('.', 1)[0]
    seq_file = open(file_name+'.seq', 'w+')

    # Variables needed n = ResID of pdb, chain = chain and sol is number of SOL.
    n = ''
    chain = ''
    sol = 0

    seq_file.write('Sequence of '+sys.argv[1]+'.')

    # Reads the .pdb file line by line
    for line in pdb_file:

        # Splits the line in arguments
        argument = line.split()

        # Only consider atom lines
        if argument[0] == 'ATOM':

            # Needed because if ResID > 999 chain and ResID are 1 argument
            if len(argument) == 11:
                if argument[4] != chain:
                    chain = argument[4]
                    seq_file.write('\n\nChain '+chain+':\n')
                # If the ResID is not already considered.
                if argument[5] != n:
                    if len(argument[3]) == 3 and argument[3] != 'SOL':
                        output = aminoconv([argument[3]], 3, 1)
                        seq_file.write(output[0])
                    elif argument[3] == 'SOL':
                        sol += 1
                    else:
                        seq_file.write('?')
                    n = argument[5]
            elif len(argument[4]) == 5:
                if argument[4][0] != chain:
                    chain = argument[4][0]
                    seq_file.write('\n\nChain '+chain+':\n')
                if argument[4][1:] != n:
                    if len(argument[3]) == 3 and argument[3] != 'SOL':
                        output = aminoconv([argument[3]], 3, 1)
                        seq_file.write(output[0])
                    elif argument[3] == 'SOL':
                        sol += 1
                    else:
                        seq_file.write('?')
            else:
                if argument[4] != n:
                    if len(argument[3]) == 3 and argument[3] != 'SOL':
                        output = aminoconv([argument[3]], 3, 1)
                        if chain != 'unknown':
                            seq_file.write('\n\nUnknown Chain:\n')
                            chain = 'unknown'
                        seq_file.write(output[0])
                    elif argument[3] == 'SOL':
                        sol += 1
                    else:
                        seq_file.write('?')

    if sol != 0:
        seq_file.write('\n\nThis pdb file includes ' +str(sol)+
                       ' solvent molecules')
    seq_file.close()
    pdb_file.close()
    print('Sequence of '+file_name+'.pdb written to '+file_name+'.seq.')
# Only call main when this script is the main script
if __name__ == "__main__":
    main()
