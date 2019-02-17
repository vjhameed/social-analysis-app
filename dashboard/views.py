from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from dashboard.utils import *
from django.shortcuts import render
import datetime
from dateutil.parser import parse
from accounts.models import Folder
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from dashboard.models import Project



def HomePageView(request):
    projects = Project.objects.all()
    return render(request,'core/index.html',{"projects":projects})

def SearchSettingView(request,proid):
    projects = Project.objects.all()
    project = Project.objects.get(id=proid)
    
    if request.POST:
        if request.POST.get('keywords',False):
            project.title = request.POST['title']
            project.key1 = request.POST['key1']        
            project.key2 = request.POST['key2']        
            project.key3 = request.POST['key3']        
            project.key4 = request.POST['key4']        
            project.key5 = request.POST['key5']        
            project.key6 = request.POST['key6']        
            project.key7 = request.POST['key7']        
            project.key8 = request.POST['key8']        
            project.key9 = request.POST['key9']        
            project.key10 = request.POST['key10']        
            project.exkey1 = request.POST['exkey1']        
            project.exkey2 = request.POST['exkey2']        
            project.exkey3 = request.POST['exkey3']        
            project.exkey4 = request.POST['exkey4']        
            project.exkey5 = request.POST['exkey5']        
            project.exkey6 = request.POST['exkey6']        
            project.exkey7 = request.POST['exkey7']        
            project.exkey8 = request.POST['exkey8']        
            project.exkey9 = request.POST['exkey9']        
            project.exkey10 = request.POST['exkey10']        
            project.save()
        elif request.POST.get('notifications',False):
            project.notification_duration = request.POST['notification_duration']
            project.notification_email = request.POST['notification_email']
            project.save()

    return render(request,'core/search-setting.html',{"projects":projects,'pro':project})

def DeleteProject(request,pid):
    pro = Project.objects.get(id=pid)    
    pro.delete()
    return redirect('dashboard')

def GeneralDashboardView(request):
    projects = Project.objects.all()
    return render(request,'core/general.html',{"projects":projects})

def BrandDashboard(request):
    projects = Project.objects.all()
    return render(request,'core/branddash.html',{"projects":projects})

def CompetitiveDashboard(request):
    projects = Project.objects.all()
    return render(request,'core/comp-dash.html',{"projects":projects})

def InfluencerDashboard(request):
    projects = Project.objects.all()
    return render(request,'core/inf-dash.html',{"projects":projects})

def MentionsDashboard(request):
    projects = Project.objects.all()
    return render(request,'core/mentions.html',{"projects":projects})

def CreateProject(request):
    if request.method == 'POST':
        pro = Project()
        pro.title = request.POST['project_name']
        pro.notification_duration = 8
        pro.save()
    return redirect('dashboard')
        


        

# class PageView(TemplateView):
#     template_name = 'core/Page.html'

#     def render_to_response(self, context, **response_kwargs):
#         if context is None:
#             url = reverse("logout")
#             return redirect(url, args=(), kwargs={})
#         return super(PageView, self).render_to_response(
#             context, **response_kwargs
#         )

#     def get_context_data(self, **kwargs):
#         context = super(PageView, self).get_context_data(**kwargs)
#         try:
#             comments = self.request.session['comments']
#             del self.request.session['comments']
#         except Exception as e:
#             pass
#         if 'page' in self.request.path:
#             context['redirect']='page'
#         else:
#             context['redirect'] = 'comments'
#         user = self.request.user
#         try:
#             context['pages'] = getUserPages(user.fb_token)
#         except Exception as e:
#             if str(e) == "facebook":
#                return None

#             print("something went wrong")
#             context['pages']= []
#         return context

# class PageDetailView(TemplateView):
#     template_name = 'core/PageDetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(PageDetailView, self).get_context_data(**kwargs)
#         user = self.request.user
#         page_id = self.kwargs.get('page_id')
#         page_token = self.request.GET.get('token')
#         try:
#             context['page'] = getPageDetail(page_id, page_token)
#             posts = getPagePosts(page_id, page_token)
#             list=[]
#             comments_list = []
#             for post in posts:
#                 comments = getPostComments(post['id'], page_token)
#                 comments_list.extend(comments)
#                 list.append({
#                     'post': post,
#                     'comments': comments
#                 })

