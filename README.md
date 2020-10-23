# Bugmon
[![Build Status](https://travis-ci.com/MozillaSecurity/bugmon.svg?branch=master)](https://travis-ci.org/MozillaSecurity/bugmon)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Bugmon is a tool for the automatic analysis of bugs filed against Firefox or Spidermonkey in Mozilla's Bugzilla database. It is capable of automatically confirming open bugs, verifying closed bugs, and bisecting the bug's introduction or fix.

## Table of Contents
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Overview](#overview)
  - [Manual Analysis](#manual-analysis)
    * [Valid Commands](#valid-commands)
    * [Status Flags](#status-flags)
  - [Bug Requirements](#bug-requirements)
    * [Flags and Environment Variables](#flags-and-environment-variables)
    * [Testcase Identification](#testcase-identification)

## Installation
```shell script
git clone https://github.com/MozillaSecurity/bugmon
cd bugmon
poetry install
```
## Basic Usage
```shell script
export BZ_API_ROOT=https://bugzilla.mozilla.org/rest
export BZ_API_KEY=3e94273b56150a4ab62927378e8a98848d09e716

python -m bugmon --bugs [bug_num...]
[2020-03-20 11:00:32] Analyzing bug 1234567 (Status: NEW, Resolution: )
[2020-03-20 11:00:34] Attempting to reproduce bug on mozilla-central 20200320095353-32d6a3f1f83c
[2020-03-20 11:00:36] > Downloading: https://firefox-ci-tc.services.mozilla.com/api/queue/v1/task/YoJI7ae0T9mLJWkYeoPY8g/artifacts/public/build/target.tar.bz2 (87.12MB total)
[2020-03-20 11:01:38] > Verifying build...
[2020-03-20 11:01:49] >> Target closed itself
[2020-03-20 11:01:49] > Launching build with testcase...
[2020-03-20 11:02:53] >> Browser is alive but has crash reports. Terminating...
...
[2020-03-20 12:05:13] Begin bisection...
[2020-03-20 12:05:13] > Start: 2c49e736571bdcf4d8897eab3c3ad6d4a079f664 (20190322012300)
[2020-03-20 12:05:13] > End: 32d6a3f1f83cec54b8190f1993c7fa343406ce20 (20200320095353)
...
[2020-03-20 12:26:12] The bug appears to have been introduced in the following build range:
[2020-03-20 12:26:12] > Start: 51efc4b931f748899be0fa3c9603fc4e07b668b6 (20200302094818)
[2020-03-20 12:26:12] > End: c3270629341670f948584dc15f68d64006ea737f (20200302212732)
[2020-03-20 12:26:12] > Pushlog: https://hg.mozilla.org/mozilla-central/pushloghtml?fromchange=51efc4b931f748899be0fa3c9603fc4e07b668b6&tochange=c3270629341670f948584dc15f68d64006ea737f
[2020-03-20 12:26:12] Changes: {"whiteboard": "[bugmon:bisected,confirmed]"}

```

## Overview
Bugmon will automatically analyse bugs that have the `bugmon` keyword.  The actions performed are based on the current status of the bug.

**Confirmation**
- Bugmon will automatically confirm the reproducibility of bugs where the status is ASSIGNED, NEW, UNCONFIRMED, or REOPENED.
- Bugs that are confirmed as open will also be bisected.
- If the bug cannot be confirmed using the latest available build, Bugmon will attempt to confirm the bug using a build matching the original revision or a revision closest to the bug creation date.  If this succeeds, Bugmon will attempt to bisect which changeset introduced the fix. 

**Verification**
- Bugmon will automatically confirm that the bug has been fixed where the bug status is RESOLVED and the resolution is FIXED.
- Bugmon will also iterate over the tracking flags and attempt to verify each branch marked as FIXED.
       
## Manual Analysis

In addition to Bugmon's automatic analysis, specific actions can be requested via the bug whiteboard using the `bugmon` identifier.  The whiteboard should match the following format:
```
[bugmon:cmd1,cmd2,cmd3...]
```

### Valid Commands

- `confirm` - Request manual bug confirmation
- `verify` - Request manual verification
- `bisect` - Request manual bisection

### Status Flags
In addition to requesting manual actions, some actions can be excluded by adding the following status flags to the bugmon whiteboard. 

- `confirmed` - Bug has already been confirmed
- `verified` - Bug has already been verified
- `bisected` - Bug has already been bisected*

*Bisection may still be performed if a previously unconfirmed bug is confirmed.*

## Bug Requirements
To ensure that your bug is analysed correctly, Bugmon requires specific information to be present.

### Flags and Environment Variables
Bugmon expects comment 0 to include any build flags, runtime flags, or environment variables required to reproduce the bug.

### Testcase Identification
Bugmon will download all non-obsolete attachments and attempt to determine which file to use as a testcase.  Key indicators of testcases are attachment filenames or descriptions that match `/^testcase.*$/`. 

Testcases that span multiple files can either be included as individual attachments or via a single zip file.  However, the filename or description of the testcase entrypoint must match the regex above.
