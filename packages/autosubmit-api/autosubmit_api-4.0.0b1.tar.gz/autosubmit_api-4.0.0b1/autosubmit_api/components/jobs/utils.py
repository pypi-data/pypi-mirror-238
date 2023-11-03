#!/usr/bin/env python

from datetime import date
from pickle import NONE
from ...autosubmit_legacy.job.job_common import Status
from typing import List, Dict

wrapped_title_format = " <span class='badge' style='background-color:#94b8b8'>Wrapped {0} </span>"
source_tag = " <span class='badge' style='background-color:#80d4ff'>SOURCE</span>"
target_tag = " <span class='badge' style='background-color:#99ff66'>TARGET</span>"
sync_tag = " <span class='badge' style='background-color:#0066ff; color:white'>SYNC</span>"
checkmark_tag = " <span class='badge' style='background-color:#4dffa6'>&#10004;</span>"

completed_tag_with_anchors = " <span class='badge' style='background-color:%B'> %C / %T COMPLETED</span>"
running_tag_with_anchors = " <span class='badge' style='background-color:green; color:#fff'>%R RUNNING</span>"
queuing_tag_with_anchors = " <span class='badge' style='background-color:pink'>%Q QUEUING</span>"
failed_tag_with_anchors = " <span class='badge' style='background-color:red'>%F FAILED</span>"
held_tag_with_anchors = " <span class='badge' style='background-color:#fa8072; color:#fff'>%H HELD</span>"

# Status.HELD, Status.PREPARED
SUBMIT_STATUS = {Status.COMPLETED, Status.FAILED, Status.QUEUING, Status.RUNNING, Status.SUBMITTED}
START_STATUS = {Status.COMPLETED, Status.FAILED, Status.RUNNING}
FINISH_STATUS = {Status.COMPLETED, Status.FAILED}

def is_a_completed_retrial(fields):
  # type: (List[str]) -> bool
  """ Identifies one line of _TOTAL_STATS file """
  if len(fields) == 4:
    if fields[3] == 'COMPLETED':
      return True
  return False

def get_corrected_submit_time_by_status(status_code, submit_time):
  # type: (int, str) -> str
  if status_code in SUBMIT_STATUS:
    return submit_time
  return None

def get_corrected_start_time_by_status(status_code, start_time):
  # type: (int, str) -> str
  if status_code in START_STATUS:
    return start_time
  return None

def get_corrected_finish_time_by_status(status_code, finish_time):
  # type: (int, str) -> str
  if status_code in FINISH_STATUS:
    return finish_time
  return None

def get_status_text_color(status_code):
  # type: (int) -> str
  if status_code in [Status.RUNNING, Status.FAILED, Status.HELD]:
    return "#fff"
  return "#000"


def get_folder_checkmark(completed_count, jobs_in_folder_count):
  # type: (int, int) -> str
  if completed_count == jobs_in_folder_count:
      return checkmark_tag
  return ""

def get_folder_completed_tag(completed_count, jobs_in_folder_count):
  # type: (int, int) -> str
  tag = ""
  if completed_count == jobs_in_folder_count:
      tag = "<span class='badge' style='background-color:yellow'>"
  else:
      tag = "<span class='badge' style='background-color:#ffffb3'>"
  return  "{0} {1} / {2} COMPLETED</span>".format(tag, completed_count, jobs_in_folder_count)

def get_folder_running_tag(running_count):
  # type: (int) -> str
  if running_count > 0:
    return " <span class='badge' style='background-color:green; color:#fff'>{0} RUNNING</span>".format(running_count)
  return ""

def get_folder_queuing_tag(queuing_count):
  # type: (int) -> str
  if queuing_count > 0:
    return " <span class='badge' style='background-color:pink'>{0} QUEUING</span>".format(queuing_count)
  return ""

def get_folder_failed_tag(failed_count):
  # type: (int) -> str
  if failed_count > 0:
    return " <span class='badge' style='background-color:red'>{0} FAILED</span>".format(failed_count)
  return ""

def get_folder_held_tag(held_count):
  # type: (int) -> str
  if held_count > 0:
    return " <span class='badge' style='background-color:#fa8072; color:#fff'>{0} HELD</span>".format(held_count)
  return ""


def get_date_folder_tag(title, startdate_count):
  # type: (str, int) -> str

  # set the proper color
  if title == "COMPLETED":
      color = "yellow"
  if title == "WAITING":
      color = "#aaa"
  if title == "SUSPENDED":
      color = "orange"
  tag = "<span class='badge' style='background-color:{0}'>".format(color)
  return  "{0} {1} / {2} {3} </span>".format(tag, startdate_count, startdate_count, title)

def get_folder_date_member_title(expid, formatted_date, member, date_member_jobs_count, counters):
  # type: (str, str, str, int, Dict[int, int]) -> str
  return "{0}_{1}_{2} {3}{4}{5}{6}{7}{8}".format(
      expid,
      formatted_date,
      member,
      get_folder_completed_tag(counters[Status.COMPLETED], date_member_jobs_count),
      get_folder_failed_tag(counters[Status.FAILED]),
      get_folder_running_tag(counters[Status.RUNNING]),
      get_folder_queuing_tag(counters[Status.QUEUING]),
      get_folder_held_tag(counters[Status.HELD]),
      get_folder_checkmark(counters[Status.COMPLETED], date_member_jobs_count)
  )

def get_folder_package_title(package_name, jobs_count, counters):
  # type: (str, int, Dict[int, int]) -> str
  return "Wrapper: {0} {1}{2}{3}{4}{5}{6}".format(
      package_name,
      get_folder_completed_tag(counters[Status.COMPLETED], jobs_count),
      get_folder_failed_tag(counters[Status.FAILED]),
      get_folder_running_tag(counters[Status.RUNNING]),
      get_folder_queuing_tag(counters[Status.QUEUING]),
      get_folder_held_tag(counters[Status.HELD]),
      get_folder_checkmark(counters[Status.COMPLETED], jobs_count)
  )