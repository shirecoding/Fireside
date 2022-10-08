from fireside_tests.models import BasicShipModel
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
import pytest
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404


@pytest.fixture
def bsg(db) -> BasicShipModel:

    # test create
    obj = BasicShipModel.objects.create(name="Battle Star Galactica")
    assert BasicShipModel.objects.filter(name="Battle Star Galactica").exists()
    assert obj.name == "Battle Star Galactica"
    assert obj.type == "Basic"

    # update with new field level permissions
    call_command("update_permissions")
    call_command("remove_stale_contenttypes")

    return obj


@pytest.fixture
def discovery(db) -> BasicShipModel:

    # test create
    obj = BasicShipModel.objects.create(name="Discovery")
    assert BasicShipModel.objects.filter(name="Discovery").exists()
    assert obj.name == "Discovery"
    assert obj.type == "Basic"

    # update with new field level permissions
    call_command("update_permissions")
    call_command("remove_stale_contenttypes")

    return obj


@pytest.fixture
def starbuck(db) -> User:
    return User.objects.create(username="starbuck")


@pytest.fixture
def adama(db) -> User:
    return User.objects.create(username="adama")


@pytest.fixture
def humans(db) -> Group:
    return Group.objects.create(name="humans")


def test_model(bsg):

    # test permissions
    bsg_perms = Permission.objects.filter(
        content_type=ContentType.objects.get_for_model(BasicShipModel)
    )

    assert any([p.codename == "write_basicshipmodel_name" for p in bsg_perms])
    assert any([p.codename == "read_basicshipmodel_name" for p in bsg_perms])
    assert any([p.codename == "write_basicshipmodel_type" for p in bsg_perms])
    assert any([p.codename == "read_basicshipmodel_type" for p in bsg_perms])


def test_field_permissions(bsg, humans, starbuck):

    # no perms to start
    assert bool(starbuck.get_all_permissions()) == False

    # test get permissions
    write_basicshipmodel_name = BasicShipModel.get_permission_by_codename(
        "write_basicshipmodel_name"
    )
    assert (
        BasicShipModel.get_field_permission(BasicShipModel.name, "write")
        == write_basicshipmodel_name
    )
    assert (
        BasicShipModel.get_field_permission(BasicShipModel.name.field, "write")
        == write_basicshipmodel_name
    )

    # test add & remove user perm
    assert starbuck.has_perm("fireside_tests.write_basicshipmodel_name") == False
    starbuck.user_permissions.add(write_basicshipmodel_name)
    starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
    assert starbuck.has_perm("fireside_tests.write_basicshipmodel_name") == True

    starbuck.user_permissions.remove(write_basicshipmodel_name)
    starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
    assert starbuck.has_perm("fireside_tests.write_basicshipmodel_name") == False

    # test add & remove group perm
    humans.permissions.add(write_basicshipmodel_name)
    humans.user_set.add(starbuck)
    starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
    assert starbuck.has_perm("fireside_tests.write_basicshipmodel_name") == True

    humans.permissions.remove(write_basicshipmodel_name)
    starbuck = get_object_or_404(User, pk=starbuck.id)  # refetch
    assert starbuck.has_perm("fireside_tests.write_basicshipmodel_name") == False


def test_object_permissions(bsg, discovery, humans, starbuck, adama):

    add_basicshipmodel = BasicShipModel.get_permission_by_codename("add_basicshipmodel")
    read_basicshipmodel_name = BasicShipModel.get_field_permission(
        BasicShipModel.name, "read"
    )

    # test add & remove user object level permission
    discovery.assign_perm(read_basicshipmodel_name, adama)
    adama = get_object_or_404(User, pk=adama.id)  # refetch
    assert adama.has_perm("fireside_tests.read_basicshipmodel_name", discovery) == True
    assert discovery.has_perm(read_basicshipmodel_name, adama) == True
    assert discovery.has_perm("fireside_tests.read_basicshipmodel_name", adama) == True

    assert (
        starbuck.has_perm("fireside_tests.read_basicshipmodel_name", discovery) == False
    )

    discovery.remove_perm(read_basicshipmodel_name, adama)
    adama = get_object_or_404(User, pk=adama.id)  # refetch
    assert adama.has_perm("fireside_tests.read_basicshipmodel_name", discovery) == False
    assert discovery.has_perm(read_basicshipmodel_name, adama) == False
    assert (
        starbuck.has_perm("fireside_tests.read_basicshipmodel_name", discovery) == False
    )

    # test add & remove group object level permission
    assert adama.has_perm("fireside_tests.add_basicshipmodel", discovery) == False
    discovery.assign_perm(add_basicshipmodel, humans)
    humans.user_set.add(adama)
    adama = get_object_or_404(User, pk=adama.id)  # refetch
    assert adama.has_perm("fireside_tests.add_basicshipmodel", discovery) == True

    discovery.remove_perm(add_basicshipmodel, humans)
    adama = get_object_or_404(User, pk=adama.id)  # refetch
    assert adama.has_perm("fireside_tests.add_basicshipmodel", discovery) == False
