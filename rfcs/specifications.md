# Specifications & TODO

## Development

- [ ] enable print statement inside docker for debugging

## REST Framework

- [x] Replace DRF with django ninja
- [ ] Handle permissions for rest end points
- [ ] User setting to allow access to rest endpoints
- [ ] Create base for htmx and widgets

## Tests

- [ ] Setup integration test environment with the redis, rq scheduler, rq worker
- [ ] Remove fireside_tests, make chat/tasks a core app + example and use that for the integration testing

## Permissions & ACLs

- [x] OLP Change read/write to view/change
- [ ] ACLs for list view dose not work, blank out fields? for OLP?
- [x] Module level ACLs not working with Admin (cant see fields even though set)
- [ ] Permissions for list display
  - how to do this fast?
  - add a seperate permission for list display?
  - compiling user permissions from all objects would be slow
  - make seperate table to keep track of list_permissions and update? too tedious to keep it updated
  - or just ignore totally?
  - current it needs global change to be able edit, else its readonly
- [ ] Add test cases for all combinations
  - global read
  - global write
  - global delete
  - global none + obj read
  - global none + obj write
  - ...
- [ ] Try adding thousands of items and test speed of queryset

## Tasks

- [ ] `fireside.tasks.apps.ready` should not reschedule tasks on management commands but only on app start
- [ ] `fireside.utils.tasks.task` Add schema based on type hints of function
- [ ] Replace inputs JSONField with SchemaJSONField (validate with `task_definitions.<task>.schema`)
- [ ] Store results, errors
- [ ] Add is_valid/is_active and reflect on admin page (if `TaskDefinition` changes) (remove from admin column)
- [ ] Task Definition change of function name should not remove it from the database, but should just update the import path, else just changing a function name will break any tasks which use the definition
- [ ] Task should map to rq job with kwargs like timeout and be callable in code
- [ ] Ability to run task with args, kwargs from admin
- [ ] Task/TaskSchedule Admin "Run Task" permissions
- [x] Add realtime pretty cron when typing in admin

- [x] remove name and description from TaskSchedule (use readable cron name and name/description from task)
- [x] Display cron as readable string "every saturday 10 pm"
- [x] Tasks should be renamed to TaskSchedule
- [x] TaskDefinition should be renamed to Task
- [x] Add action to run task immediately
- [x] `Task` should have a .delay method
- [x] Move `tasks` into `fireside.tasks`

## Utils

- [ ] Add enabled/disabled mask to ActivatableModel
- [ ] Permissions for enable/disable for ActivatableModel
- [x] Add admin action to disable/enable ActivableModel in fireside admin
- [x] Add red/green indicator for ActivableModel in fireside admin
- [x] Use full path imports instead of dumping all functions in utils (reduce circular imports)
- [x] Write `ActivatableModel` object manager with active qs
- [ ] Write test cases for `ActivatableModel` object manager with active qs

## Dynamic Widgets

- [x] Hook up htmx to admin
- [x] Rename `HintsTextInput` to `FiresideTextInput`
- [x] Find a better way to get the URL instead of hardcoding `HintsTextInput(hints_url='/fireside/api/utils/cron_pretty')`
- [ ] Fix htmx csrf error in `addEventListener`
