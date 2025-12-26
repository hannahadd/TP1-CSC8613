from fastapi import FastAPI
from feast import FeatureStore

app = FastAPI()

# Le repo Feast est monté dans /repo via docker-compose
store = FeatureStore(repo_path="/repo")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/features/{user_id}")
def get_features(user_id: str):
    features = [
        "subs_profile_fv:months_active",
        "subs_profile_fv:monthly_fee",
        "subs_profile_fv:paperless_billing",
    ]

    feature_dict = store.get_online_features(
        features=features,
        entity_rows=[{"user_id": user_id}],
    ).to_dict()

    # to_dict() renvoie des listes (même pour 1 user). On transforme en scalaires.
    simple = {k: v[0] for k, v in feature_dict.items() if k != "user_id"}

    return {"user_id": user_id, "features": simple}
