from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CommunityPost, CommunityComment
from .forms import MarketPostForm, CommunityPostForm
import json


def get_board(board_en):
    board_dict = {"market": "장터 게시판",
                  "promotion": "홍보 게시판",
                  "free": "자유 게시판",
                  "study": "스터디/강의 게시판"}
    return board_dict[board_en]


def get_list_ctx(board_en, board_ko):
    queryset = CommunityPost.objects.filter(board=board_en).order_by("-created_at")
    ctx = {
        "board": board_ko,
        "posts": queryset,
    }
    return ctx


def market_list(request):
    ctx = get_list_ctx("market", "장터 게시판")
    return render(request, "community/community_list.html", ctx)


def promotion_list(request):
    ctx = get_list_ctx("promotion", "홍보 게시판")
    return render(request, "community/community_list.html", ctx)


def free_list(request):
    ctx = get_list_ctx("free", "자유 게시판")
    return render(request, "community/community_list.html", ctx)


def study_list(request):
    ctx = get_list_ctx("study", "스터디/강의 게시판")
    return render(request, "community/community_list.html", ctx)


def community_detail(request, pk):
    queryset = CommunityPost.objects.get(pk=pk)
    comments = CommunityComment.objects.filter(post=queryset)
    board = get_board(queryset.board)
    login_user = request.user
    is_post_user = True if queryset.user == login_user else False

    if request.method == "POST":
        post = queryset
        contents = request.POST["contents"]
        user = request.user
        CommunityComment.objects.create(post=post, contents=contents, user=user)
        return redirect("community:community_detail", pk)

    ctx = {
        "board": board,
        "post": queryset,
        "comments": comments,
        "login_user": login_user,
        "is_post_user": is_post_user,
    }
    return render(request, "community/community_detail.html", ctx)


def market_create(request):
    BOARD = "market"
    if request.method == "POST":
        form = MarketPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = BOARD
            post.save()
            return redirect("community:market_list")
    else:
        form = MarketPostForm()

    board = get_board(BOARD)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/market_create.html", ctx)


def promotion_create(request):
    BOARD = "promotion"
    if request.method == "POST":
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = BOARD
            post.save()
            return redirect("community:promotion_list")
    else:
        form = CommunityPostForm()

    board = get_board(BOARD)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/community_create.html", ctx)


def free_create(request):
    BOARD = "free"
    if request.method == "POST":
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = BOARD
            post.save()
            return redirect("community:free_list")
    else:
        form = CommunityPostForm()

    board = get_board(BOARD)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/community_create.html", ctx)


def study_create(request):
    BOARD = "study"
    if request.method == "POST":
        form = CommunityPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.board = BOARD
            post.save()
            return redirect("community:study_list")
    else:
        form = CommunityPostForm()

    board = get_board(BOARD)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/community_create.html", ctx)


def market_update(request, pk):
    queryset = CommunityPost.objects.get(pk=pk)
    board = get_board(queryset.board)

    if request.method == "POST":
        form = MarketPostForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect("community:community_detail", pk)
    else:
        form = MarketPostForm(instance=queryset)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/market_create.html", ctx)


def community_update(request, pk):
    queryset = CommunityPost.objects.get(pk=pk)
    board = get_board(queryset.board)

    if request.method == "POST":
        form = CommunityPostForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect("community:community_detail", pk)
    else:
        form = CommunityPostForm(instance=queryset)
    ctx = {
        "form": form,
        "board": board,
    }
    return render(request, "community/community_create.html", ctx)


def community_delete(request, pk):
    queryset = CommunityPost.objects.get(pk=pk)

    if request.method == "POST":
        queryset.delete()
        return redirect(f"community:{queryset.board}_list")
    return redirect("community:community_detail", pk)


def community_comment_update(request):
    json_object = json.loads(request.body)
    comment = CommunityComment.objects.filter(pk=json_object.get("id"))
    ctx = {"result": "FAIL"}
    if comment:
        comment.update(contents=json_object.get("contents"))  # update queryset에서만 동작 (get 대신 filter 사용)
        ctx = {"result": "SUCCESS"}
    return JsonResponse(ctx)


def community_comment_delete(request):
    json_object = json.loads(request.body)
    comment = CommunityComment.objects.filter(pk=json_object.get("id"))
    ctx = {"result": "FAIL"}
    if comment:
        comment.delete()
        ctx = {"result": "SUCCESS"}
    return JsonResponse(ctx)
