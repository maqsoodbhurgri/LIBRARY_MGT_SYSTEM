import datetime

# ---------- Base Classes ----------
class Person:
    def __init__(self, name):
        self.name = name

    def display_info(self):
        print(f"Name: {self.name}")


# ---------- Inheritance Example ----------
class Member(Person):
    def __init__(self, member_id, name):
        super().__init__(name)
        self.member_id = member_id
        self.borrowed_books = []

    def display_info(self):
        print(f"Member ID: {self.member_id}, Name: {self.name}, Borrowed Books: {len(self.borrowed_books)}")


class Book:
    def __init__(self, book_id, title, author, total_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies

    def display_info(self):
        print(f"[{self.book_id}] {self.title} by {self.author} | Total: {self.total_copies}, Available: {self.available_copies}")


# ---------- Borrow Record ----------
class BorrowRecord:
    def __init__(self, member, book, borrow_date, due_date):
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    def mark_returned(self, return_date):
        self.return_date = return_date

    def is_overdue(self):
        if self.return_date is None:
            return datetime.date.today() > self.due_date
        return self.return_date > self.due_date

    def display_info(self):
        print(f"Member: {self.member.name}, Book: {self.book.title}, "
              f"Borrowed: {self.borrow_date}, Due: {self.due_date}, "
              f"Returned: {self.return_date if self.return_date else 'Not yet returned'}")


# ---------- Library Class (Polymorphism used in display methods) ----------
class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.borrow_records = []
        self.next_book_id = 1
        self.next_member_id = 1

    # ---------- Book Management ----------
    def add_book(self, title, author, total_copies):
        book = Book(self.next_book_id, title, author, total_copies)
        self.books.append(book)
        print(f"\n Book '{title}' added with ID {self.next_book_id}.")
        self.next_book_id += 1

    def display_all_books(self):
        if not self.books:
            print("\n No books available.")
            return
        print("\n--- All Books ---")
        for book in self.books:
            book.display_info()

    def display_available_books(self):
        available = [b for b in self.books if b.available_copies > 0]
        if not available:
            print("\n No available books right now.")
            return
        print("\n--- Available Books ---")
        for book in available:
            book.display_info()

    def search_book(self, keyword):
        found = [b for b in self.books if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
        if not found:
            print("\n No books found with that keyword.")
        else:
            print("\n Search Results:")
            for b in found:
                b.display_info()

    # ---------- Member Management ----------
    def add_member(self, name):
        member = Member(self.next_member_id, name)
        self.members.append(member)
        print(f"\n Member '{name}' registered with ID {self.next_member_id}.")
        self.next_member_id += 1

    def display_members(self):
        if not self.members:
            print("\n👥 No members found.")
            return
        print("\n--- All Members ---")
        for m in self.members:
            m.display_info()

    def delete_member(self, member_id):
        for m in self.members:
            if m.member_id == member_id:
                if m.borrowed_books:
                    print("\n Cannot delete member with borrowed books.")
                    return
                self.members.remove(m)
                print(f"\n Member '{m.name}' deleted.")
                return
        print("\n Member not found.")

    # ---------- Borrow & Return ----------
    def borrow_book(self, member_id, book_id):
        member = self._find_member(member_id)
        book = self._find_book(book_id)

        if not member or not book:
            print("\n Invalid member or book ID.")
            return

        if book.available_copies == 0:
            print(f"\n '{book.title}' is not available right now.")
            return

        try:
            days = int(input(" Enter number of days to borrow (default 15): ") or 15)
        except ValueError:
            days = 15 

        borrow_date = datetime.date.today()
        due_date = borrow_date + datetime.timedelta(days=days)

        record = BorrowRecord(member, book, borrow_date, due_date)
        self.borrow_records.append(record)

        member.borrowed_books.append(record)
        book.available_copies -= 1

        print(f"\n '{book.title}' borrowed by {member.name}.")
        print(f"Borrow Date: {borrow_date}, Due Date: {due_date}")
        print(f" Copies Left: {book.available_copies}/{book.total_copies}")

    def return_book(self, member_id, book_id):
        member = self._find_member(member_id)
        book = self._find_book(book_id)

        if not member or not book:
            print("\n Invalid member or book ID.")
            return

        for record in member.borrowed_books:
            if record.book.book_id == book_id and record.return_date is None:
                record.mark_returned(datetime.date.today())
                book.available_copies += 1
                print(f"\n '{book.title}' returned by {member.name}.")
                if record.is_overdue():
                    print(" This book was returned late!")
                member.borrowed_books.remove(record)
                return
        print("\n No borrowed record found for this book.")

    def view_member_borrowed_books(self, member_id):
        member = self._find_member(member_id)
        if not member:
            print("\n Member not found.")
            return
        print(f"\n Books borrowed by {member.name}:")
        found = False
        for record in self.borrow_records:
            if record.member == member and record.return_date is None:
                record.display_info()
                found = True
        if not found:
            print("No active borrowed books.")

    def view_overdue_books(self):
        print("\n Overdue Books:")
        found = False
        for record in self.borrow_records:
            if record.is_overdue() and record.return_date is None:
                record.display_info()
                found = True
        if not found:
            print(" No overdue books!")

    def library_report(self):
        print("\n=====  Library Report =====")
        print(f"Total Books: {len(self.books)}")
        print(f"Total Members: {len(self.members)}")
        active_borrows = sum(1 for r in self.borrow_records if r.return_date is None)
        overdue = sum(1 for r in self.borrow_records if r.is_overdue() and r.return_date is None)
        print(f"Active Borrowed Books: {active_borrows}")
        print(f"Overdue Books: {overdue}")

    # ---------- Helpers ----------
    def _find_book(self, book_id):
        return next((b for b in self.books if b.book_id == book_id), None)

    def _find_member(self, member_id):
        return next((m for m in self.members if m.member_id == member_id), None)


# ---------- Main Menu ----------
def main():
    library = Library()

    while True:
        print("\n=========  Library Management System =========")
        print("1. Display All Books")
        print("2. Display Available Books")
        print("3. Display All Members")
        print("4. Search Books")
        print("5. Borrow a Book")
        print("6. Return a Book")
        print("7. View Member's Borrowed Books")
        print("8. View Overdue Books")
        print("9. Library Report")
        print("10. Add New Book")
        print("11. Register New Member")
        print("12. Delete Member")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            library.display_all_books()
        elif choice == "2":
            library.display_available_books()
        elif choice == "3":
            library.display_members()
        elif choice == "4":
            keyword = input("Enter title or author: ")
            library.search_book(keyword)
        elif choice == "5":
            try:
                m_id = int(input("Enter Member ID: "))
                b_id = int(input("Enter Book ID: "))
                library.borrow_book(m_id, b_id)
            except ValueError:
                print(" Invalid input.")
        elif choice == "6":
            try:
                m_id = int(input("Enter Member ID: "))
                b_id = int(input("Enter Book ID: "))
                library.return_book(m_id, b_id)
            except ValueError:
                print(" Invalid input.")
        elif choice == "7":
            m_id = int(input("Enter Member ID: "))
            library.view_member_borrowed_books(m_id)
        elif choice == "8":
            library.view_overdue_books()
        elif choice == "9":
            library.library_report()
        elif choice == "10":
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            copies = int(input("Enter total copies: "))
            library.add_book(title, author, copies)
        elif choice == "11":
            name = input("Enter member name: ")
            library.add_member(name)
        elif choice == "12":
            m_id = int(input("Enter Member ID to delete: "))
            library.delete_member(m_id)
        elif choice == "0":
            print("\n Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice, try again.")


if __name__ == "__main__":
    main()
