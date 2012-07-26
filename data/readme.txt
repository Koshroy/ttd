Koushik Roy

5/10/12 -- Final Final Submission

I previously thought that the last submission was the final submission
due to some error of mine.

Attempts:

1. Tried to change the topic determiner to split each sub-topic into
two until a fine-grained amount of topics were found. The previous
error threshold was found of the superset, and the subset error
thresholds were compared against this error threshold to determine
whether to keep the split or not. Unfortunately, this resulted in
erroneous splitting.

1a. Made modifications to the binning algorithm that would break
ties and choose a better random seed. This produced much better results.

2. Cleaned up a lot of code that generated similarity.

3. Decided not to implement a Zipf distribution.

4. Incorporated the similarity matrix along with the burstiness matrix
in order to determine topicality.

5. Please look at Final Submission notes.

Results:

Topical data is indeed classified well.

Example (given) Output:

=== Topic #1 contains ===
anandtech-nvidia-sklavos.txt
anandtech-nvidia-smith.txt
fa-china-glowing-pork.txt
fa-china-challenge.txt
=== Topic #2 contains ===
anandtech-sklavos.txt
=== Topic #3 contains ===
anandtech-nvidia-500mrefresh-walton.txt
=== Topic #4 contains ===
anandtech-nvidia-lal-email.txt
=== Topic #5 contains ===
anime-utena-review-windimage.txt
=== Topic #6 contains ===
anime-utena-review-razorx.txt
ee-surround-psycho-p1.txt
ee-surround-psycho-p2.txt
ee-asml-euv-progress.txt
ee-asml-euv-track.txt
=== Topic #7 contains ===
air-review-albinosqrl.txt
=== Topic #8 contains ===
air-review-pantha.txt
=== Topic #9 contains ===
saikano-review-requiem.txt
=== Topic #10 contains ===
saikano-review-wtx.txt
=== Topic #11 contains ===
fa-beijing.txt
fa-cuba-timewarp.txt
fa-obamas-tango.txt
fa-iran-regime-change.txt
fa-not-attack-iran.txt
fa-flawed-strike-iran.txt
=== Topic #12 contains ===
fa-egypt.txt

Topic 1 needs to be split to seperate AnandTech and Foreign Affairs
articles. Topics2-4 need to be joined (indicates uncertainty on the
part of the algorithm). anime-utena-review-razorx needs to be removed
from Topic #6 and merged with #5 in order to group them in a coherent
topic, other than that Topic #6 is correct. Topics #7-8 need to be
combined. Likewise with Topics #9-10. Topic #11 and #12 are correct.
Overall, the text classifier did much better than I had hoped. It
seems to classify highly topical data (in this case, seperating data
about politics, from Electrical Engineering articles and Computer
Hardware blogs) into different topics, although has trouble by either
lumping topics in too broadly, or splitting out a topic too finely. I
feel that the data that is needed to make a good choice is present,
but given more time, would work on the clustering algorithm to try and
cluster the data better.


4/19/2012 -- Final Submission

1. Made refinements to the burstiness algorithm to decrease false
positives. Input data set has been increased, and the number of topics
detected has also been increased. The next step will be to run the
burstiness and similarity algorithms multiple times until we converge
upon an ideal number of topics.

2. In order to dynamically determine the number of topics that should
result in an optimal classification, I decided to run the algorithm
multiple times. Each time I had access to a set of distortion values
that tracked the distortion of each data point to its assigned
centroid. The *minimum* value of these distortions was obtained and
tracked. If on a subsquent run the minimum distortion was less than
the minimum distortion of a previous run, then that run was considered
the current most optimal run. Running the algorithm a max of
#-of-text/2 times (i.e. there could be at most 2 topics per topic), I
was able to come up with a maximum number of topics.

3. Performance was not as well as I had hoped. Often times multiple
topics that the human is aware of are lumped together into a single
topic. Curiously enough, this topic seems to contain texts that is
strictly the union of texts in human-identified topics. I played
around with ways to come up with a more fine-grained set of topics,
but I could not come up with a better way of producing consistent,
good results.

4. The testing was done on a set of 25 different texts of varying
topics. The longer the length of the text, the more consistently
correctly the text was binned into the correct topic. The shortet
anime-review texts that I included had the most trouble in
classification, while the long essays I included from Foreign Affairs
Magazine were easily classified.

5. Added comments to the burstiness.py library.

4/12/2012

Added a new way to rank topicality based on n-topics (which must be
provided statically) in order to track burstiness. Burstiness seems to
classify 3 different, robust topics quite well within the set of input
parameters (2 known/provided topics and a single miscellaneous
topic). Code has been added into a new module and the new ranking
mechanism is demonstrated.


4/5/2012

Minor updates to the functionality. Similarity is now calculated using
a hypothetical "average frequency distribution" that is built up from
the constituent texts. This new averaging scheme produces much tighter
centroids and, at least to human analysis, can recognize three
different means inside the K-means implementation.

Code has been commented and old code has been cleaned up.


3/27/2012

=== Explanation and Usage == 

The attached code can classify text into two topical categories. To
use the program, simply give it an argument containing a newline
separated list of text files which contain text belonging to one of
two topics. Sample text files have been given upon which the
classifier has shown to succeed well upon. The text for both
categories have been obtained through the web. The first is a set of
articles appearing on the popular computer hardware review blog
AnandTech regarding the release of Nvidia graphics cards. The second
is a set of articles reviewing a Japanese animation titled "Utena"
available on the AniDB anime database. Both of these categories are
highly separate in topic matter and have little in common.


=== Implementation Details === 

In order to identify the topicality of texts, a cosine-similarity rating
is used between terms in two different texts. Most papers that I
encountered said that along with word-rank similarity, an equally
fundamental parameter was the relative burstiness of common, uncommon,
and rare words. Most telling was the distribution of uncommon
words. Therefore my implementation currently only keeps track of the
cosine-similarity based on terms encountered below the first ten
ranks. These uncommon words can differentiate highly topical texts,
while excluding more common words common to all English texts.

Cosine-similarity is calculated in respect to a single respect. Each
of these similarities are indexed, and then the K-Means clustering
algorithm is run upon the results. The clustering identifies two
different centroids of given similarity means. By finding which
centroid is "closer" for a given text's similarity rating, the texts
may be classified into one or another topic.

=== Further Work ===

I plan to also incorporate a proper measurement of relative ranking
between common, uncommon, and rare words ("burstiness") as a second
parameter, and Zipf distribution coefficients as a third parameter. To
facilitate ranking between multiple topics, I would like to use
Principle Component Analysis and determine how much varying is
ocurring between the parameters and use K-Means to try and cluster
into each of these centroids.

