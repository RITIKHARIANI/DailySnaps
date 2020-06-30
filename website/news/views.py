from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from django.urls import reverse
from .models import News,Saved_Articles
from newsapi import NewsApiClient
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .forms import SignUpForm
from .tokens import account_activation_token
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import stringfilter
from django.contrib.auth.decorators import login_required

newsapi = NewsApiClient(api_key='API_KEY')

source_info = {'':'','ABC News': 'abc-news', 'ABC News (AU)': 'abc-news-au', 'Aftenposten': 'aftenposten', 'Al Jazeera English': 'al-jazeera-english', 'ANSA.it': 'ansa', 'Argaam': 'argaam', 'Ars Technica': 'ars-technica', 'Ary News': 'ary-news', 'Associated Press': 'associated-press', 'Australian Financial Review': 'australian-financial-review', 'Axios': 'axios', 'BBC News': 'bbc-news', 'BBC Sport': 'bbc-sport', 'Bild': 'bild', 'Blasting News (BR)': 'blasting-news-br', 'Bleacher Report': 'bleacher-report', 'Bloomberg': 'bloomberg', 'Breitbart News': 'breitbart-news', 'Business Insider': 'business-insider', 'Business Insider (UK)': 'business-insider-uk', 'Buzzfeed': 'buzzfeed', 'CBC News': 'cbc-news', 'CBS News': 'cbs-news', 'CNBC': 'cnbc', 'CNN': 'cnn', 'CNN Spanish': 'cnn-es', 'Crypto Coins News': 'crypto-coins-news', 'Der Tagesspiegel': 'der-tagesspiegel', 'Die Zeit': 'die-zeit', 'El Mundo': 'el-mundo', 'Engadget': 'engadget', 'Entertainment Weekly': 'entertainment-weekly', 'ESPN': 'espn', 'ESPN Cric Info': 'espn-cric-info', 'Financial Post': 'financial-post', 'Focus': 'focus', 'Football Italia': 'football-italia', 'Fortune': 'fortune', 'FourFourTwo': 'four-four-two', 'Fox News': 'fox-news', 'Fox Sports': 'fox-sports', 'Globo': 'globo', 'Google News': 'google-news', 'Google News (Argentina)': 'google-news-ar', 'Google News (Australia)': 'google-news-au', 'Google News (Brasil)': 'google-news-br', 'Google News (Canada)': 'google-news-ca', 'Google News (France)': 'google-news-fr', 'Google News (India)': 'google-news-in', 'Google News (Israel)': 'google-news-is', 'Google News (Italy)': 'google-news-it', 'Google News (Russia)': 'google-news-ru', 'Google News (Saudi Arabia)': 'google-news-sa', 'Google News (UK)': 'google-news-uk', 'Göteborgs-Posten': 'goteborgs-posten', 'Gruenderszene': 'gruenderszene', 'Hacker News': 'hacker-news', 'Handelsblatt': 'handelsblatt', 'IGN': 'ign', 'Il Sole 24 Ore': 'il-sole-24-ore', 'Independent': 'independent', 'Infobae': 'infobae', 'InfoMoney': 'info-money', 'La Gaceta': 'la-gaceta', 'La Nacion': 'la-nacion', 'La Repubblica': 'la-repubblica', 'Le Monde': 'le-monde', 'Lenta': 'lenta', "L'equipe": 'lequipe', 'Les Echos': 'les-echos', 'Libération': 'liberation', 'Marca': 'marca', 'Mashable': 'mashable', 'Medical News Today': 'medical-news-today', 'MSNBC': 'msnbc', 'MTV News': 'mtv-news', 'MTV News (UK)': 'mtv-news-uk', 'National Geographic': 'national-geographic', 'National Review': 'national-review', 'NBC News': 'nbc-news', 'News24': 'news24', 'New Scientist': 'new-scientist', 'News.com.au': 'news-com-au', 'Newsweek': 'newsweek', 'New York Magazine': 'new-york-magazine', 'Next Big Future': 'next-big-future', 'NFL News': 'nfl-news', 'NHL News': 'nhl-news', 'NRK': 'nrk', 'Politico': 'politico', 'Polygon': 'polygon', 'RBC': 'rbc', 'Recode': 'recode', 'Reddit /r/all': 'reddit-r-all', 'Reuters': 'reuters', 'RT': 'rt', 'RTE': 'rte', 'RTL Nieuws': 'rtl-nieuws', 'SABQ': 'sabq', 'Spiegel Online': 'spiegel-online', 'Svenska Dagbladet': 'svenska-dagbladet', 'T3n': 't3n', 'TalkSport': 'talksport', 'TechCrunch': 'techcrunch', 'TechCrunch (CN)': 'techcrunch-cn', 'TechRadar': 'techradar', 'The American Conservative': 'the-american-conservative', 'The Globe And Mail': 'the-globe-and-mail', 'The Hill': 'the-hill', 'The Hindu': 'the-hindu', 'The Huffington Post': 'the-huffington-post', 'The Irish Times': 'the-irish-times', 'The Jerusalem Post': 'the-jerusalem-post', 'The Lad Bible': 'the-lad-bible', 'The Next Web': 'the-next-web', 'The Sport Bible': 'the-sport-bible', 'The Times of India': 'the-times-of-india', 'The Verge': 'the-verge', 'The Wall Street Journal': 'the-wall-street-journal', 'The Washington Post': 'the-washington-post', 'The Washington Times': 'the-washington-times', 'Time': 'time', 'USA Today': 'usa-today', 'Vice News': 'vice-news', 'Wired': 'wired', 'Wired.de': 'wired-de', 'Wirtschafts Woche': 'wirtschafts-woche', 'Xinhua Net': 'xinhua-net', 'Ynet': 'ynet'}


