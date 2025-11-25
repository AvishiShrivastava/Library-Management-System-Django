# libraryapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Book, Member, IssueRecord
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def home(request):
    stats = {
        'total_books': Book.objects.count(),
        'available_books': Book.objects.filter(available=True).count(),
        'members': Member.objects.count(),
        'issued': IssueRecord.objects.filter(return_date__isnull=True).count(),
    }
    return render(request, 'libraryapp/home.html', {'stats': stats})

# ---------------- Books ----------------
@login_required
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title','').strip()
        author = request.POST.get('author','').strip()
        isbn = request.POST.get('isbn','').strip()
        if not title or not author:
            messages.error(request, "Title and author are required.")
            return redirect('add_book')
        Book.objects.create(title=title, author=author, isbn=isbn)
        messages.success(request, f'Book "{title}" added.')
        return redirect('view_books')
    return render(request, 'libraryapp/add_book.html')
@login_required
def view_books(request):
    """
    List books with optional search and server-side pagination.

    Query params:
      - q : search string (title OR author OR isbn)
      - page : page number (defaults to 1)
    """
    q = request.GET.get('q', '').strip()

    # base queryset
    books_qs = Book.objects.all().order_by('title')

    # apply search if provided
    if q:
        # use icontains for case-insensitive partial match
        books_qs = books_qs.filter(
            models.Q(title__icontains=q) |
            models.Q(author__icontains=q) |
            models.Q(isbn__icontains=q)
        )

    # pagination
    page = request.GET.get('page', 1)
    per_page = 6  # change to whatever you prefer
    paginator = Paginator(books_qs, per_page)

    try:
        books_page = paginator.page(page)
    except PageNotAnInteger:
        books_page = paginator.page(1)
    except EmptyPage:
        books_page = paginator.page(paginator.num_pages)

    context = {
        'books': books_page,   # paginated page object (iterate like a list)
        'q': q,
        'paginator': paginator,
        'page_obj': books_page,  # consistent with Django generic view naming
    }
    return render(request, 'libraryapp/view_books.html', context)
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title','').strip()
        book.author = request.POST.get('author','').strip()
        book.isbn = request.POST.get('isbn','').strip()
        book.available = True if request.POST.get('available') == 'on' else False
        book.save()
        messages.success(request, 'Book updated.')
        return redirect('view_books')
    return render(request, 'libraryapp/edit_book.html', {'book': book})
@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    messages.success(request, 'Book deleted.')
    return redirect('view_books')

# ---------------- Members ----------------
@login_required
def add_member(request):
    if request.method == "POST":
        name = request.POST.get('name','').strip()
        email = request.POST.get('email','').strip()
        phone = request.POST.get('phone','').strip()
        if not name:
            messages.error(request, "Member name required.")
            return redirect('add_member')
        Member.objects.create(name=name, email=email, phone=phone)
        messages.success(request, f'Member "{name}" added.')
        return redirect('view_members')
    return render(request, 'libraryapp/add_member.html')
@login_required
def view_members(request):
    members = Member.objects.all().order_by('name')
    return render(request, 'libraryapp/view_members.html', {'members': members})
@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    member.delete()
    messages.success(request, 'Member deleted.')
    return redirect('view_members')

# ---------------- Issue & Return ----------------
@login_required
def issue_book(request):
    if request.method == "POST":
        member_id = request.POST.get('member')
        book_id = request.POST.get('book')
        member = get_object_or_404(Member, pk=member_id)
        book = get_object_or_404(Book, pk=book_id)
        if not book.available:
            messages.error(request, f'Book "{book.title}" is currently not available.')
            return redirect('issue_book')
        IssueRecord.objects.create(member=member, book=book)
        book.available = False
        book.save()
        messages.success(request, f'Issued "{book.title}" to {member.name}.')
        return redirect('view_issued')
    members = Member.objects.filter().order_by('name')
    books = Book.objects.filter(available=True).order_by('title')
    return render(request, 'libraryapp/issue_book.html', {'members': members, 'books': books})
@login_required
def view_issued(request):
    issued = IssueRecord.objects.select_related('member','book').order_by('-issue_date')
    return render(request, 'libraryapp/view_issued.html', {'issued': issued})
@login_required
def return_book(request, issue_id):
    issue = get_object_or_404(IssueRecord, pk=issue_id)
    if issue.return_date:
        messages.info(request, 'Book already returned.')
    else:
        issue.return_date = timezone.now().date()
        issue.save()
        book = issue.book
        book.available = True
        book.save()
        messages.success(request, f'Book "{book.title}" returned.')
    return redirect('view_issued')
# Edit book (if not already present or to replace)
@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title','').strip()
        book.author = request.POST.get('author','').strip()
        book.isbn = request.POST.get('isbn','').strip()
        # optional: if you have quantity field
        qty = request.POST.get('quantity')
        if qty is not None and qty != '':
            try:
                book.quantity = int(qty)
            except ValueError:
                pass
        # checkbox for available (if field exists)
        if hasattr(book, 'available'):
            book.available = True if request.POST.get('available') == 'on' else False
        book.save()
        messages.success(request, 'Book updated.')
        return redirect('view_books')
    return render(request, 'libraryapp/edit_book.html', {'book': book})
@login_required
# Edit member
def edit_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    if request.method == "POST":
        member.name = request.POST.get('name','').strip()
        member.email = request.POST.get('email','').strip()
        member.phone = request.POST.get('phone','').strip()
        member.save()
        messages.success(request, 'Member updated.')
        return redirect('view_members')
    return render(request, 'libraryapp/edit_member.html', {'member': member})
@staff_member_required
def staff_dashboard(request):
    # simple example: show all issued records and basic stats
    stats = {
        'total_books': Book.objects.count(),
        'total_members': Member.objects.count(),
        'issued_count': IssueRecord.objects.filter(return_date__isnull=True).count(),
    }
    issued = IssueRecord.objects.select_related('member','book').order_by('-issue_date')[:30]
    return render(request, 'libraryapp/staff_dashboard.html', {'stats': stats, 'issued': issued})


