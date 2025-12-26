from feast import Entity

user = Entity(
    name="user",
    join_keys=["user_id"],
    description="Entité principale StreamFlow : un utilisateur (client) identifié de façon unique par user_id.",
)
