
def main_wordclouds():
    df = read_file()
    generate_annual_wordcloud_images(df, "abstract")
    generate_annual_wordcloud_images(df, "title")


def main_example():
    #df = read_sample(100)
    df = read_file()
    lsas = get_lsa_by_year(df)
    lsa_df = pd.DataFrame.from_dict({'year' : lsas.index,
                                     'lsa_terms' : [" ".join(a.terms) for a in lsas]})
    print lsa_df
    generate_annual_wordcloud_images(lsa_df, 'lsa_terms')
    #lsa_df = interesting_words(lsa)
    #p = bokeh_lsa(year, lsa_df)
    return

def main_msr_wordclouds():
    #df = read_file()
    df = read_sample(100)
    lsas = get_lsa_by_year(df)
    texts = df[['year', 'abstract']].groupby('year').sum()
    doc_dicts = []
    for year, lsa in lsas.iterkv():
        text = texts.ix[year]['abstract']
        words = interesting_words_1(lsa, 100)
        lsa_terms = set(words)
        processed_texts = " ".join([w for w in text.split() if w in lsa_terms])
        doc_dicts.append({"year": year, "lsa_abs": processed_texts})
    doc_df = pd.DataFrame(doc_dicts)
    make_output_dir("output/lsa_abs")
    for row, (abs, year) in doc_df.iterrows():
        generate_word_cloud_image(abs, "output/lsa_abs/"+year+".jpg")
