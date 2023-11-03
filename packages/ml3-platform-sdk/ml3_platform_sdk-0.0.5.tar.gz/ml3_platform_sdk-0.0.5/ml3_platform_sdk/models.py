from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from ml3_platform_sdk.enums import (
    DatasetType,
    DetectionEventActionType,
    DetectionEventSeverity,
    DetectionEventType,
    ExternalIntegration,
    KPIStatus,
    ModelMetricName,
    ModelStatus,
    MonitoringTarget,
    StoragePolicy,
    TaskStatus,
    TaskType,
    UserCompanyRole,
)

# Used for polymorphic classes (de)serialization
subclass_registry: Dict = {}


class Company(BaseModel):
    """
    Company model

    Attributes:
        company_id: str
        name: str
        address: str
        vat: str
    """

    company_id: str
    name: str
    address: str
    vat: str


class Project(BaseModel):
    """
    Project model

    Attributes:
        project_id: str
        name: str

    """

    project_id: str
    name: str


class Task(BaseModel):
    """
    Task model

    Attributes:
        task_id: str
        name: str
        type: TaskType
        status: TaskStatus
        status_start_date: str
    """

    task_id: str
    name: str
    type: TaskType
    status: TaskStatus
    status_start_date: str


class Model(BaseModel):
    """
    Base model to define model item

    Attributes:
        model_id: str
        task_id: str
        name: str
        version: str
        status: ModelStatus
        status_data_start_timestamp: Optional[datetime]
        status_insert_datetime: datetime
        metric_name: performance or error metric associated with
            the model
    """

    model_id: str
    task_id: str
    name: str
    version: str
    status: ModelStatus
    status_data_start_timestamp: Optional[datetime]
    status_insert_datetime: datetime
    metric_name: ModelMetricName


class Job(BaseModel):
    """
    Job information item model

    Attributes:
        job_id: str
        job_group: str
        project_id: str
        project_name: str
        task_id: str
        task_name: str
        model_id: Optional[str]
        model_name: Optional[str]
        status: str
        error: Optional[str]

    """

    job_id: str
    job_group: str
    project_id: str
    project_name: str
    task_id: str
    task_name: str
    model_id: Optional[str]
    model_name: Optional[str]
    status: str
    error: Optional[str]


class ColumnInfo(BaseModel):
    """
    Column base model

    Attributes:
        name: str
        data_type: str
        role: str
        is_nullable: bool
        predicted_target: Optional[str] = None
        possible_values: Optional[List] = None
        model_id: Optional[str] = None
    """

    name: str
    data_type: str
    role: str
    is_nullable: bool
    predicted_target: Optional[str] = None
    possible_values: Optional[List] = None
    model_id: Optional[str] = None


class DataSchema(BaseModel):
    """
    Data schema base model

    Attributes:
        columns: List[ColumnInfo]

    """

    columns: List[ColumnInfo]


class KPI(BaseModel):
    """
    KPI base model

    Attributes:
        kpi_id: str
        name: str
        status: ModelStatus
        status_kpi_start_timestamp: Optional[datetime]
        status_insert_datetime: datetime
    """

    kpi_id: str
    name: str
    status: KPIStatus
    status_kpi_start_timestamp: Optional[datetime]
    status_insert_datetime: datetime


class Suggestion(BaseModel):
    """
    Suggestion base model

    Attributes:
        id: str
        executed: bool
        timestamp: str
    """

    id: str
    executed: bool
    timestamp: str


class RetrainingReport(BaseModel):
    """
    base model for Retraining Report

    Attributes:
        report_id: str
        sample_ids: List[str]
        sample_weights: List[float]
        effective_sample_size: float
        model_metric_name: str
        upper_bound: float
        lower_bound: float
    """

    report_id: str
    suggestion_id: str
    sample_ids: List[str]
    sample_weights: List[float]
    effective_sample_size: float
    model_metric_name: str
    upper_bound: float
    lower_bound: float


class CompanyUser(BaseModel):
    """
    base model for company user

    Attributes:
        user_id: str
        company_role: UserCompanyRole
    """

    user_id: str
    company_role: UserCompanyRole


class ApiKey(BaseModel):
    """
    base model for api key

    Attributes:
        api_key: str
    """

    api_key: str
    name: str
    expiration_time: Optional[str]


class DetectionEventAction(BaseModel):
    """
    Generic action that can be performed

    Attributes:
        type: DetectionEventActionType
    """

    type: DetectionEventActionType

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        subclass_registry[cls.__name__] = cls


class DiscordNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Discord server through
    a webhook that you configure

    Attributes:
        type = DetectionEventActionType.DISCORD_NOTIFICATION
        webhook: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.DISCORD_NOTIFICATION
    )
    webhook: str


class SlackNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Slack channel through
    a webhook that you configure.

    Attributes:
        type = DetectionEventActionType.SLACK_NOTIFICATION
        webhook: str
        channel: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.SLACK_NOTIFICATION
    )
    webhook: str
    channel: str


def deserialize_actions(**kwargs):
    """
    Deserializes polymorphic actions from dict to their models.
    """

    for index in range(len(kwargs['actions'])):
        current_action = kwargs['actions'][index]
        if isinstance(current_action, dict):
            item_action_keys = sorted(current_action.keys())
            for subclass in subclass_registry.values():
                registered_keys = sorted(subclass.__fields__.keys())
                if (
                    item_action_keys == registered_keys
                    and current_action['type']
                    == subclass.__fields__['type'].default.value
                ):
                    current_action = subclass(**current_action)
                    break
            kwargs['actions'][index] = current_action


class DetectionEventRule(BaseModel):
    """
    A rule that can be triggered by a detection event, and executes
    a series of actions.

    Attributes:
        rule_id: str
        name: str
        task_id: str
        model_id: Optional[str]
        severity: DetectionEventSeverity
        detection_event_type: DetectionEventType
        monitoring_target: MonitoringTarget
        actions: List[DetectionEventAction]
    """

    rule_id: str
    name: str
    task_id: str
    model_id: Optional[str]
    severity: DetectionEventSeverity
    detection_event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    actions: List[DetectionEventAction]

    # Dynamically instantiate the correct subclass of every ActionModel
    # in the list of actions
    def __init__(self, **kwargs):
        if 'actions' in kwargs and kwargs['actions'] is not None:
            deserialize_actions(**kwargs)
        super().__init__(**kwargs)


class IntegrationCredentials(BaseModel):
    """
    Credentials to authenticate to a 3rd party service provider
    via an integration.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
    """

    credentials_id: str
    name: str
    default: bool
    type: ExternalIntegration


class AWSCredentials(IntegrationCredentials):
    """
    AWS integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the role that should be assumed via STS
    """

    role_arn: str


class SecretAWSCredentials(AWSCredentials):
    """
    AWS integration credentials, that also include the external_id
    you need to set up the trust policy on AWS.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the IAM role that should be assumed
        external_id: Secret key used to assume the IAM role via STS
    """

    external_id: str

    def generate_trust_policy(self):
        """
        Generates a JSON trust policy that you can copy into the IAM
        role on AWS.
        """

        return f"""
{{
    "Effect": "Allow",
    "Principal": {{
        "AWS": "arn:aws:iam::883313729965:root"
    }},
    "Action": "sts:AssumeRole",
    "Condition": {{
        "StringEquals": {{
            "sts:ExternalId": "{self.external_id}"
        }}
    }}
}}
        """


class GCPCredentials(IntegrationCredentials):
    """
    GCP integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        gcp_project_id: The id of the project on GCP
        client_email: The email that identifies the service account
        client_id: The client id
    """

    gcp_project_id: str
    client_email: str
    client_id: str


class AzureCredentials(IntegrationCredentials):
    """
    Azure integration credentials.

    Attributes:
        app_id: The id of the service principal
    """

    app_id: str
    display_name: str
    tenant: str


class DataSource(BaseModel):
    """
    Generic data source.

    Attributes:
        dataset_type: DatasetType
    """

    dataset_type: DatasetType


class LocalDataSource(DataSource):
    """
    Use this data source if you want to upload a file from your
    local disk to the ML cube platform cloud.

    Attributes:
        file_path: str
    """

    file_path: str


class RemoteDataSource(DataSource):
    """
    A source that identifies where data is stored.

    Attributes:
        credentials_id: The id of the credentials to use to authenticate
        to the remote data source. If None, the default will be used
    """

    credentials_id: Optional[str]
    storage_policy: Optional[StoragePolicy] = None


class S3DataSource(RemoteDataSource):
    """
    A source that identifies a file in an S3 bucket.

    Attributes:
        object_path: str
    """

    object_path: str


class GCSDataSource(RemoteDataSource):
    """
    A source that identifies a file in a GCS bucket.

    Attributes:
        object_path: str
    """

    object_path: str


class AzureBlobDataSource(RemoteDataSource):
    """
    A source that identifies a blob in Azure Storage.

    Attributes:
        object_path: str
    """

    object_path: str


class PredictionDataSourceInfo(BaseModel):
    """
    Base model to define the relationship
    between a model and its prediction file
    """

    model_id: str
    predictions_data_source: DataSource
