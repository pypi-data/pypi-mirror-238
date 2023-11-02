

# kmers return value in string or list.
def k_mers(sequence, k, alter=1, joined=False):
    '''
    k-mer method can converts the sequence string in to form of k numbers of letters word
    set alter to int value for selecting base just alternative, by deafult it is set with 1
    means alternative of one is selected for k-mer, joined=False; True for making single sentence through
    k-mer list.
    '''
    if joined == True:
        # if join = True than it will join the list of k-mer word with space using ' '.join(List) method
        return ' '.join([sequence[i:i+k] for i in range(0, len(sequence), alter) if k == len(sequence[i:i+k])])
    else:
        # else it will returns the list of words, by default because joined set equals to False
        return [sequence[i:i+k] for i in range(0, len(sequence), alter) if k == len(sequence[i:i+k])]


class BagOfWord():

    def uniqueAndKmerSep(self, sequence, k, alter=1):
        (kmer_unique, dup) = ([], [])
        for s in sequence:
            for i in range(0, len(s), alter):
                fragment = s[i:i+k]
                if k == len(fragment):
                    if fragment not in kmer_unique:
                        kmer_unique.append(fragment)
                    else: dup.append(fragment)
        return kmer_unique, dup

    ## vectorization
    def vectorization(self, seq, kmerList, k=6):
        vectorize = []
        for s in seq:
            cache = []
            kList = k_mers(s, k)
            for i in kmerList:
                cache.append(kList.count(i))
            vectorize.append(cache)
        return vectorize


# all the methods or analysis related to nucleotide sequence are written 
# in these Nucleotide class
class Nucleotides:

    def __init__(self, sequence) -> None:
        # converts all the sequence to UPPER CASE first, if it is exist in lower case 
        self.seq = sequence.upper()

    def IsNucleotide(self):
        nts = ['A', 'G', 'C', 'T']
        for i in self.seq:
            if i not in nts: return 1 # in case of error i.e. any non 'ATGC' letter found in seq
            else: pass # else it's pass normally

    def Length(self):
        return len(self.seq)
    
    def Contents(self):
        return self.seq.count('A'), self.seq.count('T'), self.seq.count('G'), self.seq.count('C')

    def GC_percent(self):
        if self.IsNucleotide() == 1:
            return 'ERR202: Not a valid nucleotide sequence.'
        
        else:
            (countG, countC) = (self.Contents()[2], self.Contents()[3])
            return ((countC+countG)/len(self.seq))*100
        
    def AT_percent(self):
        if self.IsNucleotide() == 1:
            return 'ERR202: Not a valid nucleotide sequence.'
        
        else:
            (countA, countT) = (self.Contents()[0], self.Contents()[1])
            return ((countA+countT)/self.Length())*100


def transform(mtrix):
    transf = []
    for i in range(len(mtrix[0])):
        lisr = []
        for j in range(len(mtrix)):
            lisr.append(mtrix[j][i])
        transf.append(lisr)
    return transf


# print(FASTQ_to_FASTA_Convertion('A:/miniProject/biobeee/docs/samples/out_1000_ERR101899.1.fastq', ''))

# there is the seperate function for removing duplicates from the list of the sequences
# returns the tuple of index and unique
def remove_duplicates(sequence_list):
    # 'index', where only unique sequence is counted and 'unique', filter the item in list of sequence_list variable
    (unique, index) = ([], [])
    for i in sequence_list:
        if sequence_list.index(i) not in index:
            index.append(sequence_list.index(i))
    
    for i in index:
        unique.append(sequence_list[i])

    return index, unique


def GC_percentage(seq_dict):
    GC_ = []
    def calc_GC_percentage(seq):
        (count_g, count_c) = (0, 0)
        for code in seq:
            if code == 'G':
                count_g += 1
            if code == 'C':
                count_c += 1
        return 100 * float((count_g + count_c)) / len(seq)

    for key in seq_dict:
        GC_.append(round(calc_GC_percentage(key), 2))
    return GC_


class Quality_scoring:

    def __init__(self, fastq_seq):
        self.seq_ = fastq_seq
    
    def pred_score_33(self, str_values):
        pred_list = []
        for char in str_values:
            pred_list.append(ord(char)-33)
        return pred_list

    def pred_score_64(self, str_values):
        pred_list = []
        for char in str_values:
            pred_list.append(ord(char)-64)
        return pred_list

    def isBASE(self):
        base_ = 'ILLUMINA_33'
        for k in self.seq_:
            ascii = self.seq_[k]
            for char in ascii:
                if char.islower() == True:
                    base_ = 'ILLUMINA_64'
                break
        return base_

    def quality(self):
        reading_scores = []
        for k in self.seq_:
            
            if self.isBASE() == 'ILLUMINA_33':
                reading_scores.append(self.pred_score_33(self.seq_[k]))
            if self.isBASE() == 'ILLUMINA_64':
                reading_scores.append(self.pred_score_64(self.seq_[k]))
        trasf = transform(reading_scores)
        mean = []
        for item in trasf:
            mean.append(sum(item)/len(item))
        return mean, trasf

    def best_readedScore(self):
        quality_list = Quality_scoring(self.seq_).quality()
        majorError = []
        for phreds in quality_list:
            error_prob = []
            for phred in phreds:
                P = 10**(-phred/10)
                error_prob.append(round(P, 6))
            S = sum(error_prob)/len(error_prob)
            majorError.append(round(S, 6))
        return majorError.index(min(majorError)), quality_list[majorError.index(min(majorError))]


class Trimming:
    
    def __init__(self, FASTQ_file):
        self.fastq = FASTQ_file

    def trimFASTQ_reads(self, chunks, outputfileLocation='null'):
        with open(self.fastq, 'r') as FASTQ:
            line = FASTQ.readlines()
            seqlines = line[:chunks*4]
        if outputfileLocation == 'null':
            file = self.fastq.split('/')
            file.pop()
            file.append(f'out_{chunks}_{seqlines[0].split()[0][1:]}.fastq')
            output = '/'.join(file)
        else: output = f'{outputfileLocation}out_{chunks}_{seqlines[0].split()[0][1:]}.fastq'

        with open(output, 'a') as outputFASTQ:
            for li in seqlines:
                outputFASTQ.write(li)
        return output
    
    def seqTrimming(self, probs, outputLocation):
        lines = ''
        with open(self.fastq, 'r') as FastqR:
            r = FastqR.readlines()
            for line in range(len(r)):
                if line%2 != 0:
                    even = r[line]
                    if '-' in probs:
                        frto = probs.split('-')
                        lines += even[int(frto[0]):int(frto[1])]+'\n'
                    else: lines += even[:probs]+'\n'
                else: lines += r[line][:-1]+f' => length={probs}\n'
                
        outfile = f"{outputLocation}out_{probs}trim{r[0].split()[0]}.fastq"
        with open(outfile, 'a') as fastqOut:
            fastqOut.write(lines)
            fastqOut.close()
        return outfile


############################## END OF THE PROGRAM ####################################

# print(Nucleotides('atggttaaccgtt').AT_percent())