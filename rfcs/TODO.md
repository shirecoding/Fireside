# TODOs

## REST Framework

- Replace DRF with django ninja
- Handle permissions for rest end points
- User setting to allow access to rest endpoints

## Tests

- Setup integration test environment with the redis, rq scheduler, rq worker

## Permissions & ACLs

- OLP Change read/write to view/change
- ACLs for list view dose not work, blank out fields? for OLP?

- [DONE] Module level ACLs not working with Admin (cant see fields even though set)

## Tasks

- `fireside.tasks.apps.ready` should not reschedule tasks on management commands but only on app start
- `fireside.utils.tasks.task` Add schema based on type hints of function

- Replace inputs JSONField with SchemaJSONField (validate with `task_definitions.<task>.schema`)

- Store results, errors
- Add is_valid and reflect on admin page (if `TaskDefinition` changes)

- Task Definition change of function name should not remove it from the database, but should just update the import path, else just changing a function name will break any tasks which use the definition

- Task should map to rq job with kwargs like timeout and be callable in code
- Ability to run task with args, kwargs from admin

- Add realtime pretty cron when typing in admin

- [Done] remove name and description from TaskSchedule (use readable cron name and name/description from task)
- [Done] Display cron as readable string "every saturday 10 pm"
- [Done] Tasks should be renamed to TaskSchedule
- [Done] TaskDefinition should be renamed to Task
- [DONE] Add action to run task immediately
- [DONE]`Task` should have a .delay method
- [DONE] Move `tasks` into `fireside.tasks`

## Utils

- Add enabled/disabled mask to ActivatableModel
- Add red/green indicator for ActivableModel in fireside admin
- [Done] Use full path imports instead of dumping all functions in utils (reduce circular imports)
