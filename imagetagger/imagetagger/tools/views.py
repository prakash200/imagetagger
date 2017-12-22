from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.db import transaction
from django.db.models import Q
from django.template.response import TemplateResponse
from django.contrib import messages
from .models import Tool
from .forms import ToolUploadForm
import os


def tools_enabled(in_function):
    if not settings.TOOLS_ENABLED:
        raise Http404
    return in_function


@tools_enabled
@login_required
def overview(request):
    tools = Tool.objects.select_related('team').order_by(
        'name').filter(
        Q(team__members=request.user) | Q(public=True)).distinct()
    return TemplateResponse(request, 'overview.html', {
        'tools': tools,
        'form' : ToolUploadForm(),
    })


@tools_enabled
@login_required
def create_tool(request):
    if request.method == 'POST':
        form = ToolUploadForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                tool = form.instance
                tool.save()
            tool.filename = '{}_{}'.format(tool.id,
                                           request.FILES['file'].name)
            if not os.path.isdir(settings.TOOLS_PATH):
                os.makedirs(settings.TOOLS_PATH)
            with open(os.path.join(settings.TOOLS_PATH, tool.filename), 'wb+') as f:
                for chunk in request.FILES['file']:
                    f.write(chunk)
            messages.success(request, 'The tool was successfully uploaded')
            return redirect(reverse('tools:overview'))

    messages.error(request, 'There was an error with your upload. You can only upload files up to 2 MiB')
    return redirect(reverse('tools:overview'))



@tools_enabled
@login_required
def edit_tool(request, tool_id):
    pass


@tools_enabled
@login_required
def delete_tool(request, tool_id):
    pass


@tools_enabled
@login_required
def download_tool(request, tool_id):
    pass
