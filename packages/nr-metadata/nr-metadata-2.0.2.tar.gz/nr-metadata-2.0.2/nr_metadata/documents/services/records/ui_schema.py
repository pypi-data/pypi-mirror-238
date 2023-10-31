import marshmallow as ma
from marshmallow import Schema
from marshmallow import fields as ma_fields
from marshmallow.fields import String
from oarepo_runtime.services.schema.ui import InvenioUISchema, LocalizedDate
from oarepo_vocabularies.services.ui_schema import (
    HierarchyUISchema,
    VocabularyI18nStrUIField,
)

from nr_metadata.common.services.records.ui_schema_common import (
    AdditionalTitlesUISchema,
    NRCommonMetadataUISchema,
    NRContributorUISchema,
    NRCreatorUISchema,
)
from nr_metadata.common.services.records.ui_schema_datatypes import (
    NRAccessRightsVocabularyUISchema,
    NRAffiliationVocabularyUISchema,
    NRAuthorityRoleVocabularyUISchema,
    NRCountryVocabularyUISchema,
    NREventUISchema,
    NRExternalLocationUISchema,
    NRFunderVocabularyUISchema,
    NRFundingReferenceUISchema,
    NRGeoLocationPointUISchema,
    NRGeoLocationUISchema,
    NRItemRelationTypeVocabularyUISchema,
    NRLanguageVocabularyUISchema,
    NRLicenseVocabularyUISchema,
    NRLocationUISchema,
    NRRelatedItemContributorUISchema,
    NRRelatedItemCreatorUISchema,
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


class NRDocumentRecordUISchema(InvenioUISchema):
    class Meta:
        unknown = ma.RAISE

    metadata = ma_fields.Nested(lambda: NRDocumentMetadataUISchema())

    syntheticFields = ma_fields.Nested(lambda: SyntheticFieldsUISchema())


class NRDocumentMetadataUISchema(NRCommonMetadataUISchema):
    class Meta:
        unknown = ma.RAISE

    additionalTitles = ma_fields.List(
        ma_fields.Nested(lambda: AdditionalTitlesItemUISchema())
    )

    collection = ma_fields.String()

    contributors = ma_fields.List(ma_fields.Nested(lambda: ContributorsItemUISchema()))

    creators = ma_fields.List(
        ma_fields.Nested(lambda: CreatorsItemUISchema()), required=True
    )

    thesis = ma_fields.Nested(lambda: NRThesisUISchema())


class GeoLocationsItemUISchema(NRGeoLocationUISchema):
    class Meta:
        unknown = ma.RAISE

    geoLocationPoint = ma_fields.Nested(lambda: GeoLocationPointUISchema())


class NRThesisUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    dateDefended = LocalizedDate()

    defended = ma_fields.Boolean()

    degreeGrantors = ma_fields.List(ma_fields.Nested(lambda: NRDegreeGrantorUISchema()))

    studyFields = ma_fields.List(ma_fields.String())


class RelatedItemsItemUISchema(NRRelatedItemUISchema):
    class Meta:
        unknown = ma.RAISE

    itemContributors = ma_fields.List(
        ma_fields.Nested(lambda: ItemContributorsItemUISchema())
    )

    itemCreators = ma_fields.List(ma_fields.Nested(lambda: ItemCreatorsItemUISchema()))


class AccessRightsUISchema(NRAccessRightsVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class AdditionalTitlesItemUISchema(AdditionalTitlesUISchema):
    class Meta:
        unknown = ma.RAISE


class AffiliationsItemUISchema(NRAffiliationVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class AuthorityIdentifiersItemUISchema(NRAuthorityIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class ContributorsItemUISchema(NRContributorUISchema):
    class Meta:
        unknown = ma.RAISE


class CountryUISchema(NRCountryVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class CreatorsItemUISchema(NRCreatorUISchema):
    class Meta:
        unknown = ma.RAISE


class EventLocationUISchema(NRLocationUISchema):
    class Meta:
        unknown = ma.RAISE


class EventsItemUISchema(NREventUISchema):
    class Meta:
        unknown = ma.RAISE


class ExternalLocationUISchema(NRExternalLocationUISchema):
    class Meta:
        unknown = ma.RAISE


class FunderUISchema(NRFunderVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class FundingReferencesItemUISchema(NRFundingReferenceUISchema):
    class Meta:
        unknown = ma.RAISE


class GeoLocationPointUISchema(NRGeoLocationPointUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemContributorsItemUISchema(NRRelatedItemContributorUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemCreatorsItemUISchema(NRRelatedItemCreatorUISchema):
    class Meta:
        unknown = ma.RAISE


class ItemRelationTypeUISchema(NRItemRelationTypeVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class ItemResourceTypeUISchema(NRResourceTypeVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class LanguagesItemUISchema(NRLanguageVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class NRDegreeGrantorUISchema(Schema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    hierarchy = ma_fields.Nested(lambda: HierarchyUISchema())

    title = VocabularyI18nStrUIField()


class ObjectIdentifiersItemUISchema(NRObjectIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE


class RightsItemUISchema(NRLicenseVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class RoleUISchema(NRAuthorityRoleVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SeriesItemUISchema(NRSeriesUISchema):
    class Meta:
        unknown = ma.RAISE


class SubjectCategoriesItemUISchema(NRSubjectCategoryVocabularyUISchema):
    class Meta:
        unknown = ma.INCLUDE

    _id = String(data_key="id", attribute="id")

    _version = String(data_key="@v", attribute="@v")

    title = VocabularyI18nStrUIField()


class SubjectsItemUISchema(NRSubjectUISchema):
    class Meta:
        unknown = ma.RAISE


class SyntheticFieldsUISchema(Schema):
    class Meta:
        unknown = ma.RAISE

    institutions = ma_fields.String()

    keywords_cs = ma_fields.String()

    keywords_en = ma_fields.String()

    person = ma_fields.String()


class SystemIdentifiersItemUISchema(NRSystemIdentifierUISchema):
    class Meta:
        unknown = ma.RAISE
