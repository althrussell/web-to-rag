import asyncio
import enum
import json
import logging
import re
from contextlib import contextmanager
from datetime import timedelta
from typing import List, Union

import IPython
from pyspark.sql import SparkSession

# from lib.dates import utcnow
# from lib.dicts import getitem_by_path
# from lib.table_repo import TableRepo

# from .paths import get_user_temp_path

logger = logging.getLogger("lib.notebook")


# def get_current_widgets():
#     current_widgets = get_db_utils().notebook.entry_point.getCurrentBindings()
#     return {key: current_widgets[key] for key in current_widgets}


# class DeploymentMode(str, enum.Enum):
#     PROD = "prod"
#     STAGING = "staging"
#     DEV = "dev"

#     @classmethod
#     def has_value(cls, value: str) -> bool:
#         return value in cls._value2member_map_

#     @classmethod
#     def values(cls) -> List[str]:
#         return sorted(list(cls._value2member_map_.keys()))

#     @classmethod
#     def check_value(cls, value: str):
#         if not DeploymentMode.has_value(value):
#             raise ValueError(f"{value} is not a valid option in {DeploymentMode.values()}")

#     @staticmethod
#     def is_dev(value: str) -> bool:
#         return value == DeploymentMode.DEV

#     @staticmethod
#     def setup_widget(descriptor="deploymentMode", default_deployment_mode="dev"):
#         """Create a Notebook widget for specifying deployment mode. Will skip creating widget if one already exists."""
#         if "deploymentMode" not in get_current_widgets():
#             get_db_utils().widgets.dropdown(
#                 "deploymentMode",  # widget ID
#                 default_deployment_mode,  # default value
#                 ["dev", "staging", "prod"],  # selectable values
#                 descriptor,  # widget label
#             )

#     @staticmethod
#     def get_deployment_mode() -> str:
#         """Get and validate the Notebook's specified deployment mode"""
#         deployment_mode = get_widget_value("deploymentMode")
#         DeploymentMode.check_value(deployment_mode)
#         return deployment_mode


# def is_notebook() -> bool:
#     """Checks if this is running inside a Databricks notebook.

#     Returns:
#         bool: True if running inside a Databricks notebook, and False otherwise.
#     """
#     return IPython.get_ipython() is not None


# def get_global(name):
#     if is_notebook():
#         return IPython.get_ipython().user_ns[name]
#     else:
#         raise RuntimeError(f"Could not retrieve {name} because not running in a notebook")


def get_notebook_context() -> dict:  # pragma: no cover
    return json.loads(get_db_utils().notebook.entry_point.getDbutils().notebook().getContext().toJson())


# def is_job_retry() -> bool:
#     """Check if the notebook-job run is a retry or the original run. This
#     is useful for scenarios where operations do not need to be repeated for
#     retries eg. alert - sends

#     Returns:
#         bool: If the job-run is a retry, True else False
#     """
#     context = get_notebook_context()
#     trigger_type = getitem_by_path(context, "tags?.jobTriggerType?").lower()
#     logging.info(f"Trigger type for the job: {trigger_type}")
#     if trigger_type == "retry":
#         return True
#     return False


def get_db_utils():
    """
    Get dbutils in a way that works even within a function.
    """
    return get_global("dbutils")


# # This exists to make unit testing easier.
# def _get_spark() -> SparkSession:
#     return get_global("spark")


# def get_spark() -> SparkSession:
#     """
#     Get spark in a way that works even within a function.
#     """
#     return _get_spark()


# def displayLinesHTML(lines: Union[str, List[str]]):
#     lines = lines if isinstance(lines, list) else [lines]
#     displayHTML = get_global("displayHTML")
#     displayHTML("\n".join(lines))


# def displayURL(url: str, *, title=None) -> None:
#     """
#     Displays a URL as a clickable link in the notebook.
#     """

#     if not title:
#         title = url
#     displayHTML = get_global("displayHTML")
#     displayHTML(f"""<a href="{url}">{title}</a>""")


