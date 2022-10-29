# TODOs

## REST Framework

- [x] Replace DRF with django ninja
- Handle permissions for rest end points
- User setting to allow access to rest endpoints

## Tests

- Setup integration test environment with the redis, rq scheduler, rq worker

## Permissions & ACLs

- OLP Change read/write to view/change
- ACLs for list view dose not work, blank out fields? for OLP?
- [x] Module level ACLs not working with Admin (cant see fields even though set)

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

- [x] remove name and description from TaskSchedule (use readable cron name and name/description from task)
- [x] Display cron as readable string "every saturday 10 pm"
- [x] Tasks should be renamed to TaskSchedule
- [x] TaskDefinition should be renamed to Task
- [x] Add action to run task immediately
- [x] `Task` should have a .delay method
- [x] Move `tasks` into `fireside.tasks`

## Utils

- Add enabled/disabled mask to ActivatableModel
- Add red/green indicator for ActivableModel in fireside admin
- [x] Use full path imports instead of dumping all functions in utils (reduce circular imports)
