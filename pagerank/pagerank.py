""" Assignment 6: PageRank. """
from collections import defaultdict
import glob
from bs4 import BeautifulSoup


def parse(folder, inlinks, outlinks):
    """
    Read all .html files in the specified folder. Populate the two
    dictionaries inlinks and outlinks. inlinks maps a url to its set of
    backlinks. outlinks maps a url to its set of forward links.
    """
    fold = folder + "/*.html"
    files = glob.glob(fold)
    for num,each in enumerate(files):
        soup = BeautifulSoup(open(each))
        link_list = soup.find_all('a')
        for every in link_list:
            outlinks[folder+"/"+each[5:]].add(folder+"/"+every.get('href'))
            inlinks[folder+"/"+every.get('href')].add(folder+"/"+each[5:])
    return

def compute_pagerank(urls, inlinks, outlinks, b=.85, iters=20):
    """ Return a dictionary mapping each url to its PageRank.
    The formula is R(u) = 1-b + b * (sum_{w in B_u} R(w) / (|F_w|)

    Initialize all scores to 1.0
    """
    page_rank = defaultdict(lambda: 1.0)
    for i in range(0,iters):
        for each in urls:
            sumwinbu = 0.
            for every in inlinks[each]:
                sumwinbu += 1.0 * page_rank[every]/len(outlinks[every])
            page_rank[each] = 1.0 - b + (1.0 * b * sumwinbu)
    return page_rank

def run(folder, b):
    """ Do not modify this function. """
    inlinks = defaultdict(lambda: set())
    outlinks = defaultdict(lambda: set())
    parse(folder, inlinks, outlinks)
    urls = sorted(set(inlinks) | set(outlinks))
    ranks = compute_pagerank(urls, inlinks, outlinks, b=b)
    print 'Result for', folder, '\n', '\n'.join('%s\t%.3f' % (url, ranks[url]) for url in sorted(ranks))


def main():
    """ Do not modify this function. """
    run('set1', b=.5)
    run('set2', b=.85)


if __name__ == '__main__':
    main()
