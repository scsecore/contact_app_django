from django.shortcuts import render, redirect
from contact_app.models import Contact, PasswordResetToken,Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib import messages


# ─── Contacts (index) ─────────────────────────────────────────────────────────

@login_required
def sss(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        category_id = request.POST.get("category")

        # Phone validation
        if not phone.isdigit():
            contacts = Contact.objects.filter(user=request.user)
            categories = Category.objects.filter(user=request.user)

            return render(request, "contact/index.html", {
                "contacts": contacts,
                "categories": categories,
                "error": "Phone number must contain only digits"
            })

        if len(phone) != 10:
            contacts = Contact.objects.filter(user=request.user)
            categories = Category.objects.filter(user=request.user)

            return render(request, "contact/index.html", {
                "contacts": contacts,
                "categories": categories,
                "error": "Phone number must be exactly 10 digits"
            })

        # Duplicate phone check
        if Contact.objects.filter(
            user=request.user,
            phone=phone
        ).exists():

            contacts = Contact.objects.filter(user=request.user)
            categories = Category.objects.filter(user=request.user)

            return render(request, "contact/index.html", {
                "contacts": contacts,
                "categories": categories,
                "error": "Phone number already exists"
            })

        # Duplicate email check
        if email and Contact.objects.filter(
            user=request.user,
            email=email
        ).exists():

            contacts = Contact.objects.filter(user=request.user)
            categories = Category.objects.filter(user=request.user)

            return render(request, "contact/index.html", {
                "contacts": contacts,
                "categories": categories,
                "error": "Email already exists"
            })

        category = None

        if category_id:
            category = Category.objects.get(
                id=category_id,
                user=request.user
            )

        Contact.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            category=category
        )

    search = request.GET.get("search")

    contacts = Contact.objects.filter(
        user=request.user
    )

    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )

    categories = Category.objects.filter(
        user=request.user
    )

    return render(
        request,
        "contact/index.html",
        {
            "contacts": contacts,
            "categories": categories,
            "search": search
        }
    )

# CRUD operations for contacts

def delete_contact(request, id):

    contact = Contact.objects.get(
        id=id,
        user=request.user
    )

    contact.delete()

    messages.success(
        request,
        "Contact deleted successfully!"
    )

    return redirect("index")

def edit_contact(request, id):

    contact = Contact.objects.get(
        id=id,
        user=request.user
    )

    categories = Category.objects.filter(
        user=request.user
    )

    if request.method == "POST":

        contact.name = request.POST.get("name")
        contact.email = request.POST.get("email")
        contact.phone = request.POST.get("phone")

        category_id = request.POST.get("category")

        if category_id:
            contact.category = Category.objects.get(
                id=category_id,
                user=request.user
            )
        else:
            contact.category = None

        contact.save()

        return redirect("index")

    return render(
        request,
        "contact/edit_contact.html",
        {
            "contact": contact,
            "categories": categories
        }
    )
    

# ------------------------------------------profile---------------------------------------------------------
@login_required
def profile(request):
    return render(
        request,
        "contact/profile.html",
        {
            "user": request.user
        }
    )

def about(request):
    return render(request, "contact/about.html")
    
def category_page(request):

    if request.method == "POST":

        category_name = request.POST.get("category_name")

        Category.objects.create(
            user=request.user,
            name=category_name
        )

    categories = Category.objects.filter(user=request.user)

    return render(
        request,
        "contact/category.html",
        {
            "categories": categories
        }
    )
    # -------------------------------delete category---------------------------------------------------------
def delete_category(request, id):

    category = get_object_or_404(
        Category,
        id=id,
        user=request.user
    )

    category.delete()

    return redirect("categories")

@login_required
def category_contacts(request, id):

    category = get_object_or_404(
        Category,
        id=id,
        user=request.user
    )

    contacts = Contact.objects.filter(
        user=request.user,
        category=category
    )

    return render(
        request,
        "contact/category_contacts.html",
        {
            "category": category,
            "contacts": contacts
        }
    )