import marshmallow as ma



class UIPropertySchema(ma.Schema):
    detail = ma.fields.String()


class UIObjectSchema(UIPropertySchema):
    pass
