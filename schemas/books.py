from datetime import date
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator


# common properties
class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str]
    publication_date: Optional[date]

    @validator("title", always=True)
    def validate_title(cls, value):
        title = value
        min_length = 3
        errors = ""
        if len(title) < min_length:
            errors += "Valid title must be provided. "
        if errors:
            raise ValueError(errors)
        return value

    @validator("author", always=True)
    def validate_author(cls, value):
        title = value
        min_length = 3
        errors = ""
        if len(title) < min_length:
            errors += "Valid author must be provided. "
        if errors:
            raise ValueError(errors)
        return value


#  Create a Book
class BookCreate(BookBase):
    date_posted: Optional[date] = datetime.now().date()

    # @classmethod
    # def add_fields(cls, **field_definitions: Any):
    #     new_fields: Dict[str, Field] = {}
    #     new_annotations: Dict[str, Optional[type]] = {}

    #     for f_name, f_def in field_definitions.items():
    #         if isinstance(f_def, tuple):
    #             try:
    #                 f_annotation, f_value = f_def
    #             except ValueError as e:
    #                 raise Exception(
    #                     'field definitions should either be a tuple of (<type>, <default>) or just a '
    #                     'default value, unfortunately this means tuples as '
    #                     'default values are not allowed'
    #                 ) from e
    #         else:
    #             f_annotation, f_value = None, f_def

    #         if f_annotation:
    #             new_annotations[f_name] = f_annotation

    #         new_fields[f_name] = Field.infer(name=f_name, value=f_value, annotation=f_annotation, class_validators=None, config=cls.__config__)

    #     cls.__fields__.update(new_fields)
    #     cls.__annotations__.update(new_annotations)


# return book
class ShowBook(BookBase):
    id: int
    publication_date: date
    cover_path: Optional[str] = None

    class Config:
        orm_mode = True


# Model for dashboard summary
class Summary(BaseModel):
    count: int
    books: List[ShowBook]
