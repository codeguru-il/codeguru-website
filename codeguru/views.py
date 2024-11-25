from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import translation
from django.utils.crypto import get_random_string
from django.utils.translation import gettext

from website.settings import CAN_REGISTER

from .forms import NewCenterForm, NewGroupForm, NewUserForm
from .models import Center, CgGroup, Invite, Message, Profile, User, group_name_validator, validate_center


def error(request, msg):
    return render(request, "error.html", {"error_message": msg})


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def delete_profile(request):
    request.user.delete()
    return redirect("/")


def group(request, id=None):
    render_params = {"form": NewGroupForm(), "CAN_REGISTER": CAN_REGISTER}

    if (not id) and request.user:
        if request.user.profile.group:
            return redirect("group", id=request.user.profile.group.id)

        if request.method == "POST":
            form = NewGroupForm(request.POST)
            if form.is_valid():
                new_group = CgGroup(
                    name=form.cleaned_data["name"],
                    owner=request.user,
                    center=form.cleaned_data["center"],
                    competition=form.cleaned_data["competition"],
                )
                new_group.save()
                request.user.profile.group = new_group
                request.user.profile.save()

                return redirect("group", id=new_group.id)

            if CgGroup.objects.all().filter(name=form.data["name"]).exists():
                return error(request, gettext("Group already exists. try choosing another name."))
            try:
                group_name_validator(form.data["name"])
            except:
                return error(
                    request,
                    gettext(
                        "Group name is invalid. Groups names may only include alphanumerical characters and underscores"
                    ),
                )
            return error(request, form.errors)

        return render(request, "group.html", render_params)

    current_group: CgGroup = CgGroup.objects.all().filter(id=id).first()
    if not current_group:
        return error(request, "Group not found.")

    members = list(User.objects.all().filter(profile__group__exact=current_group))
    members.sort(key=lambda member: member.username)

    # Sort for group owner to be appear first. When sorting python puts False before True
    group_owner = members[0].profile.group.owner
    members.sort(key=lambda member: member != group_owner)

    try:
        link_expired = current_group.invite.expired
    except:
        link_expired = False

    return render(
        request,
        "group.html",
        {
            **render_params,
            "is_expired": link_expired,
            "group": current_group,
            "members": members,
            "is_in_group": (current_group == request.user.profile.group) if request.user.is_authenticated else False,
        },
    )


def center(request, tkr: str):
    if len(tkr) != 3:
        return error(request, "Sorry the center ticker must be 3 chars")
    center = Center.objects.all().filter(ticker=tkr).first()
    return render(request, "center.html", {"center": center, "groups": CgGroup.objects.all().filter(center=center)})


@login_required
def new_center(request):
    if request.user and request.method == "POST":
        form = NewCenterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            ticker = form.cleaned_data["ticker"]

            if Center.objects.filter(ticker=ticker).exists():
                return error(request, gettext("Center {} already exists.".format(ticker)))

            new_center = Center(name=name, ticker=ticker)
            new_center.save()
            return redirect("group")
        try:
            validate_center(form.name)
            return error(request, form.errors)
        except:
            return error(request, gettext("Center should be represented with 3 letters in english."))

    return render(request, "new_center.html", {"form": NewCenterForm})


def register(request):
    if request.user.is_authenticated:
        return redirect("profile/")
    if request.method == "POST":
        form = NewUserForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
            except ValidationError as e:
                return error(request, f"{' '.join(e)}")
            login(request, user)
            return redirect("/")
    form = NewUserForm()
    return render(request, "registration/registration_form.html", {"form": form})


@login_required
def invite(request, code):
    if request.user.profile.group:
        return error(request, gettext("You must leave your group first."))
    try:
        invite = Invite.objects.get(code=code)
        if invite.expired:
            return error(request, gettext("Invite expired."))
        if Profile.objects.filter(group=invite.group).count() >= 3:
            return error(request, gettext("Sorry groups must be 3 members max."))
        if request.user.profile.group != invite.group:
            leave_group(request)
        request.user.profile.group = invite.group
        request.user.profile.save()
        return redirect("/group/")
    except Invite.DoesNotExist:
        return error(request, gettext("Invalid Invite link."))


@login_required
def create_invite(request):
    if not request.user.profile.group:
        return error(request, gettext("You do not have a group."))
    if request.user != request.user.profile.group.owner:
        return error(request, gettext("Only an owner can create a group invite."))

    try:
        invite = Invite.objects.get(group=request.user.profile.group)
    except Invite.DoesNotExist:
        invite = Invite(group=request.user.profile.group, code=get_random_string(64))
        invite.save()
    return redirect("/group/")


@login_required
def leave_group(request):
    if request.user.profile.group:
        group = request.user.profile.group
        members = Profile.objects.all().filter(group=group)
        if members.count() == 1:
            group.delete()
        else:
            request.user.profile.group = None
            request.user.profile.save()
            if request.user == group.owner:
                group.owner = Profile.objects.all().filter(group=group).first().user
            group.save()
    return redirect("/group/")


def set_lang(request):
    if request.method == "POST":
        language = request.POST.get("language", "en")
        if language not in ("en", "he"):
            return HttpResponse("Bad request", status=400)

        translation.activate(language)

        next_uri: str = request.POST["next"].removeprefix(f"/{request.LANGUAGE_CODE}")
        response = redirect(next_uri)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response
    return HttpResponse("Method Not Allowed", status=405)


def index(request):
    return render(
        request,
        "index.html",
        {
            "groups": CgGroup.objects.all(),
            "messages": enumerate(Message.objects.order_by("-date")),
            "users": User.objects.all(),
        },
    )
