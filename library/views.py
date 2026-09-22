from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Book, BorrowBook


def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect("admin_dashboard")

            return redirect("dashboard")

        return render(request, "home.html", {
            "error": "Invalid username or password"
        })

    return render(request, "home.html")

def admin_dashboard(request):

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "admin_delete":
            book_id = request.POST["book_id"]
            Book.objects.get(id=book_id).delete()

        elif action == "admin_edit":
            book_id = request.POST["book_id"]

            title = request.POST["title"]
            author = request.POST["author"]
            category = request.POST["category"]
            quantity = request.POST["quantity"]

            book = Book.objects.get(id=book_id)

            book.title = title
            book.author = author
            book.category = category
            book.quantity = quantity

            book.save()

        elif action == "admin_return":
            borrow_id = request.POST["borrow_id"]

            borrow = BorrowBook.objects.get(id=borrow_id)

            if borrow.return_date is None:
                borrow.return_date = __import__("datetime").date.today()
                borrow.save()

                book = borrow.book
                book.quantity += 1
                book.save()
        elif action == "admin_logout":
            logout(request)
            return redirect("home")
        
        return redirect("admin_dashboard")

    books = Book.objects.all()
    borrowed_books = BorrowBook.objects.all()

    return render(request, "admin_dashboard.html", {
        "books": books,
        "borrowed_books": borrowed_books
    })

def dashboard(request):
    if request.method == "POST":

        action = request.POST.get("action")

        if action == "add":
            title = request.POST["title"]
            author = request.POST["author"]
            category = request.POST["category"]
            quantity = request.POST["quantity"]

            Book.objects.create(
                title=title,
                author=author,
                category=category,
                quantity=quantity
            )

        elif action == "delete":
            book_id = request.POST["book_id"]
            Book.objects.get(id=book_id).delete()

        elif action == "edit":
            book_id = request.POST["book_id"]
            title = request.POST["title"]
            author = request.POST["author"]
            category = request.POST["category"]
            quantity = request.POST["quantity"]

            book = Book.objects.get(id=book_id)

            book.title = title
            book.author = author
            book.category = category
            book.quantity = quantity
            book.save()

        elif action == "borrow":
            book_id = request.POST["book_id"]
            username = request.POST["username"]

            book = Book.objects.get(id=book_id)

            if book.quantity > 0:
                BorrowBook.objects.create(
                    username=username,
                    book=book,
                    borrow_date=__import__("datetime").date.today()
                )

                book.quantity -= 1
                book.save()
        elif action == "return":
            borrow_id = request.POST["borrow_id"]

            borrow = BorrowBook.objects.get(id=borrow_id)

            if borrow.return_date is None:
                borrow.return_date = __import__("datetime").date.today()
                borrow.save()

                borrow.book.quantity += 1
                borrow.book.save()
        elif action == "logout":
            logout(request)
            return redirect("home")

        return redirect("dashboard")

    books = Book.objects.all()
    borrowed_books = BorrowBook.objects.all()

    return render(request, "dashboard.html", {
        "books": books,
        "borrowed_books": borrowed_books
    })