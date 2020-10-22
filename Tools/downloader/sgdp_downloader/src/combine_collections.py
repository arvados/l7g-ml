import arvados
import arvados.collection
api = arvados.api()
project_uuid = "su92l-j7d0g-564z7zxkttp3vih"
collection_uuids = ["su92l-4zz18-c3wnxzg56doxaxv", "su92l-4zz18-c7f9t14zqmthlx2"]
combined_manifest = ""
for u in collection_uuids:
    c = api.collections().get(uuid=u).execute()
    combined_manifest += c["manifest_text"]
newcol = arvados.collection.Collection(combined_manifest)
newcol.save_new(name="Simons Diversity Data", owner_uuid=project_uuid)