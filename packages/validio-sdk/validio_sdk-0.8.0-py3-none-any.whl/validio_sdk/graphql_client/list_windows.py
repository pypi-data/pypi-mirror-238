from datetime import datetime
from typing import Annotated, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import JsonPointer, SourceId, WindowId

from .base_model import BaseModel
from .enums import WindowTimeUnit


class ListWindows(BaseModel):
    windows_list: List[
        Annotated[
            Union[
                "ListWindowsWindowsListWindow",
                "ListWindowsWindowsListFileWindow",
                "ListWindowsWindowsListFixedBatchWindow",
                "ListWindowsWindowsListTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="windowsList")


class ListWindowsWindowsListWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListWindowsWindowsListWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListWindowsWindowsListFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListWindowsWindowsListFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListWindowsWindowsListFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListWindowsWindowsListFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class ListWindowsWindowsListTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "ListWindowsWindowsListTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    config: "ListWindowsWindowsListTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class ListWindowsWindowsListTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class ListWindowsWindowsListTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")


ListWindows.update_forward_refs()
ListWindowsWindowsListWindow.update_forward_refs()
ListWindowsWindowsListWindowSource.update_forward_refs()
ListWindowsWindowsListFileWindow.update_forward_refs()
ListWindowsWindowsListFileWindowSource.update_forward_refs()
ListWindowsWindowsListFixedBatchWindow.update_forward_refs()
ListWindowsWindowsListFixedBatchWindowSource.update_forward_refs()
ListWindowsWindowsListFixedBatchWindowConfig.update_forward_refs()
ListWindowsWindowsListTumblingWindow.update_forward_refs()
ListWindowsWindowsListTumblingWindowSource.update_forward_refs()
ListWindowsWindowsListTumblingWindowConfig.update_forward_refs()
