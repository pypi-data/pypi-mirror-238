import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.validate import OneOf
from oarepo_runtime.i18n.ui_schema import (
    I18nStrUIField,
    MultilingualLocalizedUIField,
    MultilingualUIField,
)
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedEDTF

from nr_metadata.common.services.records.ui_schema_datatypes import (
    NRAccessRightsVocabularyUISchema,
    NRAffiliationVocabularyUISchema,
    NRAuthorityRoleVocabularyUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationUISchema,
    NRLanguageVocabularyUISchema,
    NRLicenseVocabularyUISchema,
    NRRelatedItemUISchema,
    NRResourceTypeVocabularyUISchema,
    NRSeriesUISchema,
    NRSubjectCategoryVocabularyUISchema,
    NRSubjectUISchema,
)
from nr_metadata.ui_schema.identifiers import (
    NRAuthorityIdentifierUISchema,
    NRObjectIdentifierUISchema,
    NRSystemIdentifierUISchema,
)
from nr_metadata.ui_schema.subjects import NRSubjectListField


class NRCommonRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRCommonMetadataUISchema())


class NRCommonMetadataUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    abstract = MultilingualUIField(I18nStrUIField())

    accessRights = ma_fields.Nested(lambda: NRAccessRightsVocabularyUISchema())

    accessibility = MultilingualLocalizedUIField(I18nStrUIField())

    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesUISchema())
    )

    contributors = ma_fields.List(ma_fields.Nested(lambda: NRContributorUISchema()))

    creators = ma_fields.List(
        ma_fields.Nested(lambda: NRCreatorUISchema()), required=True
    )

    dateAvailable = LocalizedEDTF()

    dateModified = LocalizedEDTF()

    events = ma_fields.List(ma_fields.Nested(lambda: NREventUISchema()))

    externalLocation = ma_fields.Nested(lambda: NRExternalLocationUISchema())

    fundingReferences = ma_fields.List(
        ma_fields.Nested(lambda: NRFundingReferenceUISchema())
    )

    geoLocations = ma_fields.List(ma_fields.Nested(lambda: NRGeoLocationUISchema()))

    languages = ma_fields.List(
        ma_fields.Nested(lambda: NRLanguageVocabularyUISchema()), required=True
    )

    methods = MultilingualUIField(I18nStrUIField())

    notes = ma_fields.List(ma_fields.String())

    objectIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRObjectIdentifierUISchema())
    )

    originalRecord = ma_fields.String()

    publishers = ma_fields.List(ma_fields.String())

    relatedItems = ma_fields.List(ma_fields.Nested(lambda: NRRelatedItemUISchema()))

    resourceType = ma_fields.Nested(
        lambda: NRResourceTypeVocabularyUISchema(), required=True
    )

    rights = ma_fields.List(ma_fields.Nested(lambda: NRLicenseVocabularyUISchema()))

    series = ma_fields.List(ma_fields.Nested(lambda: NRSeriesUISchema()))

    subjectCategories = ma_fields.List(
        ma_fields.Nested(lambda: NRSubjectCategoryVocabularyUISchema())
    )

    subjects = NRSubjectListField(ma_fields.Nested(lambda: NRSubjectUISchema()))

    systemIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRSystemIdentifierUISchema())
    )

    technicalInfo = MultilingualUIField(I18nStrUIField())

    title = ma_fields.String(required=True)

    version = ma_fields.String()


class AdditionalTitlesUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    title = I18nStrUIField(required=True)

    titleType = ma_fields.String(
        required=True,
        validate=[OneOf(["translatedTitle", "alternativeTitle", "subtitle", "other"])],
    )


class NRContributorUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularyUISchema())
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierUISchema())
    )

    fullName = ma_fields.String(required=True)

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])

    role = ma_fields.Nested(lambda: NRAuthorityRoleVocabularyUISchema())


class NRCreatorUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularyUISchema())
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierUISchema())
    )

    fullName = ma_fields.String(required=True)

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])
