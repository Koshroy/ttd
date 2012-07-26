import operator, math, numpy, nltk
from scipy.cluster.vq import *

class FreqTable(object):

    def __init__(self):
        # Initialize the frequency table
        self.__table = {}
        self.__word_cnt = 0
        return

    def add_word_inst(self, word):
        # Add a word to the frequency table
        self.__word_cnt = self.__word_cnt + 1
        if (word == " ") or (word == ""):
            return
        if word in self.__table:
            res = self.__table[word]
            res = res + 1
            self.__table[word] = res
        else:
            self.__table[word] = 1

    def add_word_occurances(self, word, num_occur):
        # Add n instances of a word to the frequency table
        self.__word_cnt = self.__word_cnt + 1
        if (word == " ") or (word == ""):
            return
        if word in self.__table:
            res = self.__table[word]
            res = res + num_occur
            self.__table[word] = res
        else:
            self.__table[word] = num_occur


    def del_word(self, word):
        # Remove word from the table
        if word in self.__table:
            del(self.__table[word])

    def get_word_count(self, word):
        # Return the number of occurrances of a word in the table
        if word in self.__table:
            return self.__table[word]
        else:
            return 0

    def word_list(self):
        # Return a list of words in the table
        return self.__table.keys()

    def get_word_freq(self, word):
        # Return the frequency of a word in this table
        if word in self.__table:
            return (self.__table[word]*1.0) / self.__word_cnt
        else:
            return 0

    def freq_list(self):
        # Return a list of the form [word, occurrances]
        return sorted(self.__table.items(), key=operator.itemgetter(1), reverse=True)

    def print_freq_list(self):
        # Print a list of words and their frequencies
        l = self.freq_list()
        for entry in l:
            print "Word: [" + entry[0] + "]: " + str(entry[1])

    def get_top_words(self, top_ind):
        # Return the top #top_ind ranked words in a list
        top_list = sorted(self.__table.items(), key=operator.itemgetter(1), reverse=True)
        if len(top_list) < top_ind:
            top_ind = len(top_list)
        out_list = []
        for i in xrange(top_ind):
            out_list.append(top_list[i][0])
        return out_list
        
        
class Text(object):
    def __init__(self, fname):
        self.__fname = fname
        self.__freq_table = FreqTable()

    def fname(self):
        return self.__fname

    def __sanitize(self, text):
        # Process the text to remove undesirable
        # markers
        ftext = text
        ftext = ftext.lower()
        ftext = ftext.replace('\r', ' ')
        ftext = ftext.replace('\n', ' ')
        ftext = ftext.replace('.', '')
        ftext = ftext.replace(',', '')
        ftext = ftext.replace(';', '')
        ftext = ftext.replace("'", '')
        ftext = ftext.replace('_', '')
        ftext = ftext.replace('"', '')
        ftext = ftext.replace(':', '')
        ftext = ftext.replace('-', '')
        ftext = ftext.replace('(', '')
        ftext = ftext.replace(')', '')
        return ftext
        

    def build_freq_table(self):
        # Build the underlying frequency table
        # for the text
        f = open(self.__fname, 'rt')
        text = f.read()
        new_text = self.__sanitize(text)
        words_text = new_text.split(' ')
        for word in words_text:
            self.__freq_table.add_word_inst(word)

    def change_filename(self, fname):
        # Change the filename
        self.__fname = fname
        self.__freq_table = FreqTable()
        
    def get_freq_table(self):
        # Return the build frequency table
        return self.__freq_table

    
        
