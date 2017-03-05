from django.shortcuts import render
from market.models import Category,Goods,UserProfile,Comment,InstationMessage,User
from market.forms import UserForm,UserProfieldForm,GoodsForm,CommentForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from PIL import Image

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        message_unread = InstationMessage.objects.filter(receiver=user_profile, active=True).count()
    else:
        user_profile = []
        message_unread = 0
    category_list = Category.objects.all()
    goods_list = Goods.objects.all().order_by('-publish_time')
    context_dic = {'categories':category_list,'user_profile':user_profile,'goodses':goods_list,'message_unread':message_unread}
    return render(request, 'market/index.html',context_dic)


def category(request,category_id):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
    else:
        user_profile = []
    page_list = []
    try:
        category = Category.objects.get(pk=category_id)
        name = category.name
        if request.GET.get('rank'):
            rank = request.GET.get('rank')
            goodses_list = Goods.objects.filter(category=category).order_by('-'+rank)
        else:
            goodses_list = Goods.objects.filter(category=category)
        # 实现分页功能
        paginator = Paginator(goodses_list, 12)
        page = request.GET.get('page')
        goodses = paginator.page(page)
    except Category.DoesNotExist:
        pass
    except PageNotAnInteger:
        goodses = paginator.page(1)
    except EmptyPage:
        goodses = paginator.page(paginator.num_pages)

    for i in range(1,6):
        order = (int)((goodses.number-1) / 5)
        page_list.append(order*5+i)

    context_dic={'category':category,'category_name':name,'goodses':goodses,'page_list':page_list,'user_profile':user_profile}

    return render(request, 'market/category.html',context_dic)


def goods_page(request,goods_id):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
    else:
        user_profile = []
    comment_form = CommentForm()
    goods = Goods.objects.get(pk=goods_id)
    comment_list = Comment.objects.filter(goods=goods)
    context_dic = {'goods':goods,'comments':comment_list,'form':comment_form,'user_profile':user_profile}
    return render(request, 'market/goods.html',context_dic)


@login_required
def add_comment(request,goods_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=True)
            goods = Goods.objects.get(pk=goods_id)
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            comment.user = user_profile
            comment.goods = goods
            comment.save()
            message = InstationMessage()
            message.sender = user_profile
            message.receiver = goods.seller
            message.content = comment.content
            message.save()

            return goods_page(request,goods_id)
        else:
            print(comment_form.errors)
    else:
        comment_form =CommentForm()
    return render(request, 'market/add_comment.html')


@login_required
def add_goods(request):
    if request.method == 'POST':
        goods_form = GoodsForm(request.POST)
        if goods_form.is_valid():
            goods = goods_form.save(commit=True)
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            goods.seller = user_profile
            if 'picture' in request.FILES:
                goods.picture = request.FILES['picture']
            print(goods.picture)
            goods.save()
            return index(request)
        else:
            print(goods_form.errors)
    else:
        goods_form = GoodsForm()

    return render(request, 'market/add_goods.html',{'form':goods_form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfieldForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'avatar' in request.FILES:
                profile.avatar = request.FILES['avatar']
            profile.save()
            registered = True

            return user_login(request)
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfieldForm()
    return render(request, 'market/register.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/market/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invid login details:{0},{1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'market/login.html',{})


@login_required
def about(request):
    return HttpResponse("This is about page.")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/market/')


def profile(request,user_id):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
    else:
        user_profile = []
    user = User.objects.get(pk=user_id)
    user = UserProfile.objects.get(user=user)
    goodses = Goods.objects.filter(seller=user)
    context_dic = {'profile':user,'user_profile':user_profile,'goodses':goodses}
    return render(request, 'market/profile.html',context_dic)


def search(request):
    if request.user.is_authenticated:
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
    else:
        user_profile = []
        key_word = request.GET.get('keyword')
        category_list = Category.objects.all()
        goods_list = Goods.objects.filter(name__icontains=key_word)
        context_dic = {'categories':category_list,'user_profile':user_profile,'goodses':goods_list}
        return render(request, 'market/index.html',context_dic)

@login_required
def display_message(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    messages = InstationMessage.objects.filter(receiver=user_profile).order_by('-send_time')
    for mes in messages:
        mes.active = False
        mes.save()
    context_dic = { 'user_profile': user_profile, 'messages':  messages}
    return render(request, 'market/message.html', context_dic)

