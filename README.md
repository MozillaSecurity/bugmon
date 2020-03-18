# Bugmon

Bugmon is a tool for the automatic analysis of bugs filed against Firefox or Spidermonkey in Mozilla's Bugzilla database. It is capable of automatically confirming open bugs, verifying closed bugs, and bisecting the bugs introduction or fix.

## Table of Contents
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
  - [Overview](#overview)
    - [Automatic Actions](#actions)
      - [Confirmation](#confirmation)
      - [Verification](#verification)
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
python -m bugmon --bugs [bug_num...]
```

## Overview
Bugmon will automatically analyse bugs that have the `bugmon` keyword.  The actions performed are based on the current status of the bug.

### Automatic Actions
#### Confirmation
- Bugmon will automatically confirm the reproducibility of bugs where the status is ASSIGNED, NEW, UNCONFIRMED, or REOPENED.
- Bugs that are confirmed as open will also be bisected.
- If the bug cannot be confirmed using the latest available build, Bugmon will attempt to confirm the bug using a build matching the original revision or a revision closest to the bug creation date.  If this succeeds, Bugmon will attempt to bisect which changeset introduced the fix. 
#### Verification
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