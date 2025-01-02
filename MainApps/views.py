import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password

from siwarkah.models import User
from siwarkah.views import items, say

def index(request):
    print ('+++++++++++ INDEX ++++++++++++++++')
    return render(request, 'mainapp/index.html', items())


def daftar(request):
    if request.method == 'POST':
        form = request.POST
        username = form['username']
        departemen = form['departemen']
        bidang = form['bidang']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            password = make_password(form['password'], salt=None, hasher='default')
            data = User(username=username, departemen=departemen, bidang=bidang, password=password)
            data.save()
            messages.success(request, 'Username '+username+' berhasil dibuat, silahkan login.')
            return redirect('/login')
        if user:
            messages.error(request, 'Username '+username+' sudah digunakan, ganti nama lain.')
            return redirect('/daftar')
    return render(request, 'mainapp/sign-up.html')


def login(request):
    session = request.session
    if request.method == 'POST':
        form = request.POST
        username = form['username']
        try:
            user = User.objects.values_list('password', 'username', 'departemen', 'bidang', 'id', named=True).get(username=username)
            password = check_password(form['password'], str(user[0]))
        except User.DoesNotExist:
            messages.error(request, 'Maaf username '+username+' belum terdaftar.')
            return redirect('/login')

        if password == True:
            session['user'] = user[1]
            session['dept'] = user[2]
            session['bid'] = user[3] or '-'
            session['uid'] = user[4]
            print ('*********** LOGIN SUCCESS ***********')
            messages.success(request, 'Hallo selamat '+say(request)+', '+session['user']+'.')
            return redirect('/')
        else:
            messages.warning(request, 'Maaf username atau password yang anda masukkan salah.')
            return redirect('/login')
    return render(request, 'mainapp/log-in.html')


def akun(request):
    session = request.session
    user = User.objects.get(id=session['uid'])
    if request.method == 'POST':
        form = request.POST
        check_pass = check_password(form['pass'], str(user.password))

        try:
            check_user = User.objects.get(username=form['username'])
        except User.DoesNotExist:
            if check_pass == True:
                user.username       = form['username']
                user.departemen     = form['departemen']
                user.bidang         = form['bidang']
                user.update_date    = datetime.datetime.today()
                user.save()

                session['user'] = form['username']
                session['dept'] = form['departemen']
                session['bid'] = form['bidang'] or '-'
                messages.success(request, 'Selamat username '+form['username']+' berhasil diupdate.')
                return redirect('/akun')
            else:
                messages.error(request, 'Maaf username '+form['username']+' gagal diupdate, cek lagi password.')
                return redirect('/akun')

        if check_user.username == form['username'] and check_user.id != session['uid']:
            messages.warning(request, 'Maaf username '+form['username']+' sudah terpakai, ganti yang lain.')
            return redirect('/akun')
        elif check_pass == True:
            user.username       = form['username']
            user.departemen     = form['departemen']
            user.bidang         = form['bidang']
            user.update_date    = datetime.datetime.today()
            user.save()

            session['user'] = form['username']
            session['dept'] = form['departemen']
            session['bid'] = form['bidang'] or '-'
            messages.success(request, 'Selamat username '+form['username']+' berhasil diupdate.')
            return redirect('/akun')
        else:
            messages.error(request, 'Maaf username '+form['username']+' gagal diupdate, cek lagi password.')
            return redirect('/akun')
    return render(request, 'mainapp/profile.html', items())


def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    print ('*********** LOGOUT SUCCESS ***********')
    return redirect('/')