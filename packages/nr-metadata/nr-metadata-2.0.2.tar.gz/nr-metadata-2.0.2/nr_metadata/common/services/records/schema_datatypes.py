import marshmallow as ma
from edtf import Interval as EDTFInterval
from invenio_vocabularies.services.schema import i18n_strings
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from marshmallow.validate import OneOf
from marshmallow_utils.fields import TrimmedString
from oarepo_runtime.i18n.schema import I18nStrField, MultilingualField
from oarepo_runtime.services.schema.validation import CachedMultilayerEDTFValidator
from oarepo_vocabularies.services.schema import HierarchySchema

from nr_metadata.schema.identifiers import (
    NRAuthorityIdentifierSchema,
    NRObjectIdentifierSchema,
)


class NREventSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    eventDate = TrimmedString(
        required=True, validate=[CachedMultilayerEDTFValidator(types=(EDTFInterval,))]
    )

    eventLocation = ma_fields.Nested(lambda: NRLocationSchema(), required=True)

    eventNameAlternate = ma_fields.List(ma_fields.String())

    eventNameOriginal = ma_fields.String(required=True)


class NRRelatedItemSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma_fields.List(
        ma_fields.Nested(lambda: NRRelatedItemContributorSchema())
    )

    itemCreators = ma_fields.List(
        ma_fields.Nested(lambda: NRRelatedItemCreatorSchema())
    )

    itemEndPage = ma_fields.String()

    itemIssue = ma_fields.String()

    itemPIDs = ma_fields.List(ma_fields.Nested(lambda: NRObjectIdentifierSchema()))

    itemPublisher = ma_fields.String()

    itemRelationType = ma_fields.Nested(lambda: NRItemRelationTypeVocabularySchema())

    itemResourceType = ma_fields.Nested(lambda: NRResourceTypeVocabularySchema())

    itemStartPage = ma_fields.String()

    itemTitle = ma_fields.String(required=True)

    itemURL = ma_fields.String()

    itemVolume = ma_fields.String()

    itemYear = ma_fields.Integer()


class NRFundingReferenceSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    funder = ma_fields.Nested(lambda: NRFunderVocabularySchema())

    fundingProgram = ma_fields.String()

    projectID = ma_fields.String(required=True)

    projectName = ma_fields.String()


class NRGeoLocationSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    geoLocationPlace = ma_fields.String(required=True)

    geoLocationPoint = ma_fields.Nested(lambda: NRGeoLocationPointSchema())


class NRLocationSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    country = ma_fields.Nested(lambda: NRCountryVocabularySchema())

    place = ma_fields.String(required=True)


class NRRelatedItemContributorSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularySchema())
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierSchema())
    )

    fullName = ma_fields.String(required=True)

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])

    role = ma_fields.Nested(lambda: NRAuthorityRoleVocabularySchema())


class NRRelatedItemCreatorSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    affiliations = ma_fields.List(
        ma_fields.Nested(lambda: NRAffiliationVocabularySchema())
    )

    authorityIdentifiers = ma_fields.List(
        ma_fields.Nested(lambda: NRAuthorityIdentifierSchema())
    )

    fullName = ma_fields.String(required=True)

    nameType = ma_fields.String(validate=[OneOf(["Organizational", "Personal"])])


class NRAccessRightsVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRAffiliationVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchySchema())

    title = i18n_strings


class NRAuthorityRoleVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRCountryVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRExternalLocationSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    externalLocationNote = ma_fields.String()

    externalLocationURL = ma_fields.String(required=True)


class NRFunderVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRGeoLocationPointSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    pointLatitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-90.0, max=90.0)]
    )

    pointLongitude = ma_fields.Float(
        required=True, validate=[ma.validate.Range(min=-180.0, max=180.0)]
    )


class NRItemRelationTypeVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRLanguageVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRLicenseVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRResourceTypeVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRSeriesSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    seriesTitle = ma_fields.String(required=True)

    seriesVolume = ma_fields.String()


class NRSubjectCategoryVocabularySchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = i18n_strings


class NRSubjectSchema(Schema):
    class Meta:
        unknown = ma.RAISE

    classificationCode = ma_fields.String()

    subject = MultilingualField(I18nStrField(), required=True)

    subjectScheme = ma_fields.String()

    valueURI = ma_fields.String()
