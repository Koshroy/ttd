from Text import *
import sys
import burstiness

def main():
    if len(sys.argv) < 2:
        print "Usage: python main.py <text-list.txt>"
        print "text-list.txt: A list of text files for classification"
        return
    
    f_list = sys.argv[1]
    list_text = []
    f = open(f_list)
    for line in f:
        if line.strip('\n') != '':
            list_text.append(line.strip('\n'))
    #[topic1, topic2] = cluster_list(list_text)

    text_obj_list = [Text(i) for i in list_text]
    for i in text_obj_list:
        i.build_freq_table()
    weight_vec = burstiness.all_weights(text_obj_list)
    #text_class = burstiness.n_topics(list_text, weight_vec, 5)
    n_rank = burstiness.optimal_n(list_text, weight_vec)

    n_topics_dict = {}
    for i in xrange(len(n_rank)):
        if n_rank[i] in n_topics_dict:
            old_topic = n_topics_dict[n_rank[i]]
            old_topic.append(list_text[i])
            n_topics_dict[n_rank[i]] = old_topic
        else:
            n_topics_dict[n_rank[i]] = [list_text[i]]

    for i in n_topics_dict:
        print "=== Topic #" + str(i+1) + " contains ==="
        for l in n_topics_dict[i]:
            print l
            


    # print "=== Texts in topic1 === "
    # for f in topic1:
    #     print f
    # print "=== Texts in topic2 === "
    # for f in topic2:
    #     print f
    
    

if __name__ == "__main__":
    main()

