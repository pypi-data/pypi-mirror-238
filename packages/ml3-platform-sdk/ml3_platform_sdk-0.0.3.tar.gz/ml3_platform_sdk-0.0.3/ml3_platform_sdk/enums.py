from enum import Enum


class TaskType(Enum):
    """
    **Fields:**

        - REGRESSION
        - CLASSIFICATION
    """

    REGRESSION = 'regression'
    CLASSIFICATION = 'classification'

    def __str__(self):
        return self.value


class TaskStatus(Enum):
    """
    **Fields:**

        - OK
        - WARNING
        - DRIFT
    """

    OK = 'ok'
    WARNING = 'warning'
    DRIFT = 'drift'

    def __str__(self):
        return self.value


class ModelStatus(Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = 'not_initialized'
    OK = 'ok'
    WARNING = 'warning'
    DRIFT = 'drift'

    def __str__(self):
        return self.value


class KPIStatus(Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = 'not_initialized'
    OK = 'ok'
    WARNING = 'warning'
    DRIFT = 'drift'

    def __str__(self):
        return self.value


class DatasetType(Enum):
    """
    **Fields:**

        - TABULAR
    """

    TABULAR = 'tabular'


class StoringDataType(Enum):
    """
    **Fields:**

        - HISTORICAL
        - REFERENCE
        - PRODUCTION
    """

    HISTORICAL = 'historical'
    REFERENCE = 'reference'
    PRODUCTION = 'production'
    KPI = 'kpi'


class FileType(Enum):
    """
    **Fields:**

        - CSV
        - JSON
    """

    CSV = 'csv'
    JSON = 'json'


class JobStatus(Enum):
    """
    **Fields:**

        - IDLE
        - STARTING
        - RUNNING
        - COMPLETED
        - ERROR
    """

    IDLE = 'idle'
    STARTING = 'starting'
    RUNNING = 'running'
    COMPLETED = 'completed'
    ERROR = 'error'


class UserCompanyRole(Enum):
    """
    **Fields:**

        - COMPANY_OWNER
        - COMPANY_ADMIN
        - COMPANY_USER
        - COMPANY_NONE
    """

    COMPANY_OWNER = "COMPANY_OWNER"
    COMPANY_ADMIN = "COMPANY_ADMIN"
    COMPANY_USER = "COMPANY_USER"
    COMPANY_NONE = "COMPANY_NONE"


class UserProjectRole(Enum):
    """
    **Fields:**

        - PROJECT_ADMIN
        - PROJECT_USER
        - PROJECT_VIEW
    """

    PROJECT_ADMIN = "PROJECT_ADMIN"
    PROJECT_USER = "PROJECT_USER"
    PROJECT_VIEW = "PROJECT_VIEW"


class DetectionEventSeverity(Enum):
    """
    **Fields:**

        - LOW
        - MEDIUM
        - HIGH
    """

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class DetectionEventType(Enum):
    """
    **Fields:**

        - DRIFT
    """

    DRIFT = 'drift'


class MonitoringTarget(Enum):
    """
    **Fields:**

        - MODEL
        - INPUT
        - CONCEPT
    """

    MODEL = 'model'
    INPUT = 'input'
    CONCEPT = 'concept'


class DetectionEventActionType(Enum):
    """
    **Fields:**

        - DISCORD_NOTIFICATION
        - SLACK_NOTIFICATION

    """

    DISCORD_NOTIFICATION = 'discord_notification'
    SLACK_NOTIFICATION = 'slack_notification'


class ModelMetricName(Enum):
    """
    Name of the model metrics that is associated with the model

    **Fields:**
        - RMSE
        - RSQUARE
    """

    RMSE = 'rmse'
    RSQUARE = 'rsquare'


class ApiKeyExpirationTime(Enum):
    """
    **Fields:**

        - ONE_MONTH
        - THREE_MONTHS
        - SIX_MONTHS
        - ONE_YEAR
        - NEVER

    """

    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'
    SIX_MONTHS = 'six_months'
    ONE_YEAR = 'one_year'
    NEVER = 'never'


class ExternalIntegration(Enum):
    """
    An integration with a 3rd party service provider

    **Fields:**
        - AWS
        - GCP
    """

    AWS = 'aws'
    GCP = 'gcp'


class StoragePolicy(Enum):
    """
    Enumeration that specify the storage policy for the data sent to
    ML cube Platform

    **Fields:**
        - MLCUBE: data are copied and stored into the ML cube Platform
            cloud
        - CUSTOMER: data are kept only in your cloud and ML cube
            Platform will access to this storage source every time
            it needs to read data
    """

    MLCUBE = 'mlcube'
    CUSTOMER = 'customer'
