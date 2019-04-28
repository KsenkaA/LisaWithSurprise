from django.template.defaultfilters import register


@register.filter(name='lookup')
def lookup(arr, index):
    return arr[index]

@register.filter(name='dv')
def lookup(arr, index):
    return (arr/index)*100