def home_page(request):
    data = newsapi.get_top_headlines(country='in',page_size=5)
    context = {'carousel':[],'source':[],'author':[],'title':[],'description':[],'url':[],'image':[],'published':[],'content':[],'totalResults':[]}
    pos = 0
    for i in data['articles']:
        context['carousel'].append(1)
        context['source'].append(i['source']['name'])
        context['author'].append(i['author'])
        context['title'].append(i['title'])
        context['description'].append(i['description'])
        context['url'].append(i['url'])
        context['image'].append(i['urlToImage'])
        context['published'].append(i['publishedAt'])
        context['content'].append(i['content'])
        context['totalResults'].append(pos)
        pos+=1
    context_data = newsapi.get_everything(q="coronavirus",language='en',sort_by='popularity',page_size=5)
    for i in context_data['articles']:
        context['carousel'].append(0)
        context['source'].append(i['source']['name'])
        context['author'].append(i['author'])
        context['title'].append(i['title'])
        context['description'].append(i['description'])
        context['url'].append(i['url'])
        context['image'].append(i['urlToImage'])
        context['published'].append(i['publishedAt'])
        context['content'].append(i['content'])
        context['totalResults'].append(pos)
        pos+=1
    context_entertainment = newsapi.get_everything(q="hollywood",sort_by='popularity',language='en',page_size=2)
    for i in context_entertainment['articles']:
        context['carousel'].append(2)
        context['source'].append(i['source']['name'])
        context['author'].append(i['author'])
        context['title'].append(i['title'])
        context['description'].append(i['description'])
        context['url'].append(i['url'])
        context['image'].append(i['urlToImage'])
        context['published'].append(i['publishedAt'])
        context['content'].append(i['content'])
        context['totalResults'].append(pos)
        pos+=1
    context_entertainment = newsapi.get_everything(q="bollywood",language='en',sort_by='popularity',page_size=5)
    for i in context_entertainment['articles']:
        context['carousel'].append(3)
        context['source'].append(i['source']['name'])
        context['author'].append(i['author'])
        context['title'].append(i['title'])
        context['description'].append(i['description'])
        context['url'].append(i['url'])
        context['image'].append(i['urlToImage'])
        context['published'].append(i['publishedAt'])
        context['content'].append(i['content'])
        context['totalResults'].append(pos)
        pos+=1
    return render(request, "news/index.html", context )

