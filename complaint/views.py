from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Complaint, ComplaintComment
from .forms import ComplaintForm
import json


def complaint_list(request):
    queryset = Complaint.objects.all().order_by("-created_at")
    login_user = request.user
    ctx = {
        "posts": queryset,
        "login_user": login_user,
    }
    return render(request, "complaint/complaint_list.html", ctx)


def complaint_detail(request, pk):
    queryset = Complaint.objects.get(pk=pk)
    comments = ComplaintComment.objects.filter(post=queryset)  # .get() 함수는 하나의 object return
    login_user = request.user
    is_post_user = True if queryset.user == login_user else False

    if request.method == "POST":
        post = queryset
        contents = request.POST["contents"]
        user = request.user
        ComplaintComment.objects.create(post=post, contents=contents, user=user)
        return redirect("complaint:complaint_detail", pk)  # 양식 재제출 방지 (새로고침 시 마지막 작성 댓글 재작성 막기)

    ctx = {
        "post": queryset,
        "comments": comments,
        "is_post_user": is_post_user,
        "login_user": login_user,
    }
    return render(request, "complaint/complaint_detail.html", ctx)


def complaint_create(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("complaint:complaint_list")
    else:
        form = ComplaintForm()
    ctx = {
        "form": form,
    }
    return render(request, "complaint/complaint_create.html", ctx)


def complaint_comment_update(request):
    json_object = json.loads(request.body)
    comment = ComplaintComment.objects.filter(pk=json_object.get("id"))
    ctx = {"result": "FAIL"}
    if comment:
        comment.update(contents=json_object.get("contents"))  # update queryset에서만 동작 (get 대신 filter 사용)
        ctx = {"result": "SUCCESS"}
    return JsonResponse(ctx)


def complaint_comment_delete(request):
    json_object = json.loads(request.body)
    comment = ComplaintComment.objects.filter(pk=json_object.get("id"))
    ctx = {"result": "FAIL"}
    if comment:
        comment.delete()
        ctx = {"result": "SUCCESS"}
    return JsonResponse(ctx)
