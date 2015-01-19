
from wordcloud import WordCloud


def generate_annual_wordclouds(df, field):
    abstract_series = df[["year", field]].groupby("year").agg(np.sum)
    wordclouds = []
    for year in abstract_series.index:
        abstract = abstract_series.ix[year][field]
        wordclouds.append((year, WordCloud(font_path=FONT_PATH).generate(abstract)))
    return wordclouds


def generate_word_cloud_image(text, filename="output/wordcloud.jpg"):
    wordcloud = WordCloud(font_path=FONT_PATH).generate(text)
    wordcloud.to_image().save(filename, "JPEG")


def generate_annual_wordcloud_images(df, field):
    make_output_dir(os.path.join("output", field))
    wcs = generate_annual_wordclouds(df, field)
    for year, wordcloud in wcs:
        wordcloud.to_image().save(os.path.join("output", field, year+".jpg"), "JPEG")


def wordclouds_to_bokeh(wordclouds):
    plt.output_file("wordclouds.html", title="Wordclouds of Abstracts 1by Year")
    images = [w.to_image() for y, w in wordclouds]
    p = plt.figure(x_range=[0, 10], y_range=[0, 10])
    # XXX: Need to figure out how to put images in
    p.image(image=images, x=range(len(images)), y=[0]*len(images), dw=[10]*len(images), dh=[10]*len(images), palette="Spectral11")

    plt.show(p)