class LoginView(View): #there is a default login class also in django, we made this in class to simulate that
	def get(self,request):
		return render(request,"news/login.html",{"form":AuthenticationForm()})
	def post(self,request):
		form=AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = authenticate(request,username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password'))
			if user is None:
				return redirect(request,"news/login.html",{"form":form,"invalid_creds":True})
			auth.login(request, user)
			return redirect('home_page')
	
		else:
			return render(request,"news/login.html",{"form":form,"invalid_creds":True})

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('news/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'news/signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('home_page')

def activation_sent_view(request):
    return render(request, 'news/activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home_page')
    else:
        return render(request, 'news/activation_invalid.html')

def is_valid_queryparam(param):
    return param != '' and param is not None

def filter(request):
    data = newsapi.get_top_headlines(country='in',page_size=100)
    title_or_category = request.GET.get('title_or_category')
    source = request.GET.get('source')
    if is_valid_queryparam(title_or_category):
        data = newsapi.get_everything(q=title_or_category,page_size = 100,language='en')


    if is_valid_queryparam(source) and '-' not in source:
        if source not in source_info.values():
            final_source = source_info[source]
        else:
            final_source = source
        data = newsapi.get_everything(q=title_or_category,sources = final_source, page_size = 100,language='en')

    elif is_valid_queryparam(source) and '-' in source:
        country = source.split('-')[1]
        data = newsapi.get_top_headlines(q=title_or_category,country = country, page_size = 100)

    return data

@login_required(login_url='/login')
@csrf_exempt
def filter_news(request):
    if request.method=="POST":
        news = request.POST['news']
        #print(news)
        data = news.split('@#$')
        user_data = Saved_Articles.objects.get(user = request.user)
        #user_data.user = request.user
        if str(data[7]) not in user_data.url.split('@#$'):
            user_data.source += str(data[0]) + '@#$'
            user_data.author += str(data[1]) + '@#$'
            user_data.description += str(data[2]) + '@#$'
            user_data.title += str(data[3]) + '@#$'
            user_data.content += str(data[4]) + '@#$'
            user_data.published += str(data[5]) + '@#$'
            user_data.image += str(data[6]) + '@#$'
            user_data.url += str(data[7]) + '@#$'
            user_data.save()
        global context
        context['saved'] = user_data.url.split('@#$')
        return render(request, "news/filter_news.html", context)
    else:
        user_data = Saved_Articles.objects.get(user = request.user)
        final_data = filter(request)
        context = {'source':[],'author':[],'title':[],'description':[],'url':[],'image':[],'published':[],'content':[],'totalResults':[]}
        pos = 0
        for i in final_data['articles']:
            context['source'].append(i['source']['name'])
            context['author'].append(i['author'])
            context['title'].append(i['title'])
            context['description'].append(i['description'])
            context['url'].append(i['url'])
            context['image'].append(i['urlToImage'])
            context['published'].append(i['publishedAt'])
            context['content'].append(i['content'])
            context['totalResults'].append(pos)
            pos+=1
        context['saved'] = user_data.url.split('@#$')
        return render(request, "news/filter_news.html", context)

@login_required(login_url='/login')
def saved_news(request):
    display = {'source':[],'author':[],'title':[],'description':[],'url':[],'image':[],'published':[],'content':[],'totalResults':[]}
    user_data = Saved_Articles.objects.get(user = request.user)
    display['source'] = user_data.source.split('@#$')
    display['author'] = user_data.author.split('@#$')
    display['description'] = user_data.description.split('@#$')
    display['title'] = user_data.title.split('@#$')
    display['content'] = user_data.content.split('@#$')
    display['published'] = user_data.published.split('@#$')
    display['image'] = user_data.image.split('@#$')
    display['url'] = user_data.url.split('@#$')
    display['totalResults'] = [i for i in range(len(display['source'])-1)]
    return render(request, "news/saved_news.html", display)

import random
@csrf_exempt
@login_required(login_url='/login')
def preferences(request):
    user_data = Saved_Articles.objects.get(user = request.user)
    if request.method=="POST":
        pref = request.POST['pref']
        user_data.preference = pref
        user_data.save()
    pref = user_data.preference
    if pref=='':
        return render(request, "news/preferences.html", {})
    category = pref.split('+')[:len(pref.split('+'))-1]
    total =[i for i in range(len(pref.split('+'))-1)]
    context1 = {'source':[],'author':[],'title':[],'description':[],'url':[],'image':[],'published':[],'content':[],'total':total,'category':category,'specific':[],'totalResults':[]}
    pref_data = {}
    for i in range(len(total)):
        if i!=0:
            pref_data['articles']+=(newsapi.get_top_headlines(country='in',category=category[i],page_size=20,language='en')['articles'])
        else:
            pref_data['articles'] = newsapi.get_top_headlines(country='in',category=category[i],page_size=20,language='en')['articles']
        for j in pref_data['articles'][20*i:]:
            j['specific'] = category[i]
    pos = 0 
    for i in pref_data['articles']:
            context1['source'].append(i['source']['name'])
            context1['author'].append(i['author'])
            context1['title'].append(i['title'])
            context1['description'].append(i['description'])
            context1['url'].append(i['url'])
            context1['image'].append(i['urlToImage'])
            context1['published'].append(i['publishedAt'])
            context1['content'].append(i['content'])
            context1['specific'].append(i['specific'])
            context1['totalResults'].append(pos)
            pos+=1
    mix = list(zip(context1['source'],context1['author'],context1['title'],context1['description'],context1['url'],context1['image'],context1['published'],context1['content'],context1['specific']))
    random.shuffle(mix)
    context1['source'],context1['author'],context1['title'],context1['description'],context1['url'],context1['image'],context1['published'],context1['content'],context1['specific'] = zip(*mix)
    return render(request, "news/preferences.html", context1)

@register.filter
def index_value(List,pos):
    return List[pos]

@register.filter
@stringfilter
def value(data):
    return data

@register.filter
def carousel_content(value):
    if value == 1:
        return 1
    else:
        return 0

@register.filter
def content(value):
    if value == 0 or value == 3:
        return 1
    else:
        return 0

@register.filter
def card_content(value):
    if value == 2:
        return 1
    else:
        return 0
