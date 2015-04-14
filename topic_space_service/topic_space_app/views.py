from django.shortcuts import render
from django.http import HttpResponse

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.templates import RESOURCES
from bokeh.utils import encode_utf8
from wordcloud import WordCloud

from topic_space.wordcloud_generator import FONT_PATH, get_docs_by_year, read_file
from topic_space_app.models import WordCloudRequest


DOCS_DF = get_docs_by_year()
DF = read_file()


def index(request):
    return HttpResponse("Hello, world. You're at the topic space index.")


def wordcloud(request):
    #import pdb; pdb.set_trace()
    #print("in wordcloud")
    year1 = "2014" #request.values.get('year1','1980')
    year2 = "2014" #request.values.get('year2', '2014')
    stop_words = "film\n structure" #map(lambda x: x.strip(), request.values.get('words','').split('\n'))
    r = WordCloudRequest(start_year=year1, end_year=year2, stop_words=stop_words)
    r.save()
    context = {"year1": year1, "year2": year2, "stop_words": stop_words.split("\n")}
    return render(request, 'wordcloud.html', context)


def get_wordcloud(request, request_id):
    r = WordCloudRequest.objects.get(id=request_id)
    year1, year2, stop_words = r.start_year, r.end_year, r.stop_words
    year_list = map(str, range(int(year1), int(year2)+1))
    #text = DOCS_DF[DOCS_DF['year'].isin(year_list)]['lsa_abs'].sum()
    #for word in stop_words:
    #    text = text.replace(word, '')
        #wordcloud = WordCloud(font_path=FONT_PATH, width=800, height=600).generate(text)
    #img_io = StringIO()
    #wordcloud.to_image().save(img_io, 'JPEG', quality=70)
    #img_io.seek(0)
    #return send_file(img_io, mimetype='image/jpeg')
    return HttpResponse("Year %s to %s, without %s"  % (year1, year2, stop_words,))


colors = {
    'Black': '#000000',
    'Red':   '#FF0000',
    'Green': '#00FF00',
    'Blue':  '#0000FF',
}


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]

def histogram():
    # Grab the inputs arguments from the URL
    # This is automated by the button
    args = request.args

    # Get all the form arguments in the url with defaults
    color = colors[getitem(args, 'color', 'Black')]
    _from = int(getitem(args, '_from', 0))
    to = int(getitem(args, 'to', 10))

    count_df = DF[['year', 'abstract']].groupby('year').count()
    count_df = count_df.drop("January 2000")
    fig = figure(title="Histogram of Docs Per Year")
    fig.line(map(int, count_df.index), list(count_df['abstract']), color=color, line_width=2)

    # Configure resources to include BokehJS inline in the document.
    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/reference/resources_embedding.html#module-bokeh.resources
    plot_resources = RESOURCES.render(
        js_raw=INLINE.js_raw,
        css_raw=INLINE.css_raw,
        js_files=INLINE.js_files,
        css_files=INLINE.css_files,
    )

    # For more details see:
    #   http://bokeh.pydata.org/en/latest/docs/user_guide/embedding.html#components
    script, div = components(fig, INLINE)
    html = render_template(
        'histogram.html',
        plot_script=script, plot_div=div, plot_resources=plot_resources,
        color=color, _from=_from, to=to
    )
    return encode_utf8(html)




