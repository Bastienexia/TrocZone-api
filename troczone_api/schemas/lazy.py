import strawberry

UserSchema = strawberry.LazyType["User", "troczone_api.schemas"]
PostSchema = strawberry.LazyType["Post", "troczone_api.schemas"]