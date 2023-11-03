# lst-pressure

Python module for calculating LST pressure based on scheduled observations

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [API Docs](#api-docs)
- [Motivation](#motivation)
  - [Design](#design)
  - [Normalizing intervals](#normalizing-intervals)
- [Installation and usage](#installation-and-usage)
- [Local development](#local-development)
  - [Testing](#testing)
  - [Publishing](#publishing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# [API Docs](https://ska-sa.github.io/lst-pressure/)

# Motivation

Observation blocks encompass various time-related constraints, notably the Local Sidereal Time (LST) window of a source rise/fall, and some constraints related to UTC. As LST and UTC time can diverge over a year, it can be hard to quickly identify candidate UTC times based on LST ranges in conjunction with constraints related to sun/UTC.

This library should facilitate easily comparing intervals defined in LST with intervals defined in UTC. Essentially this library is an opinionated wrapper over a Python implementation of an [interval tree](https://en.wikipedia.org/wiki/Interval_tree) called [intervaltree](https://pypi.org/project/intervaltree/).

## Design

Each UTC day includes intervals in which an observation can be scheduled. These intervals are called:

- `ALL_DAY`
- `AVOID_SUNRISE_SUNSET`
- `AVOID_SUNSET_SUNRISE`
- `NIGHT_ONLY`

To identify the UTC intervals that satisfy scheduling constraints of observations, generate a list of LST intervals over `N` days, that are labelled with UTC information. For example:

```
[ lst_t0 : lst_t1 ]: { type: <AVOID_SUNRISE_SUNSET>, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
[ lst_t0 : lst_t1 ]: { type, utc_0, utc_1 }
... etc
```

Then, for an observation with an LST window defined, query that list for all intervals that overlap the observation LST window. The resultant list can then be filtered by UTC-related information such as sunset/sunrise and other constraints (i.e. observation duration). **Noted that the LST window in the context of this package defines possible _start_ times of observations. It's up to the user to ensure that the start time of an observation takes into account the required observation duration.**

The result is a list of UTC calendar days that a particular observation can be scheduled along with UTC start/end times for applicable observations. Done for many observations, it's easy to create a UTC calendar with potential observation events that can serve as the basis for more complicated scheduling logic (for example, picking the best observation to schedule on a particular day).

## Normalizing intervals
Intervals should strictly have `t1 > t0`, which means that in some cases intervals defined by two LST times must be normalized. For example, an LST range that begins on day0 and ends on day1 will have a start time that is higher than the end time. In this case, add a full LST day to the end time at both indexing time and at query time. Likewise, when an interval - for example `NIGHT_ONLY` - begins on the preceding day, the portion of the interval that falls on the current day is indexed. 

# Installation and usage

Install the package from [PyPi](https://pypi.org/project/lst-pressure/)

```sh
pip install lst-pressure
```

The `Observation` class represents an observation block with given Local Sidereal Time (LST) window and UTC constraints. 

```python
import lstpressure

observation = lstpressure.Observation(
  id="some-id",
  lst_window_start=2,
  lst_window_end=12,
  utc_constraints=[I.NIGHT_ONLY],
  duration=2
)
```

Check if an observation can be scheduled on a particular day, or within a date range

```python
is_valid = lstpressure.observable(observation, "20231031")

# or

is_valid = lstpressure.observable(observation, "20231031", "20231105")

# or check many observations against a single date range
calendar = lstpressure.LSTCalendar('20231001', '20231001')
is_obs1_valid = lstpressure.observable(Observation(...), calendar)
is_obs2_valid = lstpressure.observable(Observation(...), calendar)
is_obs3_valid = lstpressure.observable(Observation(...), calendar)
etc.
```

Or get a list of observations that can be scheduled on a particular date

```python
for dt in lstpressure.LSTCalendar(
    "20231001",
    "20231010",
    observations=[observation]
).dates:
    observable = dt.observations()
```

# Local development

Ensure that you have Python v3.8.10 installed on your system, and then initiate the repository for local development with the following commands:

```sh
source env.sh
```

## Testing

To test the codebase, run `pytest` in the terminal. For live testing, use the [`chomp`](https://github.com/guybedford/chomp#install) task runner. Install either via Cargo (Rust), or via NPM (Node.js)

```sh
source env.sh
chomp --watch
```

## Publishing

The publish workflow is described in [.github/workflows/publish.yml](.github/workflows/publish.yml), and is triggered on pushes to the `release` branch. The published package is available on [PyPI](https://pypi.org/project/lst-pressure/). Make sure to first increment the version in [setup.py](./setup.py) before pushing to the release branch.
