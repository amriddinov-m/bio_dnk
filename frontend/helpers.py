from django.urls import reverse

from frontend.models import Chain


def change_chain(post_request):
    title = post_request.get('title', '-')
    Chain.objects.update(title=title)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'home')),
         'title': title})


def check_codon_in_chain(post_request):
    codon = post_request.get('codon', None)
    chain = Chain.objects.filter(title__icontains=codon)
    print(chain)
    return dict(
        {'back_url': reverse(post_request.get('back_url', 'home')),
         'chain': True if chain else False})
