# scalpel_analytics_model

This simple python project is a solution to the Shopping Cart interview question at QoKoon.

The goal is to build a backend service that supports a shopping platform or a cashier system which provides
a detailed pricing of any shopping carts during checkout. The service should identify the unit price of a product,



# Project top-level directory structure

    ├── files                       # config yaml files (including postgres database config)
    ├── scalpel_analytics_model     # main project folder
        ├── compliance              # functions that evaluate and populate compliance scores
            ├── ...
        ├── load                    # functions that load and populate data
            ├── load.py
        ├── model                   # database model
            ├── base.py             # base classes
            ├── compliance.py       # compliance classes (based on different measures), e.g. IssueCompliance
            ├── core.py             # core classes including Patient, Procedure & Operation
            ├── event.py            # ORBot checklist event classes (raw and aggregated for each operation)
            ├── hospital.py         # hospital-related classes, e.g. theatre, clinicians, teams
        ├── __init__.py
        ├── add_data                # scripts that populate mock data to database
        ├── exc.py                  # exceptions
    ├── scripts                     # scripts for populating (mock) data and starting Docker & database
        ├── ...
    ├── tests                       # Automated unit test files
        ├── mock_data               # mock data (generated by ORBot and queried from event APIs) for testing
        ├── ...
    ├── Dockerfile
    ├── Jenkinsfile
    └── README.md


# Requirements





# Database schema

This analytics database structure is operation-oriented, i.e. compliance scores and checklist events are
aggregated as per each single operation in the corresponding tables.

## Core

### Patient (de-identified)
        ├── id                          (pseudo-ID, primary key, integer)
        ├── age                         (range, k-anonymised)
        ├── bmi                         (range, k-anonymised)
        ├── height                      (range, k-anonymised)
        ├── weight                      (range, k-anonymised)
    ├──linked & backpopulate
        ├── operation_id                (operation ID, foreign key, string)
        ├── operation                   (operation)

### Procedure (one entry for each operation procedures)
        ├── id                          (ID, primary key, integer)
        ├── opcs_code                   (OPCS-4 code, string)
        ├── name                        (Full name of the procedure, string)
        ├── speciality                  (speciality of the procedures, string)
        ├── site                        (surgical site, e.g. right/bottom, string)
    ├──linked & backpopulate
        ├── operation_id                (operation ID, foreign key)
        ├── operation                   (operation)

### Position (Patient positions during surgery)
        ├── id                          (ID, primary key, integer)
        ├── name                        (Name of patient position, e.g. Supine, string)
    ├──linked & backpopulate
        ├── operations                   (operations, list)

