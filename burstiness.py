import numpy
import Text
from scipy.cluster.vq import *

# Return a list of relative frequencies of one text's middle-20 words
# compared with the frequency of these words in all neighboring texts
# This is the weight vector that will be used in the final clustering
def burst_analysis(t_list):
    middle_twenty = []
    for txt in t_list:
        words = txt.get_freq_table().get_top_words(120)
        #print words[10:20]
        middle_twenty.append(words[0:10])
    weight_text = []
    #print middle_twenty
    for i in xrange(len(t_list)):
        terms = middle_twenty[i]
        weight_list = []
        for j in xrange(len(t_list)):
            sub_weight_list = []
            for term_num in xrange(len(terms)):
                if i == j:
                    sub_weight_list.append(0)
                else:
                    sub_weight_list.append(t_list[j].get_freq_table().get_word_freq(terms[term_num]) - t_list[i].get_freq_table().get_word_freq(terms[term_num]))
            weight_list.append(sub_weight_list)
        weight_text.append(weight_list)

    final_weights = []
    for weight_vector in weight_text:
        other_weights = []
        #print len(weight_vector)
        for weight_subvector in weight_vector:
            other_weights.append(reduce(lambda x, y: x + y, weight_subvector))
        final_weights.append(other_weights)

    #print weight_text[0]
    return final_weights


# Given n topics and the weight vector
# derived above, run kmeans on the result
# and come up with the optimal centroids
# that correspond to a given text.
# Each centroid corresponds to a topic
def n_topics(text_list, w_l, n):
    km_input = whiten(numpy.matrix(w_l))
    num_cols = len(w_l[0])
    # for i in xrange(n):
    #     init_weights.append([0]*num_cols)
    #print numpy.array(init_weights)
    if len(w_l) > (1+n):
        m = w_l[1:(1+n)]
    else:
        m = n
    ret = kmeans(km_input, m)
    cent_assign = vq(km_input, ret[0])

    return cent_assign

def all_weights(text_list):
    b = burst_analysis(text_list)
    s = Text.simil_matrix(text_list)
    return numpy.concatenate((b, s), 1)

# Run n_topics up to #-of-texts / 2 times
# (i.e. we should have a minimum of 2 texts per topic)
# in order to find the configuration of centroids
# such that our data-point to centroid distortion
# is the lowest
# This is how we can find the optimal number of topics
# in a given text
def optimal_n(text_list, w_l):
    # Sane max num of topics is 20
    max_distort = 100000
    max_run = 0
    for i in xrange(len(text_list)/2):
        out_class = n_topics(text_list, w_l, i+1)
        class_distort = out_class[1]
        if min(class_distort) <= max_distort:
            max_run = i+1
            max_distort = min(class_distort)
    cent_assign = n_topics(text_list, w_l, max_run)

    return cent_assign[0]


# Helper function to find the distance between
# two weight vectors
def norm_distance(dist_vec):
    retval = 0
    for i in dist_vec:
        retval = retval + (i**i)
    return retval
