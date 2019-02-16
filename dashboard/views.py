from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from django.views.generic.base import RedirectView, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from dashboard.utils import *
from django.shortcuts import render
import datetime
from dateutil.parser import parse
from accounts.models import Folder
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import redirect, render
from django.urls import reverse
from dashboard.models import Project



def HomePageView(request):
    projects = Project.objects.all()
    return render(request,'core/index.html',{"projects":projects})

def SearchSettingView(TemplateView):
    projects = Project.objects.all()
    return render(request,'core/search-setting.html',{"projects":projects})

def GeneralDashboardView(error):
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
        pro.notification_duration = 7
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