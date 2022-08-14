from fireside_tests.models import BasicShipModel
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command


def test_model(db):

    # test create
    bsg = BasicShipModel.objects.create(name="Battle Star Galactica")
    assert bsg.name == "Battle Star Galactica"
    assert bsg.type == "Basic"

    call_command("update_permissions")  # update with new field level permissions

    # test permissions
    bsg_perms = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(BasicShipModel)
    )

    assert any([p.codename == "change_basicshipmodel_name" for p in bsg_perms])
    assert any([p.codename == "view_basicshipmodel_name" for p in bsg_perms])
    assert any([p.codename == "change_basicshipmodel_type" for p in bsg_perms])
    assert any([p.codename == "view_basicshipmodel_type" for p in bsg_perms])
