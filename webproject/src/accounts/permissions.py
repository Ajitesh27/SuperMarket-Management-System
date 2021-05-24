from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def assign_permissions(role, perm_list, full=False):
    all_perms = []

    if not role and not perm_list:
        raise ValueError("Role and permission can't be empty")
    else:
        if full:
            content_type = ContentType.objects.get(model = 'user')
            all_perms += Permission.objects.filter(content_type = content_type).values_list('codename', flat=True)

            for perm in all_perms:
                role.permissions.add(Permission.objects.get(codename=perm))
                role.save()
        else:
            if len(perm_list) > 1:
                for perm in perm_list:
                    role.permissions.add(Permission.objects.get(codename=perm))
                    role.save()
            else:
                role.permissions.add(Permission.objects.get(codename=perm_list[0]))
                role.save()

def remove_permissions(role, new_perm, old_perms):
    for perm in old_perms:
        if perm not in new_perm:
            role.permissions.remove(Permission.objects.get(codename=perm))
