"""
Type annotations for translate service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_translate/type_defs/)

Usage::

    ```python
    from mypy_boto3_translate.type_defs import TermTypeDef

    data: TermTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    DirectionalityType,
    DisplayLanguageCodeType,
    FormalityType,
    JobStatusType,
    ParallelDataFormatType,
    ParallelDataStatusType,
    TerminologyDataFormatType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "TermTypeDef",
    "BlobTypeDef",
    "EncryptionKeyTypeDef",
    "ParallelDataConfigTypeDef",
    "TagTypeDef",
    "ResponseMetadataTypeDef",
    "DeleteParallelDataRequestRequestTypeDef",
    "DeleteTerminologyRequestRequestTypeDef",
    "DescribeTextTranslationJobRequestRequestTypeDef",
    "GetParallelDataRequestRequestTypeDef",
    "ParallelDataDataLocationTypeDef",
    "GetTerminologyRequestRequestTypeDef",
    "TerminologyDataLocationTypeDef",
    "InputDataConfigTypeDef",
    "JobDetailsTypeDef",
    "LanguageTypeDef",
    "ListLanguagesRequestRequestTypeDef",
    "ListParallelDataRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListTerminologiesRequestRequestTypeDef",
    "TranslationSettingsTypeDef",
    "StopTextTranslationJobRequestRequestTypeDef",
    "TimestampTypeDef",
    "TranslatedDocumentTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AppliedTerminologyTypeDef",
    "DocumentTypeDef",
    "TerminologyDataTypeDef",
    "OutputDataConfigTypeDef",
    "TerminologyPropertiesTypeDef",
    "ParallelDataPropertiesTypeDef",
    "UpdateParallelDataRequestRequestTypeDef",
    "CreateParallelDataRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateParallelDataResponseTypeDef",
    "DeleteParallelDataResponseTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "StartTextTranslationJobResponseTypeDef",
    "StopTextTranslationJobResponseTypeDef",
    "UpdateParallelDataResponseTypeDef",
    "ListLanguagesResponseTypeDef",
    "ListTerminologiesRequestListTerminologiesPaginateTypeDef",
    "TranslateTextRequestRequestTypeDef",
    "TextTranslationJobFilterTypeDef",
    "TranslateDocumentResponseTypeDef",
    "TranslateTextResponseTypeDef",
    "TranslateDocumentRequestRequestTypeDef",
    "ImportTerminologyRequestRequestTypeDef",
    "StartTextTranslationJobRequestRequestTypeDef",
    "TextTranslationJobPropertiesTypeDef",
    "GetTerminologyResponseTypeDef",
    "ImportTerminologyResponseTypeDef",
    "ListTerminologiesResponseTypeDef",
    "GetParallelDataResponseTypeDef",
    "ListParallelDataResponseTypeDef",
    "ListTextTranslationJobsRequestRequestTypeDef",
    "DescribeTextTranslationJobResponseTypeDef",
    "ListTextTranslationJobsResponseTypeDef",
)

TermTypeDef = TypedDict(
    "TermTypeDef",
    {
        "SourceText": NotRequired[str],
        "TargetText": NotRequired[str],
    },
)

BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]
EncryptionKeyTypeDef = TypedDict(
    "EncryptionKeyTypeDef",
    {
        "Type": Literal["KMS"],
        "Id": str,
    },
)

ParallelDataConfigTypeDef = TypedDict(
    "ParallelDataConfigTypeDef",
    {
        "S3Uri": NotRequired[str],
        "Format": NotRequired[ParallelDataFormatType],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

DeleteParallelDataRequestRequestTypeDef = TypedDict(
    "DeleteParallelDataRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DeleteTerminologyRequestRequestTypeDef = TypedDict(
    "DeleteTerminologyRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DescribeTextTranslationJobRequestRequestTypeDef = TypedDict(
    "DescribeTextTranslationJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

GetParallelDataRequestRequestTypeDef = TypedDict(
    "GetParallelDataRequestRequestTypeDef",
    {
        "Name": str,
    },
)

ParallelDataDataLocationTypeDef = TypedDict(
    "ParallelDataDataLocationTypeDef",
    {
        "RepositoryType": str,
        "Location": str,
    },
)

GetTerminologyRequestRequestTypeDef = TypedDict(
    "GetTerminologyRequestRequestTypeDef",
    {
        "Name": str,
        "TerminologyDataFormat": NotRequired[TerminologyDataFormatType],
    },
)

TerminologyDataLocationTypeDef = TypedDict(
    "TerminologyDataLocationTypeDef",
    {
        "RepositoryType": str,
        "Location": str,
    },
)

InputDataConfigTypeDef = TypedDict(
    "InputDataConfigTypeDef",
    {
        "S3Uri": str,
        "ContentType": str,
    },
)

JobDetailsTypeDef = TypedDict(
    "JobDetailsTypeDef",
    {
        "TranslatedDocumentsCount": NotRequired[int],
        "DocumentsWithErrorsCount": NotRequired[int],
        "InputDocumentsCount": NotRequired[int],
    },
)

LanguageTypeDef = TypedDict(
    "LanguageTypeDef",
    {
        "LanguageName": str,
        "LanguageCode": str,
    },
)

ListLanguagesRequestRequestTypeDef = TypedDict(
    "ListLanguagesRequestRequestTypeDef",
    {
        "DisplayLanguageCode": NotRequired[DisplayLanguageCodeType],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListParallelDataRequestRequestTypeDef = TypedDict(
    "ListParallelDataRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

ListTerminologiesRequestRequestTypeDef = TypedDict(
    "ListTerminologiesRequestRequestTypeDef",
    {
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

TranslationSettingsTypeDef = TypedDict(
    "TranslationSettingsTypeDef",
    {
        "Formality": NotRequired[FormalityType],
        "Profanity": NotRequired[Literal["MASK"]],
        "Brevity": NotRequired[Literal["ON"]],
    },
)

StopTextTranslationJobRequestRequestTypeDef = TypedDict(
    "StopTextTranslationJobRequestRequestTypeDef",
    {
        "JobId": str,
    },
)

TimestampTypeDef = Union[datetime, str]
TranslatedDocumentTypeDef = TypedDict(
    "TranslatedDocumentTypeDef",
    {
        "Content": bytes,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

AppliedTerminologyTypeDef = TypedDict(
    "AppliedTerminologyTypeDef",
    {
        "Name": NotRequired[str],
        "Terms": NotRequired[List[TermTypeDef]],
    },
)

DocumentTypeDef = TypedDict(
    "DocumentTypeDef",
    {
        "Content": BlobTypeDef,
        "ContentType": str,
    },
)

TerminologyDataTypeDef = TypedDict(
    "TerminologyDataTypeDef",
    {
        "File": BlobTypeDef,
        "Format": TerminologyDataFormatType,
        "Directionality": NotRequired[DirectionalityType],
    },
)

OutputDataConfigTypeDef = TypedDict(
    "OutputDataConfigTypeDef",
    {
        "S3Uri": str,
        "EncryptionKey": NotRequired[EncryptionKeyTypeDef],
    },
)

TerminologyPropertiesTypeDef = TypedDict(
    "TerminologyPropertiesTypeDef",
    {
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Arn": NotRequired[str],
        "SourceLanguageCode": NotRequired[str],
        "TargetLanguageCodes": NotRequired[List[str]],
        "EncryptionKey": NotRequired[EncryptionKeyTypeDef],
        "SizeBytes": NotRequired[int],
        "TermCount": NotRequired[int],
        "CreatedAt": NotRequired[datetime],
        "LastUpdatedAt": NotRequired[datetime],
        "Directionality": NotRequired[DirectionalityType],
        "Message": NotRequired[str],
        "SkippedTermCount": NotRequired[int],
        "Format": NotRequired[TerminologyDataFormatType],
    },
)

ParallelDataPropertiesTypeDef = TypedDict(
    "ParallelDataPropertiesTypeDef",
    {
        "Name": NotRequired[str],
        "Arn": NotRequired[str],
        "Description": NotRequired[str],
        "Status": NotRequired[ParallelDataStatusType],
        "SourceLanguageCode": NotRequired[str],
        "TargetLanguageCodes": NotRequired[List[str]],
        "ParallelDataConfig": NotRequired[ParallelDataConfigTypeDef],
        "Message": NotRequired[str],
        "ImportedDataSize": NotRequired[int],
        "ImportedRecordCount": NotRequired[int],
        "FailedRecordCount": NotRequired[int],
        "SkippedRecordCount": NotRequired[int],
        "EncryptionKey": NotRequired[EncryptionKeyTypeDef],
        "CreatedAt": NotRequired[datetime],
        "LastUpdatedAt": NotRequired[datetime],
        "LatestUpdateAttemptStatus": NotRequired[ParallelDataStatusType],
        "LatestUpdateAttemptAt": NotRequired[datetime],
    },
)

UpdateParallelDataRequestRequestTypeDef = TypedDict(
    "UpdateParallelDataRequestRequestTypeDef",
    {
        "Name": str,
        "ParallelDataConfig": ParallelDataConfigTypeDef,
        "ClientToken": str,
        "Description": NotRequired[str],
    },
)

CreateParallelDataRequestRequestTypeDef = TypedDict(
    "CreateParallelDataRequestRequestTypeDef",
    {
        "Name": str,
        "ParallelDataConfig": ParallelDataConfigTypeDef,
        "ClientToken": str,
        "Description": NotRequired[str],
        "EncryptionKey": NotRequired[EncryptionKeyTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateParallelDataResponseTypeDef = TypedDict(
    "CreateParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteParallelDataResponseTypeDef = TypedDict(
    "DeleteParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartTextTranslationJobResponseTypeDef = TypedDict(
    "StartTextTranslationJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StopTextTranslationJobResponseTypeDef = TypedDict(
    "StopTextTranslationJobResponseTypeDef",
    {
        "JobId": str,
        "JobStatus": JobStatusType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateParallelDataResponseTypeDef = TypedDict(
    "UpdateParallelDataResponseTypeDef",
    {
        "Name": str,
        "Status": ParallelDataStatusType,
        "LatestUpdateAttemptStatus": ParallelDataStatusType,
        "LatestUpdateAttemptAt": datetime,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListLanguagesResponseTypeDef = TypedDict(
    "ListLanguagesResponseTypeDef",
    {
        "Languages": List[LanguageTypeDef],
        "DisplayLanguageCode": DisplayLanguageCodeType,
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTerminologiesRequestListTerminologiesPaginateTypeDef = TypedDict(
    "ListTerminologiesRequestListTerminologiesPaginateTypeDef",
    {
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

TranslateTextRequestRequestTypeDef = TypedDict(
    "TranslateTextRequestRequestTypeDef",
    {
        "Text": str,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
        "TerminologyNames": NotRequired[Sequence[str]],
        "Settings": NotRequired[TranslationSettingsTypeDef],
    },
)

TextTranslationJobFilterTypeDef = TypedDict(
    "TextTranslationJobFilterTypeDef",
    {
        "JobName": NotRequired[str],
        "JobStatus": NotRequired[JobStatusType],
        "SubmittedBeforeTime": NotRequired[TimestampTypeDef],
        "SubmittedAfterTime": NotRequired[TimestampTypeDef],
    },
)

TranslateDocumentResponseTypeDef = TypedDict(
    "TranslateDocumentResponseTypeDef",
    {
        "TranslatedDocument": TranslatedDocumentTypeDef,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
        "AppliedTerminologies": List[AppliedTerminologyTypeDef],
        "AppliedSettings": TranslationSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TranslateTextResponseTypeDef = TypedDict(
    "TranslateTextResponseTypeDef",
    {
        "TranslatedText": str,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
        "AppliedTerminologies": List[AppliedTerminologyTypeDef],
        "AppliedSettings": TranslationSettingsTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TranslateDocumentRequestRequestTypeDef = TypedDict(
    "TranslateDocumentRequestRequestTypeDef",
    {
        "Document": DocumentTypeDef,
        "SourceLanguageCode": str,
        "TargetLanguageCode": str,
        "TerminologyNames": NotRequired[Sequence[str]],
        "Settings": NotRequired[TranslationSettingsTypeDef],
    },
)

ImportTerminologyRequestRequestTypeDef = TypedDict(
    "ImportTerminologyRequestRequestTypeDef",
    {
        "Name": str,
        "MergeStrategy": Literal["OVERWRITE"],
        "TerminologyData": TerminologyDataTypeDef,
        "Description": NotRequired[str],
        "EncryptionKey": NotRequired[EncryptionKeyTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

StartTextTranslationJobRequestRequestTypeDef = TypedDict(
    "StartTextTranslationJobRequestRequestTypeDef",
    {
        "InputDataConfig": InputDataConfigTypeDef,
        "OutputDataConfig": OutputDataConfigTypeDef,
        "DataAccessRoleArn": str,
        "SourceLanguageCode": str,
        "TargetLanguageCodes": Sequence[str],
        "ClientToken": str,
        "JobName": NotRequired[str],
        "TerminologyNames": NotRequired[Sequence[str]],
        "ParallelDataNames": NotRequired[Sequence[str]],
        "Settings": NotRequired[TranslationSettingsTypeDef],
    },
)

TextTranslationJobPropertiesTypeDef = TypedDict(
    "TextTranslationJobPropertiesTypeDef",
    {
        "JobId": NotRequired[str],
        "JobName": NotRequired[str],
        "JobStatus": NotRequired[JobStatusType],
        "JobDetails": NotRequired[JobDetailsTypeDef],
        "SourceLanguageCode": NotRequired[str],
        "TargetLanguageCodes": NotRequired[List[str]],
        "TerminologyNames": NotRequired[List[str]],
        "ParallelDataNames": NotRequired[List[str]],
        "Message": NotRequired[str],
        "SubmittedTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "InputDataConfig": NotRequired[InputDataConfigTypeDef],
        "OutputDataConfig": NotRequired[OutputDataConfigTypeDef],
        "DataAccessRoleArn": NotRequired[str],
        "Settings": NotRequired[TranslationSettingsTypeDef],
    },
)

GetTerminologyResponseTypeDef = TypedDict(
    "GetTerminologyResponseTypeDef",
    {
        "TerminologyProperties": TerminologyPropertiesTypeDef,
        "TerminologyDataLocation": TerminologyDataLocationTypeDef,
        "AuxiliaryDataLocation": TerminologyDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ImportTerminologyResponseTypeDef = TypedDict(
    "ImportTerminologyResponseTypeDef",
    {
        "TerminologyProperties": TerminologyPropertiesTypeDef,
        "AuxiliaryDataLocation": TerminologyDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTerminologiesResponseTypeDef = TypedDict(
    "ListTerminologiesResponseTypeDef",
    {
        "TerminologyPropertiesList": List[TerminologyPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetParallelDataResponseTypeDef = TypedDict(
    "GetParallelDataResponseTypeDef",
    {
        "ParallelDataProperties": ParallelDataPropertiesTypeDef,
        "DataLocation": ParallelDataDataLocationTypeDef,
        "AuxiliaryDataLocation": ParallelDataDataLocationTypeDef,
        "LatestUpdateAttemptAuxiliaryDataLocation": ParallelDataDataLocationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListParallelDataResponseTypeDef = TypedDict(
    "ListParallelDataResponseTypeDef",
    {
        "ParallelDataPropertiesList": List[ParallelDataPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTextTranslationJobsRequestRequestTypeDef = TypedDict(
    "ListTextTranslationJobsRequestRequestTypeDef",
    {
        "Filter": NotRequired[TextTranslationJobFilterTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
    },
)

DescribeTextTranslationJobResponseTypeDef = TypedDict(
    "DescribeTextTranslationJobResponseTypeDef",
    {
        "TextTranslationJobProperties": TextTranslationJobPropertiesTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTextTranslationJobsResponseTypeDef = TypedDict(
    "ListTextTranslationJobsResponseTypeDef",
    {
        "TextTranslationJobPropertiesList": List[TextTranslationJobPropertiesTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
