from datetime import timedelta

from django.utils import timezone

from fireside.models import TaskPriority, TaskSchedule


def test_activatable_model(task_schedule):

    now = timezone.now()

    # test default is_active
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    assert task_schedule.is_active == True

    # test deactivate
    task_schedule.deactivate()
    assert task_schedule.is_active == False

    # test activate
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    assert task_schedule.is_active == True

    # test deactivate_on
    task_schedule.deactivate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False

    # test activate_on
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == True

    # test deactivate_on & activate_on
    task_schedule.activate()
    assert task_schedule.activate_on == task_schedule.deactivate_on == None
    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.deactivate_on = now + timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == True

    task_schedule.activate_on = now + timedelta(seconds=60)
    task_schedule.deactivate_on = now + timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False

    task_schedule.activate_on = now - timedelta(seconds=60)
    task_schedule.deactivate_on = now - timedelta(seconds=60)
    task_schedule.save()
    assert task_schedule.is_active == False


def test_activatable_manager(db, task_preset):

    now = timezone.now()

    ts1 = TaskSchedule.objects.create(
        task_preset=task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )

    ts2 = TaskSchedule.objects.create(
        task_preset=task_preset,
        cron="* * * * *",
        repeat=2,
        priority=TaskPriority.LOW,
    )

    ts3 = TaskSchedule.objects.create(
        task_preset=task_preset,
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
