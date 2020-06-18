from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse
from webapp import views

from core.models import AdOfferProxy, AdRequestProxy, Ad, OffersByUserProxy, RequestByUserProxy, Conversation, Message


def webapp_index(request):
    template = loader.get_template('index.html')

    offers = OffersByUserProxy.objects.all().order_by('-created')[:5] or None
    requests = RequestByUserProxy.objects.all().order_by('-created')[:5] or None
    users = User.objects.annotate(count=Count('ad')).order_by('-count')[:5] or None
    context = {
        'offers_list': offers,
        'requests_list': requests,
        'users_list': users
    }

    return HttpResponse(template.render(context, request))

def webapp_register(request):
    context = {}
    template = loader.get_template('register.html')
    if request.method == 'POST':
        username = request.POST['username'] or None
        password = request.POST['password'] or None
        email = request.POST['email'] or None
        last_name = request.POST['last_name'] or None
        first_name = request.POST['first_name'] or None

        User(username=username, password=password, email=email, last_name=last_name, first_name=first_name).save()
    return HttpResponse(template.render(context, request))


def webapp_login(request):
    context = {}
    template = loader.get_template('login.html')
    if request.method == 'POST':
        username = request.POST['username'] or None
        password = request.POST['password'] or None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('webapp:webapp_profile'))
        else:
            context = {
                'error': 'utilisateur introuvable'
            }
    return HttpResponse(template.render(context, request))


def webapp_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('webapp:webapp_login'))


def webapp_profile(request):
    context = {}
    template = loader.get_template('profile.html')
    user = request.user or None
    if user is not None:
        offers = OffersByUserProxy.objects.filter(user=user).order_by('-created')[:5] or None
        requests = RequestByUserProxy.objects.filter(user=user).order_by('-created')[:5] or None

        if offers is not None and requests is not None:
            context.update({
                'user': user,
                'offers_list': offers,
                'requests_list': requests,

            })

    return HttpResponse(template.render(context, request))


def webapp_annonce(request, uuid):
    context = {}
    template = loader.get_template('annonce.html')
    ad = Ad.objects.get(pk=uuid)
    context.update({
        'ad': ad
    })
    try:
        conversation = Conversation.objects.get(ad=ad)
        messages = Message.objects.filter(conversation=conversation) or None
    except Conversation.DoesNotExist:
        conversation = None
    if conversation is not None and Message is not None:
        context.update({
            'ad': ad,
            'conversation': conversation,
            'messages': messages
        })
    return HttpResponse(template.render(context, request))


def webapp_annonces_offres(request):
    context = {}
    template = loader.get_template('annonces_offres.html')
    offers = AdOfferProxy.objects.all()
    context.update({
        'offers_list': offers
    })
    return HttpResponse(template.render(context, request))


def webapp_annonces_requests(request):
    context = {}
    template = loader.get_template('annonces_requests.html')
    requests = AdRequestProxy.objects.all()
    context.update({
        'requests_list': requests
    })
    return HttpResponse(template.render(context, request))


def webapp_annonces_offres_search(request):
    context = {}
    template = loader.get_template('annonces_offres.html')
    query = request.POST['q'] or None

    offers = AdOfferProxy.objects.all() or None
    if query is not None:
        offers = AdOfferProxy.objects.filter(
            title__icontains=str(query)
        ) or None
    if offers is not None:
        context.update({
            'offers_list': offers
        })
    return HttpResponse(template.render(context, request))


def webapp_annonces_requests_search(request):
    context = {}
    template = loader.get_template('annonces_requests.html')
    query = request.POST['q'] or None

    requests = AdRequestProxy.objects.all() or None
    if query is not None:
        requests = AdRequestProxy.objects.filter(
            title__icontains=str(query)
        ) or None
        if requests is not None:
            context.update({
                'requests_list': requests
            })
    return HttpResponse(template.render(context, request))


def webapp_conversation_start(request, uuid):
    template = loader.get_template('annonce.html')
    context = {}
    ad = Ad.objects.get(pk=uuid)

    try:
        conversation = Conversation.objects.get(ad=ad)
        try:
            messages = Message.objects.get(conversation=conversation)
        except Message.DoesNotExist:
            messages = None
            context.update({
                'ad': ad,
                'conversation': conversation
            })

    except Conversation.DoesNotExist:
        Conversation(ad=ad).save()
        conversation = Conversation.objects.get(ad=ad)

    if conversation is not None:
        context.update({
            'ad': ad,
            'conversation': conversation
        })

    return HttpResponse(template.render(context, request))


def webapp_new_message(request, uuid):
    template = loader.get_template('annonce.html')
    context = {}
    conversation = Conversation.objects.get(pk=uuid)
    query = request.POST['q'] or None
    if query is not None:
        Message(conversation=conversation, transmitter=request.user, receiver=request.user, content=query).save()
    messages = Message.objects.filter(conversation=conversation)

    ad = Ad.objects.get(conversation=conversation)

    context.update({
        'conversation': conversation,
        'messages': messages,
        'ad' : ad
    })

    return HttpResponse(template.render(context, request))
