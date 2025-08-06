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
    pagerank = {}
    links = corpus[page]


    # get total number of pages in corpus
    total = len(corpus)

    if len(links) == 0:
        return {page: (1/total) for page in corpus}       

    # prob of random page
    random_page_prob = (1 - damping_factor) / total

    # getting list of all pages
    pages = list(corpus.keys())


    # adding prob for outgoing links
    for linked_page in pages:
        if linked_page in links:
            pagerank[linked_page] = damping_factor / len(links) + random_page_prob
        else:
            pagerank[linked_page] = random_page_prob

    return pagerank




def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_appear_count = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    current_page = random.choice(pages)
    for i in range(n):
        next_page_probs = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(next_page_probs.keys()), weights=list(next_page_probs.values()), k=1)[0]
        page_appear_count[current_page] += 1
        

    prob_dict = {}
    for page in page_appear_count:
        prob_dict[page] = page_appear_count[page] / n

    return prob_dict



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    total_pages = len(corpus)
    pagerank = {page: 1 / total_pages for page in corpus}

    while True:
        new_pagerank = {}
        for page in corpus:
            rank = (1 - damping_factor) / total_pages
            for linked_page in corpus:
                if len(corpus[linked_page]) == 0:
                    rank += damping_factor * pagerank[linked_page] / total_pages
                if page in corpus[linked_page]:
                    rank += damping_factor * pagerank[linked_page] / len(corpus[linked_page])
            new_pagerank[page] = rank
        
        if all(abs(new_pagerank[page] - pagerank[page]) < 0.001 for page in corpus):
            return new_pagerank
        
        pagerank = new_pagerank
        


if __name__ == "__main__":
    main()
