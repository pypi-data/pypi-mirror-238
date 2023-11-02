#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sep 16 2023
BioParse file contains program for accessing some formats like;
FASTA, FASTQ, PDB, CIF etc.. and also different methods on it. 
@author: ANIKET YADAV
"""

# from biobeee.BioProcessing.analysis import transform

def transform(mtrix):
    transf = []
    for i in range(len(mtrix[0])):
        lisr = []
        for j in range(len(mtrix)):
            lisr.append(mtrix[j][i])
        transf.append(lisr)
    return transf

class ParsingFASTA:
    
    # this program for read the fasta file in python 
    # returns string type of single lined sequence
    def readFASTAfile(self, TextFile):
        try:
            seqString = []
            sequence = []
            stringForm = ''
            with open(TextFile, 'r') as f:
                # read from second line, drop first description line
                data = f.readlines()[1:]
                seqString = data
                f.close()
                for element in seqString:
                    # repplace new line to serice
                    sequence.append(element.replace('\n', ''))
            # returns a string type in a single line
            return stringForm.join(sequence)
        # if any type of error in reading 
        except:
            return 'ERR102: specify wrong path!'

    # read multiple sequences contains FASTA file or updated program of readFASTAfile(self, TextFile) -> str| err102
    def MultiFASTA(self, file_path):
        try:
            header = [] # make list variable for storing headers of the formats
            seq = "" # store seq with '-' seperator, in the last it can be splited with '-' symbol
            with open(file_path, 'r') as fasta: # open file with read mode as fasta variable
                for line in fasta.readlines():
                    rline = line.replace('\n', '') # first replace/remove new line with NULL for all lines
                    if '>' in rline: # if '>' contains in any line, "it is the header"
                        header.append(rline) # than push these line in to header list
                        seq += '-' # and add a '-' to into seq, for recognizing reads seperator
                    else:
                        seq += rline # else add line into seq than last close the file
                fasta.close() 
            # return's three values in the form of tuple (headers in the form of list, 
            # sequences in the form of list, number of reads/sequences)
            return header, seq.split('-')[1:], len(header)
        except:
            return 'ERR102: specify wrong path!'
    
    # to find's the length of the nucleotide/protein sequences in a FASTA file
    def SeqLen(self, file_path_):
        # read sequence with assume as multiple seq contains in a file
        header, seq, _reads = self.MultiFASTA(file_path_)
        if _reads == 1: # if fasta file contains only one sequence
            # than return's length of string for only first single..
            return len(seq[0])
        # else return's a list of all lengths of sequence
        else: return [len(s) for s in seq]

    # create fasta file using locus, DEFINITION, ORGANISM, VERSION and file_Path of text file of
    # sequence return a new file where you give file path
    def makeFASTAFile(self, sequence, LOCUS, DEFINITION, ORGANISM, VERSION, file_Path):
        try:
            with open(file_Path, 'a') as f1:
                # write first description line
                f1.write(f'>{LOCUS}| {VERSION}| {ORGANISM}| {DEFINITION}\n')
                count = 0
                # read a item and add into a single line
                for i in sequence:
                    f1.write(i)
                    count += 1
                    # check the condition if it's item count (codon) is 65
                    # then add a new line also reset the count number to 0 
                    if count == 65:
                        f1.write('\n')
                        count = 0
                f1.close()
            # returns the path of the given file where save the created fasta file 
            return file_Path
        except:
            return "ERR103: somthing went's wrong here, please try again!"


# created a class for reading FASTQ file format
# with takes a argument of file location on the local machine
class parsingFASTQ:

    def __init__(self, file_Location):
        # initialize argument of file location
        self.fileLocation = file_Location

    # function of reading FASTQ from FASTQformat class, returns dictionary of sequence and thier respective ASCII characters
    # ie. dict = {'seq': 'ASCII', ....}
    def readFASTQfile(self):
        # seqData is the empty list use for storing data of sequence and ASCII only,
        # seqData variable drop all the sep (+) and header line starting from '@'
        seqData = []
        # seq and ascii list variable stores sequence and thier ASCII code seperately...
        (seq, ascii) = ([], [])
        with open(self.fileLocation, 'r') as FASTQ:
            # open FASTQ file and read as 'FASTQ', reading start from 2nd lines and store in 'line' variable
            # ie. try to drop first header.
            line = FASTQ.readlines()[1:]
            for i in range(len(line)):
                if i%2 == 0:         # seqData stores those line which contain ASCII and sequence both (even lines)
                    seqData.append(line[i].replace('\n', ''))    # replace all new lines (\n) of the each lines
        
        # this is the seperate part of this program, makes a 'seq' and 'ascii' list from 'seqData', and than 
        # a dict (seqdict) from 'seq' and 'ascii'...
        for i in range(len(seqData)):
            if i%2 == 0:       # this part is same as above even line part, where 'seq' store sequence data from 'seqData'
                seq.append(seqData[i])
            elif i%2 != 0:      # except all (ASCII CODE) stores 'ascii'
                ascii.append(seqData[i])
        seqdict = {key: value for key, value in zip(seq, ascii)}  # use dict. comprehension to make dict of 'seq' and 'ascii'
        # return dict of final sequence and thier respective ASCII code for finding the phred score of that sequence
        return seqdict

    # fuction to return length of the FASTQ file 
    # read sequences in single file
    def FASTQlen(self):
        fastq = self.readFASTQfile()   
        # reutrns the length of the dict...
        return len(fastq)
    
    # function for returning top most limit of sequence
    def head(self, top=5):
        # takes a argument 'top' for reading or returning limited sequence from top 
        fastq_limited = self.readFASTQfile()
        # read and select all fastq and makes a list of total tuple items
        lis_limit = list(fastq_limited.items()) 
        return dict(lis_limit[:top])  # and create a dictionary of top limited list


def FASTQ_to_FASTA_Convertion(inputFile, outputFile, limits=5):
    import re
    with open(inputFile, 'r') as readFastsq:
        readlist = readFastsq.readlines()
        (header, seqs) = ([], [])
        for line in range(len(readlist)):
            if line%2 == 0:
                if readlist[line][0] == '@':
                    replacesign = readlist[line].replace('@', '>')
                    header.append(replacesign)
            else:
                if re.search("^[ATGC]+$", readlist[line]):
                    seqs.append(readlist[line])
    
    outfile = f"{outputFile}out_{header[0].split()[0][1:]}.fasta"
    with open(outfile, 'a') as outfile:
        l = 0
        for h, s in zip(header, seqs):
            if l < limits:
                outfile.write(h)
                outfile.write(s)
                l += 1
            else: break
        outfile.close()
    return outfile


def gene_transfer_format_file(file_path, row='all'):
    (data, n) = ([], 0)
    with open(file_path, 'r') as gtf:
        for line in gtf.readlines()[2:]:
            if row == 'all':
                data.append(line.replace('\n', '').split('\t'))
            elif n != row:
                data.append(line.replace('\n', '').split('\t'))
                n+=1
            else: break
    return data


################################ END OF THE PROGRAM ########################################

# path = os.path.abspath('A:/PROJECTS/BIOINFORMATICS_software/own_packages/pyCrossbill/docs/samples/dengu3_strain-D00-0107.fasta')
# sequence = fromTXTfile(path)
# print(readFASTAfile(path))
# print(ParsingFASTA().SeqLen('A:/PROJECTS/C#_Programs/Bioinfo/BioSyS_Tool/bin/Debug/net6.0/docs/samples/samples/sequence.fasta'))
# print(FASTAFile(sequence, 'NC_500.64', 'dengu3_strain-D00-0107', 'dengu3', '546.6', 'file.fasta'))


# file_path = 'A:/PROJECTS/BIOINFORMATICS_software/own_packages/pyCrossbill/test.txt'
# fastq_ = 'A:/PROJECTS/ERR101899.1_sample.fastq'
# # FASTQ = FASTQformat('A:/PROJECTS/out_140trim@ERR101899.1.fastq')
# FASTQ = parsingFASTQ('A:/PROJECTS/out_1000_ERR101899.1.fastq') # 
# s1 = 'CCTACGGGTGGCAGCAGTGAGGAATATTGGTCAATGGACGGAAGTCTGAACCAGCCAAGTAGCGTGCAG'
# s2 = 'CCTACGGGTGGCTGCAGTGAGGAATATTGGACAATGGTCGGAAGACTGATCCAGCCATGCCGCGTGCAG'
# # print(remove_duplicates(['ACGTGGCTGATCGAT', 'ACATGCGGGATCGAT', 'ACGTGGCTGATCGAT', 'AAGGATCATCGATTT', 'ACATGCGGGATCGAT']))
# lis = ['ACGTGGCTGATCGAT', 'ACATGCGGGATCGAT', 'ACGTGGCTGATCGAT', 'AAGGATCATCGATTT', 'ACATGCGGGATCGAT']

# dict = FASTQ.head(500)
# quality = Quality_scoring(dict).quality()
# print(quality[0])
# visualization().scoring_graph_BASE33(quality[0], quality[1]) # style=['hot', 'cool', 'heatmap', 'white', 'gray']
# print(Trimming(fastq_).trimFASTQ_reads(1000, 'A:/PROJECTS/BIOINFORMATICS_software/own_packages/pyCrossbill/'))
# print('number of the readings: ', FASTQ.FASTQlen())
# gc = GC_percentage(dict)
# print(len(gc))

# print(Trimming('A:/PROJECTS/out_1000_ERR101899.1.fastq').seqTrimming('14-140', 'A:/PROJECTS/'))
# visualization().GC_graph(gc)