import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

'''
def main():
    """
    a test main for functions
    """
    corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "1.html"
    damping_factor = 0.85
    transition_model_test = transition_model(corpus, page, damping_factor)
    print(transition_model_test)
'''
    

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_possibility = {}
    if len(corpus[page]) == 0:
        for page_i in corpus.keys():
            page_possibility.update({page_i:1 / len(corpus)})
        return page_possibility
    default_possibility = (1-damping_factor) / len(corpus.keys())
    for page_i in corpus.keys():
        page_possibility.update({page_i:default_possibility})
    possible_pages = corpus[page]
    extra_possibility = damping_factor / len(possible_pages)
    for page_i in possible_pages:
        page_possibility[page_i] += extra_possibility
    return page_possibility


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(corpus.keys(), 0)
    page = random.choice(list(corpus.keys()))
    pagerank[page] += 1
    for _ in range(n-1):
        estimate_model = transition_model(corpus, page, damping_factor)
        rand = random.randint(0, 99) / 100
        sum_possibility = 0
        for page in corpus.keys():
            sum_possibility += estimate_model[page]
            if sum_possibility < rand:
                continue
            else:
                pagerank[page] += 1
                break
    for page in pagerank.keys():
        pagerank[page] /= n
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(corpus.keys(), 1 / len(corpus))
    links_num = {p: len(corpus[p]) for p in corpus.keys()}

    flag = True
    while flag:
        flag = False
        newrank = {}
        for page in pagerank.keys():
            total_possibility = sum([pagerank[page_i] / links_num[page_i] 
                                     for page_i in pagerank.keys() if links_num[page_i] > 0 and page in corpus[page_i]])
            newrank[page] = (1-damping_factor) / len(corpus) + total_possibility * damping_factor
            if abs(newrank[page] - pagerank[page]) > 1e-3:
                flag = True 
        for page in pagerank.keys():
            pagerank[page] = newrank[page]
    return pagerank


if __name__ == "__main__":
    main()
