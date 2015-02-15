## Webcrawler for arxiv.com

# Purpose
The webcrawler was written in order to gain experience with python as well as to be able to build a bipartite author-paper network with timestamps (date the paper was published)

# Explanation in respect to the admins of arxiv.com
First of all I want to explain that the arxiv website forbids extensive crwaling of their website.
The webpage should be available for human activities not onlinefor robots.
With respect to this I set a delay of several seconds.

# What does it do?
Beginning from one article on the arxiv website (given in startingurl) the web crwaler searches up to 5 authors and for each author we get a list of at most 10 papers in which he or she participated.
The program queues every link to a paper.

The program saves the date, the subject, the authors(5 at most) and the arxiv ID to local mongoDB instance
