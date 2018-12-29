from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext

from .models import Comment, Report

def reports(request):
    template = loader.get_template("news/reports.html")
    context = RequestContext(request, {"reports": Report.objects.all()})
    return HttpResponse(template.render(context))

def reports_detail(request, report_id):
    try: # could also use django.shortcuts.get_object_or_404(Report)
        report = Report.objects.get(id=report_id)
    except:
        raise Http404
    lines = [
        f"Report: {report.title} from {report.timestamp.strftime('%Y-%m-%dT %H:%m:%S')}",
        f"Text: {report.text}",
        "", "-"*30,
        "Comments:", ""
    ]
    lines += [f"{comment.author}: {comment.text}" for comment in report.comment_set.all()]
    response = HttpResponse("\n".join(lines))
    response["Content-Type"] = "text/plain"
    return response