# DEPLOYMENT_MODE_ATTR = "deployment_mode_override"


# @contextmanager
# def temp_deployment_mode(mode: str) -> None:
#     """Temporarily sets the deployment mode to some other value.  This overrides any widget choice.
#     This is useful when you want to run a notebook in a dev execution mode and perhaps write to dev tables,
#     but you'd like certain components to read from prod tables, which have more realistic data.

#     Args:
#         mode (str): the deployment mode to override with
#     """
#     prev_deployment_mode = getattr(_get_table_repo, DEPLOYMENT_MODE_ATTR, None)
#     try:
#         setattr(_get_table_repo, DEPLOYMENT_MODE_ATTR, mode)
#         yield
#     finally:
#         setattr(_get_table_repo, DEPLOYMENT_MODE_ATTR, prev_deployment_mode)


# # This exists to make unit testing easier.
# def _get_table_repo() -> TableRepo:
#     deployment_mode = getattr(_get_table_repo, DEPLOYMENT_MODE_ATTR, None)
#     if not deployment_mode:
#         deployment_mode = get_widget_value("deploymentMode")
#     return TableRepo(deployment_mode)


# def get_table_repo() -> TableRepo:
#     """
#     Gets a table repo that can return full qualified names for tables based on the currently selected
#     deployment mode.
#     """
#     return _get_table_repo()


# WIDGET_SYS_PATH_BASE_DIR = "updateSysPathBaseDir"
# WIDGET_SYS_PATH_REL_DIR = "updateSysPathRelDir"
# WIDGET_SYS_PATH_EXPECTED_PREFIX = "/dbfs"


# def setup_sys_path_widgets():
#     """
#     Adds a couple widgets to make it easy for a user to update their Python sys.path to include
#     the temp user path written to by dbfs-sync.
#     """

#     user_temp_path = get_user_temp_path()
#     prefix = WIDGET_SYS_PATH_EXPECTED_PREFIX
#     if not user_temp_path.startswith(f"{prefix}/"):
#         raise RuntimeError(f"Expected {prefix}")

#     base_dir_opt = get_user_temp_path()[len(prefix) :]
#     rel_path_opt = "ds-projects"

#     get_db_utils().widgets.combobox(WIDGET_SYS_PATH_BASE_DIR, "", [base_dir_opt], "Update sys.path base dir")
#     get_db_utils().widgets.combobox(WIDGET_SYS_PATH_REL_DIR, "", [rel_path_opt], "Update sys.path relative dir")


# def check_sys_path_widget_choices():
#     # Enable overriding code with that synced over to a tmp folder using dbfs-sync.
#     sys_path_base_dir = get_db_utils().widgets.get(WIDGET_SYS_PATH_BASE_DIR)
#     sys_path_rel_dir = get_db_utils().widgets.get(WIDGET_SYS_PATH_REL_DIR)
#     if sys_path_base_dir and sys_path_rel_dir:
#         import os

#         from lib.paths import ensure_sys_path

#         prefix = WIDGET_SYS_PATH_EXPECTED_PREFIX
#         ensure_sys_path(os.path.join(prefix, sys_path_base_dir.lstrip("/"), sys_path_rel_dir))
#     elif sys_path_base_dir:
#         logging.error("No relative directory specified")


# def _format_date(date):
#     return date.strftime("%Y-%m-%d")


# def setup_default_widgets(
#     *,
#     include_dates: bool = False,
#     default_deployment_mode="dev",
#     date_defaults=False,
#     lookback_days=1,
#     uc_mode_widget=True,
# ) -> None:
#     """Creates notebook widgets for deployment mode (always) and start/end dates (optionally)

#     Args:
#         include_dates (bool, optional): Include start / end date widgets
#         default_deployment_mode (str, optional): Deployment mode.
#         date_defaults (bool, optional): Set endDate widget to today, startDate widget to yesterday - lookback_days
#         lookback_days (int, optional): Offset for startDate, relative to yesterday (to allow for ETL latency)
#     """

