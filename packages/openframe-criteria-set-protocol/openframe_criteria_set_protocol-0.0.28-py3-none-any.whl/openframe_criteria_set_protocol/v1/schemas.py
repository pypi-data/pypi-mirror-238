from marshmallow import Schema, fields

criteria_set_id = r'^[a-zA-Z0-9.\-_]+$'
version = r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'


class TreeAndMatrixBodySchema(Schema):
    locale = fields.Str(required=False)
    values = fields.Dict(required=True)
    parameters = fields.Dict(required=True)

