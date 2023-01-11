import pytest
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from fireside.models import TaskSchedule


@pytest.fixture
def starbuck(db) -> User:
    return User.objects.create(username="starbuck")


@pytest.fixture
def adama(db) -> User:
    return User.objects.create(username="adama")


@pytest.fixture
def humans(db) -> Group:
    return Group.objects.create(name="humans")


def test_permissions_created(db, logging_task_schedule):

    perms = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(TaskSchedule)
    )

    fields = {f.name for f in TaskSchedule._meta.get_fields() if f.editable}

    assert {
        "activate_on",
        "deactivate_on",
        "task_preset",
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


def test_field_permissions(logging_task_schedule, humans, starbuck):

    # test no perms at start
    assert bool(starbuck.get_all_permissions()) is False

    app_name = "fireside"
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
        assert starbuck.has_perm(f"{app_name}.change_{model_name}_{f.name}") is False
        starbuck.user_permissions.add(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"{app_name}.change_{model_name}_{f.name}") is True

        starbuck.user_permissions.remove(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"{app_name}.change_{model_name}_{f.name}") is False

        # test add & remove group perm
        humans.permissions.add(perm)
        humans.user_set.add(starbuck)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"{app_name}.change_{model_name}_{f.name}") is True

        humans.permissions.remove(perm)
        starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
        assert starbuck.has_perm(f"{app_name}.change_{model_name}_{f.name}") is False


def test_object_permissions(logging_task_schedule, humans, starbuck, adama):

    app_name = "fireside"
    model_name = TaskSchedule._meta.model_name
    fields = {f for f in TaskSchedule._meta.get_fields() if f.editable}

    for f in fields:

        add_perm = TaskSchedule.get_permission_by_codename(f"add_{model_name}")
        view_field_perm = TaskSchedule.get_field_permission(f, "view")

        # test add & remove user object level permission
        logging_task_schedule.assign_perm(view_field_perm, adama)
        adama = get_object_or_404(User, pk=adama.id)  # refetch
        assert (
            adama.has_perm(
                f"{app_name}.view_{model_name}_{f.name}", logging_task_schedule
            )
            is True
        )
        assert logging_task_schedule.has_perm(view_field_perm, adama) is True
        assert (
            logging_task_schedule.has_perm(
                f"{app_name}.view_{model_name}_{f.name}", adama
            )
            is True
        )
        assert (
            starbuck.has_perm(
                f"{app_name}.view_{model_name}_{f.name}", logging_task_schedule
            )
            is False
        )

        logging_task_schedule.remove_perm(view_field_perm, adama)
        adama = get_object_or_404(User, pk=adama.id)  # refetch
        assert (
            adama.has_perm(
                f"{app_name}.view_{model_name}_{f.name}", logging_task_schedule
            )
            is False
        )
        assert logging_task_schedule.has_perm(view_field_perm, adama) is False
        assert (
            starbuck.has_perm(
                f"{app_name}.view_{model_name}_{f.name}", logging_task_schedule
            )
            is False
        )

        # test add & remove group object level permission
        assert (
            adama.has_perm(f"{app_name}.add_{model_name}", logging_task_schedule)
            is False
        )
        logging_task_schedule.assign_perm(add_perm, humans)
        humans.user_set.add(adama)
        adama = get_object_or_404(User, pk=adama.id)  # refetch
        assert (
            adama.has_perm(f"{app_name}.add_{model_name}", logging_task_schedule)
            is True
        )

        logging_task_schedule.remove_perm(add_perm, humans)
        adama = get_object_or_404(User, pk=adama.id)  # refetch
        assert (
            adama.has_perm(f"{app_name}.add_{model_name}", logging_task_schedule)
            is False
        )