#     db_utils = get_db_utils()
#     if uc_mode_widget:
#         setup_yes_no_widget(name="isUCMode", title="isUCMode")
#     deployment_mode_descriptor = "deploymentMode"
#     if include_dates:
#         start_default, end_default = "", ""

#         if date_defaults:
#             start_default = _format_date(utcnow().date() - timedelta(days=lookback_days + 1))
#             end_default = _format_date(utcnow().date() - timedelta(days=1))

#         # numeric prefix to control lexicographic sort order in notebook ui
#         db_utils.widgets.text("startDate", start_default, "1. startDate")
#         db_utils.widgets.text("endDate", end_default, "2. endDate")
#         deployment_mode_descriptor = "3. deploymentMode"

#     db_utils.widgets.dropdown(
#         "deploymentMode", default_deployment_mode, ["dev", "staging", "prod"], deployment_mode_descriptor
#     )


# def setup_yes_no_widget(name: str, *, title: str = None, default: str = "no") -> None:
#     """Creates a widget with a yes/no dropdown.

#     Args:
#         name (str): name of the widget to use to retrieve the value
#         title (str, optional): title of widget to appear in UI. Defaults to None.
#         default (str, optional): Default value for widget if user doesn't select. Defaults to "no".

#     Raises:
#         ValueError: Invalid default option
#         ValueError: Default not specified
#     """
#     options = ["no", "yes"]
#     if default and default not in options:
#         raise ValueError(f"{default} is not a valid option in {options}")
#     if not default:
#         raise ValueError("A default is required")
#     get_db_utils().widgets.dropdown(name, default, options, title or name)


# def setup_date_partition_widget():
#     """Creates a Date widget with 'date' as the ID defaulted to today's date.

#     This is useful for daily snapshot tables that do not support multi-day runs or backfills.
#     """
#     db_utils = get_db_utils()
#     date_default = _format_date(utcnow().date() - timedelta(days=1))
#     db_utils.widgets.text("date", date_default, "Date")


# def get_widget_value(arg_name: str, default_value: str = None) -> str:
#     """
#     Gets the value of a widget given its name, with an optional default value.

#     If no default value is provided, then the widget value will be returned as is, assuming it did
#     not result in an error, in which case the error is raised.

#     If a default value is provided, then it will be returned whenever there is an error getting
#     the widget value or if the widget value is None/empty.
#     """

#     try:
#         widget_value = get_db_utils().widgets.get(arg_name.strip())
#     except Exception:
#         if default_value is None:
#             raise
#         else:
#             widget_value = None

#     if default_value is None or widget_value:
#         return widget_value
#     else:
#         return default_value


# def get_bool_widget_value(arg_name: str) -> bool:
#     """Gets a widget value that should be either a True or False string and returns the boolean value.

#     Args:
#         arg_name (str): widget name

#     Raises:
#         ValueError: widget has no value
#         ValueError: widget has invalid value

#     Returns:
#         bool: widget value converted to bool
#     """
#     val = get_widget_value(arg_name)
#     if val is None:
#         raise ValueError(f"No value for {arg_name}")
#     val = val.lower()
#     if val not in ["true", "false"]:
#         raise ValueError(f"Invalid boolean value: {val}")
#     return val == "true"


# def get_deployment_mode_from_widget() -> str:
#     deployment_mode = get_widget_value("deploymentMode")
#     DeploymentMode.check_value(deployment_mode)
#     return deployment_mode


# def maybe_nest_asyncio():
#     """
#     Notebook cells are already running inside an event loop.  This creates a problem when we call non-async
#     methods which then in turn attempt to call async methods.  In order to do this they would need to create a new
#     event loop or reuse the existing one, which is not possible.  The only clean way to fix this is to make all the
#     function async to the point where the async method is called, which is impractical.

