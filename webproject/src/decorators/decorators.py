from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy

def group_required(group_names):
    """Checks for user membership in at least one of the groups passed in."""
    def in_groups(u):
        group = []
        if u.is_authenticated:
            group += u.groups.all().values_list('name', flat=True)

            if len(group) > 0 and group[0] in group_names or u.is_superuser:
                return user_passes_test(in_groups)
        else:
            return False
    return user_passes_test(in_groups, login_url=reverse_lazy('home'))
