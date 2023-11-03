from marshmallow import Schema, fields
from lime_type.fields import LimeTypeField, LimePropertyField


def create_schema(application):
    class CompanySchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            title='Company limetype',
            description='Choose limetype which represents a company'
        )

    class PersonSchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            title='Person limetype',
            description='Choose limetype which represents a person'
        )
        first_name = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='First name',
            description='Limetype property which represents first name'
        )
        last_name = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Last name',
            description='Limetype property which represents last name'
        )
        email = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Email',
            description='Limetype property which represents email'
        )
        phone = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Phone',
            description='Limetype property which represents phone'
        )
        company = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Company',
            description='Limetype property which represents company'
        )
        company_name = LimePropertyField(
            application=application,
            limetype_field='company',
            title='Company name',
            description='Limetype property which represents company'
        )

    class CoworkerSchema(Schema):
        class Meta:
            ordered = True

        limetype = LimeTypeField(
            application=application,
            title='Coworker limetype',
            description='Choose limetype which represents a user'
        )
        first_name = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='First name',
            description='Limetype property which represents first name'
        )
        last_name = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Last name',
            description='Limetype property which represents last name'
        )
        email = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Email',
            description='Limetype property which represents email'
        )
        phone = LimePropertyField(
            application=application,
            limetype_field='limetype',
            title='Phone',
            description='Limetype property which represents phone'
        )

    class GetacceptEsigningConfigSchema(Schema):
        class Meta:
            ordered = True

        use_custom_config = fields.Boolean(
            title='Use custom config',
            description='Enable/disable usage of the custom config for custom limetypes'
        )

        use_default_persons_object = fields.Boolean(
            title='Use default persons object',
            description='Enable/disable usage of the default persons object for contacts searching'
        )
        company = fields.Nested(title='Company', nested=CompanySchema)
        person = fields.Nested(title='Person', nested=PersonSchema)
        coworker = fields.Nested(title='Coworker', nested=CoworkerSchema)

    return GetacceptEsigningConfigSchema()
