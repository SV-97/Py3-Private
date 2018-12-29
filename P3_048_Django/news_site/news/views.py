from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Comment, Report

def reports(request):
    lines = []
    for report in Report.objects.all():
        lines.append(f"Report: {report.title} from {report.timestamp.strftime('%Y-%m-%dT %H:%m:%S')}")
        lines.append(f"Text: {report.text}")
        lines += ["", "-"*30, ""]
    response = HttpResponse("\n".join(lines))
    response["Content-Type"] = "text/plain"
    return response

def reports_detail(request, report_id):
    try: # could also use django.shortcuts.get_object_of_404(Report)
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