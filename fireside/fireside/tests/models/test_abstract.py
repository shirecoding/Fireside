from datetime import timedelta

from django.utils import timezone

from fireside.models.task import TaskPriority, TaskSchedule


def test_activatable_model(logging_task_schedule):

    now = timezone.now()

    # test default is_active
    assert (
        logging_task_schedule.activate_on == logging_task_schedule.deactivate_on is None
    )
    assert logging_task_schedule.is_active is True

    # test deactivate
    logging_task_schedule.deactivate()
    assert logging_task_schedule.is_active is False

    # test activate
    logging_task_schedule.activate()
    assert (
        logging_task_schedule.activate_on == logging_task_schedule.deactivate_on is None
    )
    assert logging_task_schedule.is_active is True

    # test deactivate_on
    logging_task_schedule.deactivate_on = now - timedelta(seconds=60)
    logging_task_schedule.save()
    assert logging_task_schedule.is_active is False

    # test activate_on
    logging_task_schedule.activate()
    assert (
        logging_task_schedule.activate_on == logging_task_schedule.deactivate_on is None
    )
    logging_task_schedule.activate_on = now - timedelta(seconds=60)
    logging_task_schedule.save()
    assert logging_task_schedule.is_active is True

    # test deactivate_on & activate_on
    logging_task_schedule.activate()
    assert (
        logging_task_schedule.activate_on == logging_task_schedule.deactivate_on is None
    )
    logging_task_schedule.activate_on = now - timedelta(seconds=60)
    logging_task_schedule.deactivate_on = now + timedelta(seconds=60)
    logging_task_schedule.save()
    assert logging_task_schedule.is_active is True

    logging_task_schedule.activate_on = now + timedelta(seconds=60)
    logging_task_schedule.deactivate_on = now + timedelta(seconds=60)
    logging_task_schedule.save()
    assert logging_task_schedule.is_active is False

    logging_task_schedule.activate_on = now - timedelta(seconds=60)
    logging_task_schedule.deactivate_on = now - timedelta(seconds=60)
    logging_task_schedule.save()
    assert logging_task_schedule.is_active is False


def test_activatable_manager(db, logging_task_preset):

    now = timezone.now()

    ts1 = TaskSchedule.objects.create(
        task_preset=logging_task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )

    ts2 = TaskSchedule.objects.create(
        task_preset=logging_task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )

    ts3 = TaskSchedule.objects.create(
        task_preset=logging_task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )

    ts1.deactivate()

    # test activated
    assert ts1 not in TaskSchedule.objects.activated()
    assert ts2 in TaskSchedule.objects.activated()
    assert ts3 in TaskSchedule.objects.activated()

    # test deactivated
    assert ts1 in TaskSchedule.objects.deactivated()
    assert ts2 not in TaskSchedule.objects.deactivated()
    assert ts3 not in TaskSchedule.objects.deactivated()

    # test queryset deactivate
    TaskSchedule.objects.filter(uid=ts2.uid).deactivate()
    assert ts1 in TaskSchedule.objects.deactivated()
    assert ts2 in TaskSchedule.objects.deactivated()
    assert ts3 not in TaskSchedule.objects.deactivated()

    # test queryset activate
    TaskSchedule.objects.filter(uid=ts2.uid).activate()
    assert ts1 in TaskSchedule.objects.deactivated()
    assert ts2 not in TaskSchedule.objects.deactivated()
    assert ts3 not in TaskSchedule.objects.deactivated()

    ts1.activate()
    ts2.activate()
    ts3.activate()

    # test deactivate_on
    ts1.deactivate_on = now - timedelta(seconds=60)
    ts1.save()
    assert ts1 in TaskSchedule.objects.deactivated()
    assert ts1 not in TaskSchedule.objects.activated()

    # test activate_on
    ts1.activate()
    ts1.activate_on = now - timedelta(seconds=60)
    ts1.save()
    assert ts1 in TaskSchedule.objects.activated()
    assert ts1 not in TaskSchedule.objects.deactivated()

    # test deactivate_on & activate_on
    ts1.activate()
    ts1.activate_on = now - timedelta(seconds=60)
    ts1.deactivate_on = now + timedelta(seconds=60)
    ts1.save()
    assert ts1 in TaskSchedule.objects.activated()
    assert ts1 not in TaskSchedule.objects.deactivated()

    ts1.activate_on = now + timedelta(seconds=60)
    ts1.deactivate_on = now + timedelta(seconds=60)
    ts1.save()
    assert ts1 not in TaskSchedule.objects.activated()
    assert ts1 in TaskSchedule.objects.deactivated()

    ts1.activate_on = now - timedelta(seconds=60)
    ts1.deactivate_on = now - timedelta(seconds=60)
    ts1.save()
    assert ts1 not in TaskSchedule.objects.activated()
    assert ts1 in TaskSchedule.objects.deactivated()
