

def make_output_dir(dir_name="output"):
    try:
        os.mkdir(dir_name)
    except OSError:
        pass


def read_file():
    list_of_dicts = []
    with open(DATA_FILE, 'r') as fp:
        for line in fp.readlines():
            try:
                list_of_dicts.append(json.loads(line))
            except ValueError:
                print("Unable to process line:\n\t", line)
    return pd.DataFrame(list_of_dicts)


def read_sample(n=10):
    df = read_file()
    rows = random.sample(df.index, n)
    return df.ix[rows]


def get_abstracts_by_year(df):
    abstracts = {}
    grouped = df.groupby('year')
    for year, pks in grouped.groups.iteritems():
        abstracts[year] = df.loc[pks]
    return abstracts


def create_Kane_csv(df):
    """
    CSV Columns:
    title, abstract, url, year, author
    """

    df.to_csv("msr_data.csv", columns=["title", "abstract", "url", "year", "authors"], encoding="utf-8")


def to_str(wordlist):
    for a in wordlist:
        try:
            yield str(a)
        except UnicodeEncodeError:
            pass