### Operation
        ├── id                          (pseudo-ID, primary key, string)
        ├── expected_duration           (expected operation duration in mins, integer)
        ├── scheduled_start_time        (scheduled start-time, datetime)
        ├── start_time                  (actual start-time, datetime)
    ├──core, linked & backpopulate
        ├── patient                     (patient)
        ├── procedures                  (procedures, list)
        ├── positions                   (patient positions, lists)
    ├──hospital-related, linked & backpopulate
        ├── theatre_id                  (theatre ID, foreign key, string)
        ├── theatre                     (operating theatre where the operation taken place)
        ├── team_id                     (surgical team ID, foreign key, string)
        ├── team                        (surgical team)
    ├──checklist events-related, linked & backpopulate
        ├── questions                   (ORBOt checklist questions aggregated results, e.g. # of views per question, list)
        ├── question_events             (ORBOT checklist question raw events, list)
        ├── question_groups             (ORBOt checklist question groups aggregated results, list)
        ├── question_group_events       (ORBOT checklist question group raw events, list)
        ├── step                        (ORBOt checklist step aggregated results, list)
        ├── step_events                 (ORBOT checklist step raw events, list)
        ├── stage                       (ORBOT checklist stage, e.g. Sign-In, aggregated results, list)
        ├── stage_events                (ORBOT checklist stage raw events, list)


## Hospital-related

Note that all historical records including every (daily) updates to e-form are recorded instead of a dynamic
table where there is an unique entry for each single entities. This is to take into account of the fact that
past surgical records must be linked to the correct historical hospital records instead of the most updated ones.

### Theatre
        ├── id                          (unique ID for individual record, primary key, string)
        ├── created_timestamp           (when the entry is created, TIMESTAMP)
        ├── theatre_id                  (ID for each single theatre, string)
        ├── label                       (theatre label, string)
        ├── name                        (theatre name, string)
        ├── opening_time                (opening hour, Time)
        ├── closing_time                (closing hour, Time)
    ├──linked & backpopulate
        ├── suite_id                    (suite ID, foreign key, string)
        ├── suite                       (suite)
        ├── operations                  (operation, list)


### Suite
        ├── id                          (unique ID for individual record, primary key, string)
        ├── created_timestamp           (when the entry is created, TIMESTAMP)
        ├── suite_id                    (ID for each single suite, string)
        ├── name                        (suite name, string)
        ├── opening_time                (opening hour, Time)
        ├── closing_time                (closing hour, Time)
    ├──linked & backpopulate
        ├── theatres                    (theatres, list)

### Clinician
        ├── id                          (unique ID for individual record, primary key, string)
        ├── created_timestamp           (when the entry is created, TIMESTAMP)
        ├── clinician_id                (ID for each single clinician, string)
        ├── name                        (name, string)
        ├── role                        (role e.g. surgeon/nurse, string)
        ├── is_champion                 (whether the clinician is the "champion"/practitioner, boolean)
    ├──linked & backpopulate
        ├── teams                       (surgical teams, list)

### Team, defined by a unique set of (champion) clinicians
        ├── id                          (unique ID for individual record, primary key, string)
        ├── created_timestamp           (when the entry is created, TIMESTAMP)
        ├── team_id                     (numeric ID for each team, integer)
        ├── team_clinician_id           (ID formed by clinicians ID/name, string)
        ├── label                       (label, string)
    ├──linked & backpopulate
        ├── clinicians                  (clinicians, list)
        ├── operations                  (operations, list)

## ORBot checklist events

Raw timestamp event

============================

### QuestionEvent
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID)
        ├── state                       (started/completed/interrupted, string)
        ├── timestamp                   (when the event was created, datetime)
        ├── response                    (input response if the event is a "completed" event, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operations

### QuestionGroupEvent
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID)
        ├── state                       (started/completed/interrupted, string)
        ├── timestamp                   (when the event was created, datetime)
        ├── response                    (input response if the event is a "completed" event, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operations

### StepEvent
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID)
        ├── state                       (started/completed/interrupted, string)
        ├── timestamp                   (when the event was created, datetime)
        ├── response                    (input response if the event is a "completed" event, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operations

### StageEvent
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID)
        ├── state                       (started/completed/interrupted, string)
        ├── timestamp                   (when the event was created, datetime)
        ├── response                    (input response if the event is a "completed" event, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operations

Aggregated

============================

### Question
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the question e.g. on dashboards/report, string)
        ├── question_text               (full question text, string)
        ├── is_followon                 (whether the question is a follow-on, boolean)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──deduced/aggregated
        ├── total_time_spent            (total seconds spent on the task, integer)
        ├── final_respone               (final response, string)
        ├── number_of_views             (# of "started" events, integer)
        ├── number_of_responses         (# of "completed" events, integer)
        ├── number_of_interruptions     (# of "interrupted" events, integer)
        ├── is_completed                (boolean)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### QuestionGroup
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the question group e.g. on dashboards/report, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──deduced/aggregated
        ├── total_time_spent            (total seconds spent on the task, integer)
        ├── start_timestamp             (first event of the task, datetime)
        ├── end_timestamp               (last event of the task, datetime)
        ├── number_of_views             (# of "started" events, integer)
        ├── number_of_responses         (# of "completed" events, integer)
        ├── number_of_interruptions     (# of "interrupted" events, integer)
        ├── is_completed                (boolean)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### Step
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the checklist step e.g. on dashboards/report, string)
        ├── stage                       (corresponding ORBot checklist stage, string)
    ├──deduced/aggregated
        ├── total_time_spent            (total seconds spent on the task, integer)
        ├── start_timestamp             (first event of the task, datetime)
        ├── end_timestamp               (last event of the task, datetime)
        ├── number_of_views             (# of "started" events, integer)
        ├── number_of_responses         (# of "completed" events, integer)
        ├── number_of_interruptions     (# of "interrupted" events, integer)
        ├── is_completed                (boolean)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### Stage
        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, e.g. sign_in, string)
        ├── display                     (display name of the checklist stage e.g. on dashboards/report, string)
    ├──deduced/aggregated
        ├── total_time_spent            (total seconds spent on the task, integer)
        ├── start_timestamp             (first event of the task, datetime)
        ├── end_timestamp               (last event of the task, datetime)
        ├── number_of_views             (# of "started" events, integer)
        ├── number_of_responses         (# of "completed" events, integer)
        ├── number_of_interruptions     (# of "interrupted" events, integer)
        ├── is_completed                (boolean)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

## SSC safety compliance

These are tables about safety compliance (based on SSC checklist usage) of each operation. The compliance ratings
are computed using scoring scheme in the project scalpel_data_model. All started/monitored operations have one
entry for each check items included in the scoring scheme. NOTE: Version reference is needed as these data are
scoring scheme/ML model dependent

### IssueCompliance

compliance scores of each check items for the measure based on checklist responses when an issue or concern is raised

        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the question e.g. on dashboards/report, string)
        ├── question_text               (full question text, string)
        ├── is_mandatory                (if the corresponding task is mandatory or not, boolean)
        ├── max_score                   (item weighted score in compliance scoring scheme, integer)
    ├──deduced/aggregated
        ├── final_respone               (final response, string)
        ├── is_compliant                (boolean)
        ├── score                       (deduced compliance score, integer)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### DurationCompliance

compliance scores of each check items for the measure based on time spent on the checklist tasks

        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the question e.g. on dashboards/report, string)
        ├── question_text               (full question text, string)
        ├── is_mandatory                (if the corresponding task is mandatory or not, boolean)
        ├── max_score                   (item weighted score in compliance scoring scheme, integer)
    ├──deduced/aggregated
        ├── total_time_spent            (total time spent on the task in seconds, integer)
        ├── actual_time_minus_recommend (total time spent - min recommend time, integer)
        ├── is_compliant                (boolean)
        ├── score                       (deduced compliance score, integer)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### CompletionCompliance

compliance scores of each check items based on mandatory task completion rates

        ├── id                          (unique ID, primary key, integer)
        ├── task_id                     (ORBot task ID, string)
        ├── display                     (display name of the question e.g. on dashboards/report, string)
        ├── question_text               (full question text, for question tasks only, string)
        ├── max_score                   (item weighted score in compliance scoring scheme, integer)
    ├──deduced/aggregated
        ├── is_compliant                (boolean)
        ├── score                       (deduced compliance score, integer)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)

### ComplianceScore

Deduced compliance ratings for each operation

    ├──deduced
        ├── issue_compliance            (score based on IssueCompliance, float)
        ├── completion_compliance       (score based on completion rates, float)
        ├── duration_compliance         (score based on DurationCompliance, float)
        ├── overall_score               (overall compliance rating, float)
    ├──linked & backpopulate
        ├── operation_id                (operation_id, string)
        ├── operation                   (operation)