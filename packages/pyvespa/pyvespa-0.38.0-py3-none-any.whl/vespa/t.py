
from vespa.package import ApplicationPackage, Field, FieldSet, RankProfile
from vespa.deployment import VespaDocker
from pandas import read_csv

app_package = ApplicationPackage(name="textsearch")

app_package.schema.add_fields(
    Field(name="id",    type="string", indexing=["attribute", "summary"]),
    Field(name="title", type="string", indexing=["index", "summary"], index="enable-bm25"),
    Field(name="body",  type="string", indexing=["index", "summary"], index="enable-bm25")
)

app_package.schema.add_field_set(
    FieldSet(name="default", fields=["title", "body"])
)

app_package.schema.add_rank_profile(
    RankProfile(name="bm25", first_phase="bm25(title) + bm25(body)")
)
app_package.schema.add_rank_profile(
    RankProfile(name="native_rank", first_phase="nativeRank(title, body)")
)

vespa_docker = VespaDocker()
app = vespa_docker.deploy(application_package=app_package)

docs = read_csv(
    filepath_or_buffer="https://data.vespa.oath.cloud/blog/msmarco/sample_docs.csv"
).fillna('')
docs.head()

for x in range(50):
    print("iteration: " + str(x))
    feed_res = app.feed_df(docs, asynchronous=False, batch_size=1000)