#     nest_asyncio provides an alternative, where it patches asyncio to allow nested asyncio.
#     """
#     if is_notebook() and asyncio.get_event_loop().is_running():
#         import nest_asyncio

#         nest_asyncio.apply()


# def split_multiquery(queries: str) -> List[str]:
#     """splits a single query string into multiple distinct queries based on semicolons

#     Spark will throw an error if you have it run a query with multiple queries in it
#     split by semicolons. This method makes it easy to automatically split the query by
#     the semicolons and maintain the order.

#     # TODO: this has been copied from lib.omni_parser and modified to handle comments

#     Args:
#         queries (str): original query containing 1 or more queries

#     Returns:
#         List[str]: list of queries
#     """

#     def empty_line(_):
#         return ""

#     results = []
#     for query in queries.split(";"):
#         # remove any comment lines.  this ensure we won't try to execute a query that
#         # only has comments.
#         query = re.sub(r"^\s*--.*$", empty_line, query, flags=re.MULTILINE)

#         # make sure the query has some content or we'll get an error trying to execute it
#         if query.strip():
#             results.append(query + ";")

#     return results


# def multi_spark_sql(queries: str) -> None:
#     """Splits and executes multiple spark queries

#     Args:
#         queries (str): Semicolon delimited queries to execute
#     """
#     spark = get_spark()
#     result = None
#     for query in split_multiquery(queries):
#         result = spark.sql(query)
#     return result


def display_iframe(url: str, *, height: int = 500, width: Union[int, str] = "100%") -> None:
    """Creates an iframe in the notebook that opens the given URL.

    Args:
        url (str): url to open in iframe
        height (int, optional): height of iframe. Defaults to 500.
        width (Union[int, str], optional): width of iframe. Defaults to "100%".
    """
    get_global("display")(
        IPython.display.HTML(
            f'<div><iframe src="{url}" width="{width}" height="{height}" '
            'allow="autoplay; camera; microphone; clipboard-read; clipboard-write;" frameborder="0" allowfullscreen>'
            "</iframe></div>"
        )
    )


def get_driver_proxy_url(port: Union[int, str]) -> str:
    """Gets a URL that connects to a port on the driver node via the driver proxy.

    When launching an app connected to 0.0.0.0 on a given port in the driver node, you can connect to the app
    from the notebook using this function by providing the port.

    Args:
        port (Union[int, str]): the port to connect to

    Returns:
        str: the URL that accesses the port on the driver
    """
    context = get_notebook_context()
    host = context["tags"]["browserHostName"]
    workspace_id = context["tags"]["orgId"]
    cluster_id = context["tags"]["clusterId"]
    return f"https://{host}/driver-proxy/o/{workspace_id}/{cluster_id}/{port}/"


def gradio_launch(interface, height: int = None, width: Union[int, str] = None) -> None:
    """Launches a gradio interface (https://gradio.app/) in the notebook.

    Gradio doesn't work out of the box in Databricks notebooks because it expects to be able to connect
    to the localhost at the port it binds to.  Instead we need to connect through the driver proxy URL.
    To fix this, we lauch without being inline in the notebook, then we display the iframe ourselves.

    Args:
        interface (gradio.Interface): the gradio interface to launch
    """

    launch_kwargs = {}
    if height:
        launch_kwargs["height"] = height
    if width:
        launch_kwargs["with"] = width
    interface.launch(server_name="0.0.0.0", inline=False, **launch_kwargs)
    url = get_driver_proxy_url(interface.server_port)
    display_iframe(url, width=interface.width, height=interface.height)


# def display_web_terminal(*, height: int = None) -> None:
#     """Creates an iframe in the notebook cell that connects to the web terminal.

#     Args:
#         height (int, optional): Specify the height in pixels. Defaults to None.
#     """
#     iframe_kwargs = {}
#     if height:
#         iframe_kwargs["height"] = height
#     display_iframe(get_driver_proxy_url(7681), **iframe_kwargs)