def similarity(t1, t2):

    # Determine the similarity between two texts


    # Prune the top 10 words out.
    # Text similarity is not helped by looking
    # at the top 10 words, because in English
    # the top 10 words are shared by almost every text

    t1_top_10 = t1.get_top_words(10)
    t2_top_10 = t2.get_top_words(10)


    if len(t1.freq_list()) > len(t1_top_10):
        for word in t1_top_10:
            t1.del_word(word)
    if len(t2.freq_list()) > len(t2_top_10):
        for word in t2_top_10:
            t2.del_word(word)

    # Build up a set of all unique words in both texts

    term1 = t1.word_list()
    term2 = t2.word_list()
    term_all_set = set()

    for t in t1.get_top_words(100):
        term_all_set.add(t)
    for t in t2.get_top_words(100):
        term_all_set.add(t)

    freq_list1 = t1.freq_list()
    freq_list2 = t2.freq_list()

    common_weights_1 = []
    common_weights_2 = []

    # Now determine the relative frequencies of the
    # words shared between the two texts. We can only calculate
    # similarity for words that occur in the two corpora

    for t in term_all_set:
        common_weights_1.append(t1.get_word_freq(t))
        common_weights_2.append(t2.get_word_freq(t))


    # Calculate a vector difference

    sum_sq_w1 = 0
    sum_sq_w2 = 0
    for i in common_weights_1:
        sum_sq_w1 = sum_sq_w1 + i**2
    
    for i in common_weights_2:
        sum_sq_w2 = sum_sq_w2 + i**2

    norm_weight = math.sqrt(sum_sq_w1 * sum_sq_w2)

    mult_wt = []
    for i in xrange(len(common_weights_1)):
        #print str(common_weights_1[i]) + " " + str(common_weights_2[i])
        mult_wt.append(common_weights_1[i] * common_weights_2[i])
    sum_mult_wt = reduce(lambda x, y: x + y, mult_wt)

    # Return this vector difference

    return sum_mult_wt / norm_weight


def cluster_list(f_list):
    tables = []

    simil_dict = {}

    for f in f_list:
        m = Text(f)
        m.build_freq_table()
        tables.append(m)

    # Calculate a prototypical average frequency table
    # from all constituent texts

    # Calculate similarities from this prototypical text
    # and apply K-Means to the similarity vector

    avg_table = average_freq_table([i.get_freq_table() for i in tables])
    base_simil = avg_table
    simil = []
    cnt = 0
    for t in tables:
        s = similarity(base_simil, t.get_freq_table())
        simil.append([s])
        simil_dict[f_list[cnt]] = s
        cnt = cnt + 1

    # Try to cluster into two particular "topics"
    ret = kmeans(numpy.matrix(simil), 2)
    topic1_mean = ret[0][0][0]
    topic2_mean = ret[0][1][0]

    new_cnt = 0
    for text_inst in tables:
        print "File name: " + str(f_list[new_cnt])
        text_inst.get_freq_table().print_freq_list()
        print "\n"
        new_cnt = new_cnt + 1


    #print simil_dict

    # Find the two closest center means

    out_clust1 = []
    out_clust2 = []

    for text_file in f_list[1:]:
        dist1 = numpy.abs(simil_dict[text_file] - topic1_mean)
        dist2 = numpy.abs(simil_dict[text_file] - topic2_mean)
  

        if dist1 < dist2:
            #print "Text: " + str(text_file) + " is classified as Topic #1"
            out_clust1.append(text_file)
        else:
            #print "Text: " + str(text_file) + " is classified as Topic #2"
            out_clust2.append(text_file)

    return [out_clust1, out_clust2]

def simil_matrix(text_list):
    out_matrix = []
    for t in text_list:
        matrix_row = []
        for other_t in text_list:
            if other_t == t:
                matrix_row.append(1)
            else:
                #t.get_freq_table().print_freq_list()
                matrix_row.append(similarity(t.get_freq_table(), other_t.get_freq_table()))
        out_matrix.append(matrix_row)
    return out_matrix
        

def average_freq_table(text_list):
    # Build up a frequency table that averages several frequency
    # tables
    avg_table = FreqTable()

    for t in text_list:
        for word in t.word_list():
            avg_table.add_word_occurances(word, t.get_word_freq(word))
    return avg_table
            

