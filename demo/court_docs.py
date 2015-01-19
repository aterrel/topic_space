

def read_court_files(folder_path):
    import glob
    files = glob.glob(folder_path + "/*")
    texts = []
    for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        try:
            with open(name) as f: # No need to specify 'r': this is the default.
                texts.append(f.read())
        except IOError as exc:
            pass
    return texts


def get_lsa(texts):
    docs = [pv.Document(a) for a in texts]
    model = pv.Model(docs, weight=pv.TFIDF)
    lsa = model.reduce(2)
    return lsa


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def main_court_lsa_words():
    texts = read_court_files("court")
    lsa_terms = " ".join(get_lsa(texts).terms)
    generate_word_cloud_image(lsa_terms, "output/court_doc")


def main_court_minus_lsa_words():
    texts = read_court_files("court")
    words = interesting_words_1(get_lsa(texts), 100)
    lsa_terms = set(words)
    processed_texts = [w for w in flatten_list([t.split() for t in texts]) if w in lsa_terms]
    doc = " ".join(processed_texts)
    generate_word_cloud_image(doc, "output/court_doc.jpg")

