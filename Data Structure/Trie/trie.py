from collections import defaultdict

trie_fac = lambda: defaultdict(trie_fac)
trie = trie_fac()

def trie_insert(trie, word):
    cur = trie
    for c in word:
        cur = cur[c]
    cur[''] = True

def trie_search(trie, word):
    cur = trie
    for c in word:
        if c not in cur:
            return False
        cur = cur[c]
    return True

def trie_startswith(trie, prefix):
    cur = trie
    for c in prefix:
        if c not in cur:
            return False
        cur = cur[c]
    return True

def trie_delete(trie, word):
    cur = trie
    for c in word:
        if c not in cur:
            return False
        cur = cur[c]
    if '' in cur:
        cur.pop('')
        return True
    return False
