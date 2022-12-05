import pytest
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.shortcuts import get_object_or_404

from fireside.models import Task, TaskPriority, TaskSchedule
from fireside.utils import function_to_import_path


@pytest.fixture
def starbuck(db) -> User:
    return User.objects.create(username="starbuck")


@pytest.fixture
def adama(db) -> User:
    return User.objects.create(username="adama")


@pytest.fixture
def humans(db) -> Group:
    return Group.objects.create(name="humans")


def dummy_task(*args, **kwargs):
    pass


@pytest.fixture
def task(db) -> Task:
    return Task.objects.create(
        name="Dummy Task",
        description="Dummy Task",
        fpath=function_to_import_path(dummy_task),
    )


@pytest.fixture
def task_schedule(db, task) -> TaskSchedule:

    task_schedule = TaskSchedule.objects.create(
        task=task,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
        inputs={},
    )
    assert TaskSchedule.objects.get(task=task).task == task

    # update with new field level permissions
    call_command("update_permissions")
    call_command("remove_stale_contenttypes")

    return task_schedule


def test_permissions_created(db, task_schedule):

    perms = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(TaskSchedule)
    )

    fields = {f.name for f in TaskSchedule._meta.get_fields() if f.editable}
    assert {
        "activate_on",
        "deactivate_on",
        "task",
        "inputs",
        "cron",
        "repeat",
        "priority",
        "timeout",
    }.issubset(fields)

    # test created FLP
    model_name = TaskSchedule._meta.model_name
    for f in fields:
        assert any([p.codename == f"change_{model_name}_{f}" for p in perms])
        assert any([p.codename == f"view_{model_name}_{f}" for p in perms])


def test_field_permissions(task_schedule, humans, starbuck):

    # no perms to start
    assert bool(starbuck.get_all_permissions()) == False

    fields = {f for f in TaskSchedule._meta.get_fields() if f.editable}
    model_name = TaskSchedule._meta.model_name

    for f in fields:

        # test get permissions
        perm = TaskSchedule.get_permission_by_codename(f"change_{model_name}_{f.name}")
        assert TaskSchedule.get_field_permission(f, "change") == perm

        assert (
            TaskSchedule.get_field_permission(getattr(TaskSchedule, f.name), "change")
            == perm
        )

        # test add & remove user perm
        assert starbuck.has_perm(f"fireside.change_{model_name}_{f.name}") == False
        starbuck.user_permissions.add(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"fireside.change_{model_name}_{f.name}") == True

        starbuck.user_permissions.remove(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"fireside.change_{model_name}_{f.name}") == False

        # test add & remove group perm
        humans.permissions.add(perm)
        humans.user_set.add(starbuck)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"fireside.change_{model_name}_{f.name}") == True

        humans.permissions.remove(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"fireside.change_{model_name}_{f.name}") == False
