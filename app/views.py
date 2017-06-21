# -*- coding: utf-8 -*-

import datetime

from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

from app.models import Users,Salary_type,Salary,People,Yewu,Card
import time
import csv
import sys
import codecs
global userid
reload(sys)
sys.setdefaultencoding('utf8')
from django.shortcuts import render_to_response
##
def main(request):
    global userid
    return render_to_response('main.html',{'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})

##登陆
def login(request):
    # 首先判断页面的请求方式
    #如果是POST就表明有表单内容要提交
    global userid
    if request.method=='POST':
        #输入的获取用户名
        userid=request.POST['userid'].strip()
        #如果用户名能在数据库里找到
        if not Users.objects.filter(userid=userid) :
            return render_to_response('login_error.html',{'error_info': '用户不存在'})
        if People.objects.filter(peopleid=userid):
            #有用户再验证密码
            passwd=request.POST['password'].strip()
            db_passwd=Users.objects.filter(userid=userid).values()[0]['password']
            name=People.objects.filter(peopleid=userid).values()[0]['name'].encode('utf-8')
            #如果用户输入的密码和存储的密码相等
            if passwd==db_passwd:
                #页面跳转
                return render_to_response("main.html",{'info':name,'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid) })
            else:
                #如果密码验证失败，在页面底部显示错误提示
                return render_to_response('login_error.html',{'error_info': '密码错误'})

        #如果没有找到这个用户，就在页面上提示没有这个用户
        else:
            #这个return的返回值会直接返回ajax可以的success:function()
            return render_to_response('login_error.html',{'error_info': '用户不存在'})
    return render_to_response('login.html')
def register(request):
    global userid
    if "userid" in request.GET:
        userid=request.GET["userid"]
        password1 = request.GET["password"]
        passwordco = request.GET["password1"]
        p=People.objects.filter(peopleid = userid)
        if p:
            if(password1==passwordco):
                user = Users(
                    userid = request.GET["userid"],
                    password = request.GET["password"]
                )
                user.save()
                return HttpResponseRedirect("/login/")
        else:return render_to_response("login_error.html",{'error_info': '注册失败'})
    return render_to_response("register.html")
def chang_ps(request):
    global userid
    if request.GET:
        userid1=userid
        password1 = request.GET["password"]
        passwordco = request.GET["password1"]
        p=Users.objects.get(userid = userid1)
        if(password1==passwordco and password1 != ''):
            p.password=password1
            p.save()
            return HttpResponseRedirect("/login/")
        else:return render_to_response("chang_ps.html",{'info':'修改失败!'})
    else:return render_to_response("chang_ps.html")
def login_error(request):
    global userid
    return render_to_response("login_error.html")
def logout(request):
    global userid
    auth.logout(request)
    return HttpResponseRedirect("/login/")
#工资及签到
def qiandao(request):
    global userid
    # 首先判断页面的请求方式
    #如果是POST就表明有表单内容要提交

    #输入的获取用户名
    start=int(time.strftime("%H"))
    date=time.strftime("%Y-%m-%d")
    #如果用户名能在数据库里找到
    if Card.objects.filter(date=date) and Card.objects.filter(cardid_id=userid):
        return render_to_response('main.html',{'info': '已经签到过了','users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})
    else:
        new_card=Card(
            cardid_id = userid,
            start = start,
            over = 0,
            date = date
        )
        p=People.objects.get(peopleid=userid)
        str1='签退中'
        if p.ptype_id == 1 and start > 9:
            p.allsalary-=50
            str1="迟到了，扣了50元"
        new_card.save()
        return render_to_response('qiantui.html',{'info':str1})
        #这个return的返回值会直接返回ajax可以的success:function()

def qiantui(request):
    global userid
    # 首先判断页面的请求方式
    #如果是POST就表明有表单内容要提交
    over=int(time.strftime("%H"))
    date=time.strftime("%Y-%m-%d")
    if Card.objects.filter(date=date) and Card.objects.filter(cardid_id=userid):
        card=Card.objects.get(cardid_id=userid,date=date)
        card.over=over
        card.hours=card.over-card.start
        hours=card.hours
        card.save()
        p=People.objects.get(peopleid=userid)
        q=Salary_type.objects.get(salary_typeid=p.ptype_id)
        m=Salary.objects.get(salaryid_id=userid)
        if p.ptype_id==1 :
            if hours > 8:
                p.allsalary+=(hours-8)*50
            if over < 18:
                p.allsalary-=50
                m.forfeit+=50
        if p.ptype_id==2 :
            p.allsalary+=hours*q.hour_pay
        m.hour+=hours
        m.sub=p.allsalary
        m.save()
        p.save()
        str1="打卡完成！工作了"+str(hours)+"小时,加油哦！争了"+str(p.allsalary)+"元"
        return render_to_response('main.html',{'info':str1,'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})
            #这个return的返回值会直接返回ajax可以的success:function()

def daka(request):
    global userid

    #card=card.filter(date=datetime.datetime.now()).values()[0]
    if Card.objects.filter(cardid_id=userid,date=datetime.datetime.now()) :
        card=Card.objects.get(cardid_id=userid,date=datetime.datetime.now())
        if card.hours == 0:
            return render_to_response('qiantui.html')
        else:
            return render_to_response('main.html',{'info':"今天您已经打卡过了！",'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})

    return render_to_response('qiandao.html',{'info':"打卡中！"})

def permiss_yewu(request):
    global userid
    yewu_list = Yewu.objects.all()
    if request.GET:
        id=request.GET["id"]
        ispermiss=request.GET["is"]
        if Yewu.objects.get(yewuid=id):
            yewu=Yewu.objects.get(yewuid=id)
            yewu.isover=1
            if ispermiss:
                yewu.ispermiss=1
                people=People.objects.get(peopleid=yewu.yewupeopleid_id)
                if people.ptype_id == 3:
                    salarytype=Salary_type.objects.get(salary_typeid=people.ptype_id)
                    people.allsalary+=salarytype.plus_pay
                    m=Salary.objects.get(salaryid_id=people.peopleid)
                    m.plus+=salarytype.plus_pay
                    m.sub=people.allsalary
                    m.save()
                people.save()
            yewu.save()
    return render_to_response("permiss_yewu.html",{"yewu_list":yewu_list})

def pay(request):
    global userid
    salary_list = Salary.objects.all()
    people_list =People.objects.all()
    for salary in salary_list:

        p=People.objects.get(peopleid=salary.salaryid_id)
        salary.sub = p.allsalary
        salary.save()
    if 'search_salary' in request.POST:
        salary=Salary.objects.get(salaryid_id=request.POST['search_salary'])
        people=People.objects.get(peopleid=salary.salaryid_id)
        return render_to_response('show_salary.html',{"salary":salary,"people":people})
    return render_to_response("pay.html", {"salary_list":salary_list,"people_list":people_list})

def print_pay(request):
    if request.GET:

        salary_list = Salary.objects.all()
        people_list =People.objects.all()
        id=request.GET["id"]
        s=Salary.objects.get(salaryid_id=id)
        p=People.objects.get(peopleid=id)
        f=codecs.open('1.csv', 'a', "UTF-8")
        swriter = csv.writer(f,dialect='excel')
        swriter.writerow([s.salaryid_id,p.name, s.hour, s.plus, s.forfeit,s.sub])
        p.allsalary=0
        s.sub=0
        s.save()
        p.save()
    return render_to_response("pay.html", {"salary_list":salary_list,"people_list":people_list})
#增
def inset_people(request):
    global userid
    if request.POST:
        post = request.POST
        id=post["id"]
        new_salary=Salary(
            salaryid_id=id,
            hour=0,
            plus=0,
            forfeit=0,
            sub=0
        )
        new_people = People(
            peopleid = id,
            name = post["name"],
            nation = post["nation"],
            phone = post["phone"],
            email = post["email"],
            date = post["date"],
            address = post["address"],
            birthday = post["birthday"],
            ptype_id = Salary_type.objects.get(typename=post["post_name"]).salary_typeid,
            allsalary = Salary_type.objects.get(typename=post["post_name"]).base_pay
            )
        if post["sex"] == "M":
            new_people.sex = True
        else:
            new_people.sex = False
        new_people.save()
        new_salary.save()
    return render_to_response("insert_people.html")
def insert_yewu(request):
    global userid
    if request.POST:
        user = Users.objects.get(userid = userid)
        post = request.POST
        new_yewu = Yewu(
            yewupeopleid_id = userid,
            yewuid = post["id"],
            title = post["title"],
            money = post["money"],
            person = post["person"],
            date = post["date"],
            beizhu = post["beizhu"],
            )
        new_yewu.save()
    return render_to_response("insert_yewu.html")
#删 没实际添加此功能
def delete(request):
    global userid
    getid = request.GET["id"]
    People.objects.get(id=getid).delete()
    People.objects.all()
    return render_to_response("delete.html")

#改
def update(request):
    global userid
    if 'search_name' in request.GET and People.objects.get(name=request.GET['search_name']):
        people= People.objects.get(name=request.GET['search_name'])
        postss = Salary.objects.get(id=people.ptype)
        if request.POST:
            post = request.POST
            if post["nation"]!="":
                people.nation = post["nation"]
            if post["phone"]!="":
                people.phone = post["phone"],
            if post["email"]!="":
                people.email = post["email"],
            if post["date"]!="":
                people.date = post["date"],
            if post["address"]!="":
                people.address = post["address"],
            if post["post_name"]!="":
                people.ptype = Salary_type.objects.get(typename=post["post_name"]).id,
            if post["birthday"]!="":
                people.birthday = post["birthday"]
            people.save()
            return render_to_response('main.html',{'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})
        return render_to_response('update.html', {'people':people,'post':postss})
def update_search(request):
    global userid
    return render_to_response('update_search.html')
def update_people(request):
    global userid
    if  request.GET :
        id=request.GET["id"]
        people= People.objects.get(peopleid=id)
        postss = Salary_type.objects.get(salary_typeid=people.ptype_id)
        if request.POST:
            post = request.POST
            if post["nation"]!="":
                people.nation = post["nation"]
            if post["phone"]!="":
                people.phone = post["phone"]
            if post["email"]!="":
                people.email = post["email"]
            if post["date"]!="":
                people.date = post["date"]
            if post["address"]!="":
                people.address = post["address"]
            if post["post_name"]!="":
                people.ptype_id = Salary_type.objects.get(typename=post["post_name"]).salary_typeid
            if post["birthday"]!="":
                people.birthday = post["birthday"]
            people.save()
            return render_to_response('main.html',{'users':Users.objects.get(userid=userid),'people':People.objects.get(peopleid=userid)})
        return render_to_response('update_people.html', {'people':people,'post':postss})
#查
def browse_ever_yewu(request):
    global userid
    yewu_list = Yewu.objects.all()
    if 'search_yewu' in request.POST:
        yewu=Yewu.objects.get(yewuid=request.POST['search_yewu'])
        return render_to_response('show_yewu.html',{"yewu":yewu})
    return render_to_response("show_ever_yewu.html",{"yewu_list":yewu_list})
def browse_ever_salary(request):
    global userid
    salary_list = Salary.objects.all()
    people_list =People.objects.all()
    for salary in salary_list:
        p=People.objects.get(peopleid=salary.salaryid_id)
        salary.sub = p.allsalary
        salary.save()
    if 'search_salary' in request.POST:
        salary=Salary.objects.get(salaryid_id=request.POST['search_salary'])
        people=People.objects.get(peopleid=salary.salaryid_id)
        return render_to_response('show_salary.html',{"salary":salary,"people":people})
    return render_to_response("show_ever_salary.html", {"salary_list":salary_list,"people_list":people_list})
def browse_ever_people(request):
    global userid
    people_list = People.objects.all()
    if 'search_people' in request.POST:
        people=People.objects.get(peopleid=request.POST['search_people'])
        return render_to_response('show_people.html',{"people":people})
    return render_to_response("show_ever_people.html", {"people_list":people_list})
def browse_salary(request):
    global userid
    people = People.objects.get(peopleid=userid)
    salary=Salary.objects.get(salaryid_id=userid)
    return render_to_response("show_salary.html", {"people":people,"salary":salary})
def browse_people(request):
    global userid
    people = People.objects.get(peopleid=userid)
    return render_to_response("show_people.html", {"people":people})
def search_people(request):
    if 'search_people' in request.POST:
        people=People.objects.get(peopleid=request.POST['search_people'])
        return render_to_response('show_people.html',{"people":people})
#search_yewu 该函数没用到
def search_yewu(request):
    global userid
    if 'search_id' in request.GET and People.objects.get(name=request.GET['search_id']):
        people= People.objects.get(name=request.GET['search_id'])
        postss = Salary.objects.get(id=people.postkey_id)
        salary = Full_salary.objects.filter(peopleid_id=people.postkey_id)
        if request.POST:
            post = request.POST
            new_salary = Full_salary(
                peopleid_id = people.id,
                datemonth = post["date1"],
                tsavings = post["tsaving"],
                zsavings = post["zsaving"]
                )
            new_salary.base = Salary.objects.get(id=people.postkey_id).base
            new_salary.all_salary = new_salary.base+ (float)(post["tsaving"])+(float)(post["zsaving"])
            new_salary.save()
            return render_to_response('main.html')
        return render_to_response('show_salary.html', {'people':people,'salary':salary,'salaryen':postss})
    else:
        return HttpResponse('please submit a seach term')
##
def details_yewu(request):
    global userid
    if 'search_name' in request.GET and Yewu.objects.get(title=request.GET['search_name']):
        yewu= Yewu.objects.get(title=request.GET['search_name'])

        user = Users.objects.get(id = userid)
        yewu_list = Yewu.objects.filter(id = user.id)
        if yewu.id == user.id:
            return render_to_response('YEWUfull.html', {'yewu':yewu})
    return render_to_response('show_yewu.html', {"yewu_list":yewu_list})