#             context['objs'] = list
#             self.request.session['comments'] = comments_list
#             self.request.session['page_token'] = context['page']['access_token']
#         except Exception as e:
#             if str(e) == "facebook":
#                 return None
#             print("something went wrong")
#             context['pages']= []
#         return context

#     def render_to_response(self, context, **response_kwargs):
#         if context is None:
#             url = reverse("logout")
#             return redirect(url, args=(), kwargs={})
#         return super(PageDetailView, self).render_to_response(
#             context, **response_kwargs
#         )



# class CommentDetailView(TemplateView):
#     template_name = 'core/CommentDetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(CommentDetailView, self).get_context_data(**kwargs)
#         user = self.request.user
#         page_id = self.kwargs.get('page_id')
#         token = self.request.GET.get('token')
#         context['filter'] = '7days'
#         try:
#             comments = self.request.session['comments']
#             context['comments'] = comments
#             return context
#         except Exception as e:
#             pass
#         try:
#             page = getPageDetail(page_id, token)
#             page_token = page['access_token']
#             posts = getPagePosts(page_id, page_token)
#             comments = []
#             for post in posts:
#                 comment = getPostComments(post['id'], page_token)
#                 comments.extend(comment)
#             context['comments'] = comments
#             self.request.session['comments'] = comments
#         except Exception as e:
#             if str(e) == "facebook":
#                 return None
#             context['comments']= []
#         return context



#     def post(self, request, *args, **kwargs):
#         try:
#             start = self.request.POST.get('start_date')
#             end = self.request.POST.get('end_date')
#             filter_type = self.request.POST.get('filter_type')
#             start_date = parse(start)
#             end_date = parse(end)
#             filter = []
#             context = {}
#             comments = self.request.session['comments']
#             if filter_type == 'all':
#                 context['comments'] = comments
#                 context['filter'] = filter_type
#                 return render(self.request, self.template_name, context)
#             if filter_type == '':
#                 context['start_date'] = start
#                 context['end_date'] = end
#             for comment in comments:
#                 date = parse(comment['created_time'])
#                 date = date.replace(tzinfo=None)
#                 if(date >= start_date and date<=end_date):
#                     filter.append(comment)
#             context['comments'] = filter
#             context['filter'] = filter_type
#             return render(self.request, self.template_name, context)

#         except Exception as e:
#             if str(e) == "facebook":
#                 return None
#             context = {}
#             context['comments'] = []
#             return render(self.request, self.template_name, context)

#     def render_to_response(self, context, **response_kwargs):
#         if context is None:
#             url = reverse("logout")
#             return redirect(url, args=(), kwargs={})
#         return super(CommentDetailView, self).render_to_response(
#             context, **response_kwargs
#         )

# class FolderView(TemplateView):
#     template_name = 'core/Folder.html'

#     def get_context_data(self, **kwargs):
#         context = super(FolderView, self).get_context_data(**kwargs)
#         user = self.request.user
#         context['folders'] = Folder.objects.filter(user=user)
#         return context

#     def post(self, request, *args, **kwargs):
#         data = self.request.POST.get('data')
#         name = self.request.POST.get('name')
#         user = self.request.user
#         if name and data:
#             try:
#                 Folder.objects.create(user=user, name=name, data=json.loads(data))
#                 payload = {'success': True}
#                 return HttpResponse(json.dumps(payload), content_type='application/json')
#             except Exception as e:
#                 payload = {'success': False}
#                 return HttpResponse(json.dumps(payload), content_type='application/json')
#         else:
#             payload = {'success': False, 'message': 'request parameters missing'}
#             return HttpResponse(json.dumps(payload), content_type='application/json')


# class FolderDetailView(TemplateView):
#     template_name = 'core/FolderDetail.html'

#     def get_context_data(self, **kwargs):
#         context = super(FolderDetailView, self).get_context_data(**kwargs)
#         user = self.request.user
#         folder_id = self.kwargs.get('folder_id')
#         try:
#             context['folder'] = Folder.objects.get(id=folder_id, user=user)
#         except Exception as e:
#             print("something went wrong")
#             context['folder']= []
#         return context