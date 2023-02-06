from sqlmodel import Field, SQLModel, Relationship


class BaseUser(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    age: int


class OutputUser(BaseUser):
    pets: list['Pet']


class User(BaseUser, table=True):
    pets: list['Pet'] = Relationship(back_populates='owner')


class BasePet(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    sound: str


class OutputPet(BasePet):
    owner: User


class Pet(BasePet, table=True):

    owner_id: int | None = Field(default=None, foreign_key="user.id")
    owner: User = Relationship(back_populates='pets')


OutputUser.update_forward_refs()
User.update_forward_refs()
