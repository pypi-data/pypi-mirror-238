from lime_filter import Filter, OrOperator, EqualsOperator
from lime_filter.filter import LikeOperator
from lime_type.unit_of_work import _serialize_properties_and_values
from lime_type.limeobjects import (
    BelongsToPropertyAccessor,
    OptionPropertyAccessor,
    SetPropertyAccessor,
    HasManyPropertyAccessor,
)
from lime_application import get_application, list_applications
from lime_admin.plugins import load_config
import json


def get_filter(limetype_config, value):
    filter = None
    for key, field in limetype_config.items():
        if key == "limetype":
            continue
        operator = LikeOperator(field, value)
        if not filter:
            filter = operator
            continue
        filter = OrOperator(operator, filter)
    return Filter(filter)


def search_lime_objects(app, limetype_ref, search, limit, offset):
    limetype_config = get_plugin_config(app)[limetype_ref]
    limeobject = app.limetypes.get_limetype(limetype_config["limetype"])
    if "company_name" in limetype_config:
        limetype_config.pop("company_name")
    filter = get_filter(limetype_config, search)
    return [
        _serialize_properties_and_values(get_limetype_fields(obj, app))
        for obj in limeobject.get_all(filter=filter, limit=limit, offset=offset)
    ]

def search_lime_persons(app, search, limit, offset):
    limetype_config = {
        "limetype": "person",
        "first_name": "firstname",
        "last_name": "lastname",
        "email": "email",
        "phone": "mobilephone",
        "company": "company",
    }
    use_default_persons_object = get_plugin_config(app)['use_default_persons_object']
    if use_default_persons_object:
        limetype = app.limetypes.get_limetype('person')
        filter = get_filter(limetype_config, search)
        return [_serialize_properties_and_values(get_limetype_fields(obj, app, limetype_config))
                for obj in limetype.get_all(
                    filter=filter, limit=limit, offset=offset
        )]
    else: 
        return []


def get_documents(app, limetype, record_id):
    documents = app.limetypes.get_limetype("document").get_all(
        filter=Filter(EqualsOperator(limetype, record_id))
    )
    return [dict(**doc.values(), id=doc.id) for doc in documents]


def get_contacts_for_current_limetype(app, limetype, record_id):
    config = get_plugin_config(app)
    current_limetype = app.limetypes.get_limetype(limetype).get(record_id)
    properties = current_limetype.properties
    has_company = hasattr(properties, config["company"]["limetype"])
    related_company = (
        getattr(properties, config["company"]["limetype"]) if has_company else None
    )

    if limetype == config["company"]["limetype"]:
        contacts = app.limetypes.get_limetype(config["person"]["limetype"]).get_all(
            filter=Filter(EqualsOperator(limetype, record_id))
        )
    elif related_company:
        contacts = app.limetypes.get_limetype(config["person"]["limetype"]).get_all(
            filter=Filter(
                EqualsOperator(
                    config["company"]["limetype"], getattr(related_company, "id", None)
                )
            )
        )
    else:
        contacts = []
    return [
        _serialize_properties_and_values(get_limetype_fields(contact, app))
        for contact in contacts
    ]


def match_merge_fields(limeobject, data):
    fields = data.get("fields", [])
    for field in fields:
        value = get_merge_field_value(limeobject, field)
        field.update(
            {
                "field_label": field.get("field_label") or field.get("field_value"),
                "field_value": value,
            }
        )
    return fields


def get_file_data(app, document_id):
    document = app.limetypes.get_limetype("document").get(document_id)
    return document.properties.document.fetch()


def get_merge_field_value(limeobject, field):
    try:
        key = field["field_value"].replace("{{", "").replace("}}", "")

        value = _serialize_properties_and_values(get_lime_values(limeobject))[key]
        return value
    except Exception:
        return field["field_value"]


def extract_value(prop, fetch_nested=True):
    if isinstance(prop, BelongsToPropertyAccessor):
        nested_obj = prop.fetch()
        if not nested_obj or not fetch_nested:
            return prop.descriptive
        return {
            nested_prop.name: extract_value(nested_prop, False)
            for nested_prop in nested_obj.get_properties_with_value()
        }
    if isinstance(prop, OptionPropertyAccessor):
        return prop.value.key
    if isinstance(prop, SetPropertyAccessor):
        return [p.key for p in prop.value]
    if isinstance(prop, HasManyPropertyAccessor):
        if not fetch_nested:
            return prop.value
        result = []
        for nested_obj in prop.fetch():
            properties_dict = {
                nested_prop.name: extract_value(nested_prop, False)
                for nested_prop in nested_obj.get_properties_with_value()
            }
            result.append(properties_dict)
        return result
    return prop.value


def get_lime_values(limeobject):
    props = limeobject.properties

    def get_prop_names_to_ignore():
        ignored_props = {"*": ["history", "todo"]}
        return ignored_props.get(limeobject.limetype.name, ignored_props.get("*", []))

    values = {}

    for prop in props:
        if prop.name in get_prop_names_to_ignore():
            continue
        value = extract_value(prop)

        if isinstance(value, dict):
            for k, v in value.items():
                values[f"{prop.name}.{k}"] = v
        elif isinstance(value, list):
            for i, item in enumerate(value, 1):
                if isinstance(item, str):
                    values[f"{prop.name}.{i}"] = item
                else:
                    for k, v in item.items():
                        values[f"{prop.name}{i}.{k}"] = v

        else:
            values[f"{limeobject.limetype.name}.{prop.name}"] = value

    return values


def get_limetype_fields(obj, app, config=None):
    fields = {}
    props = obj.properties
    default_key = "company"
    for key, object in get_plugin_config(app).items():
        if not isinstance(object, dict):
            continue
        if object["limetype"] == obj.limetype.name:
            default_key = key
            break
    if not config:
        config = get_plugin_config(app)[default_key]
    for key, object_key in config.items():
        if key in ["company", "company_name"]:
            continue
        related_property = next(
            (prop for prop in props if prop.name == object_key), None
        )
        if not related_property:
            continue
        fields[key] = extract_value(related_property)
    if config.get("company_name"):
        related_company = getattr(obj.properties, config["company"], None)
        if related_company:
            related_company_object = related_company.fetch()
            if related_company_object:
                fields["company"] = getattr(
                    related_company.fetch().properties, config["company_name"]
                ).value
        else:
            fields["company"] = ""
    fields["lime_id"] = obj.id
    return fields


def get_plugin_config(app):
    default_config = {
        "use_custom_config": False,
        "use_default_persons_object": False,
        "company": {
            "limetype": "company",
        },
        "person": {
            "limetype": "person",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "email",
            "phone": "mobilephone",
            "company": "company",
            "company_name": "name",
        },
        "coworker": {
            "limetype": "coworker",
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "email",
            "phone": "mobilephone",
        },
    }
    try:
        config = json.loads(load_config(app, "limepkg_getaccept", 1))

        return config if config.get("use_custom_config") else default_config
    except:
        return default_config
