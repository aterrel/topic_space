
def bokeh_lsa(year, df):
    plt.output_file('output/lsa/'+str(year)+'.html')

    topics = [str(a) for a in df.columns]
    words = list(to_str(df.index))
    p = plt.figure(x_range=topics, y_range=words,
           plot_width=800, plot_height=600,
           title=year, tools='resize, save')

    plot_sizes = []
    plot_topics = []
    plot_words = []
    print df
    for word, coeff in df.iterrows():
        for n, c in enumerate(coeff):
            if c > 0:
                plot_sizes.append(c)
                plot_topics.append(str(n))
                plot_words.append(word)
    if len(plot_sizes) == 0:
        return
    max_size = np.max(plot_sizes)
    plot_sizes = [int(a/max_size * 75) + 25 for a in plot_sizes]

    print plot_sizes, plot_words, plot_topics

    p.circle(x=plot_topics, y=plot_words, size=plot_sizes, fill_alpha=0.6)
    plt.show(p)

    return plt.curplot()
