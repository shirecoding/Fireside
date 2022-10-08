# TODOs

## Framework

- Replace DRF with django ninja

## Tests

- Setup integration test environment with the redis, rq scheduler, rq worker

## Permissions & ACLs

- OLP Change read/write to view/change
- ACLs for list view dose not work, blank out fields? for OLP?

- [DONE] Module level ACLs not working with Admin (cant see fields even though set)

## Tasks

- `fireside.tasks.apps.ready` should not reschedule tasks on management commands but only on app start
- `fireside.utils.tasks.register_task` Add schema based on type hints of function
- Task Definition change of function name should not remove it from the database, but should just update the import path, else just changing a function name will break any tasks which use the definition
- Replace inputs JSONField with SchemaJSONField (validate with `task_definitions.<task>.schema`)
- Display cron as readable string "every saturday 10 pm"
- Store results, errors
- Add action to run task immediately
- Add is_valid and reflect on admin page (if `TaskDefinition` changes)
- [DONE] Move `tasks` into `fireside.tasks`
