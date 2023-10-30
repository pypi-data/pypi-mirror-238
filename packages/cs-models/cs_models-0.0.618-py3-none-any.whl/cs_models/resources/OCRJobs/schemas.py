from marshmallow import (
    Schema,
    fields,
    validate,
)


class OCRJobResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    job_id = fields.String(required=True)
    bucket_name = fields.String(required=True)
    key_name = fields.String(required=True)
    updated_at = fields.DateTime()
