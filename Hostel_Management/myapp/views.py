from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")

def log(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        user = authenticate(username=email, password=passw)
        print("Authentication ", user)
        if user is not None:
            print(user)
            login(request, user)
            if user.userType == "Administrator":
                return HttpResponse(
                    "<script>alert('Login As Admin'); window.location='/admin_home'</script>"
                )
            elif user.userType == "Student":
                id = user.id
                email = user.username
                userType = user.userType
                request.session["uid"] = id
                request.session["type"] = userType
                request.session["email"] = email
                return HttpResponse(
                    "<script>alert('Login As Student'); window.location='/user_home'</script>"
                )

            # elif user.userType == "Guest":
            #     id = user.id
            #     email = user.username
            #     userType = user.userType
            #     request.session["uid"] = id
            #     request.session["type"] = userType
            #     request.session["email"] = email
            #     return HttpResponse(
            #         "<script>alert('Login as Hosteller'); window.location='/hostel_home'</script>"
            #     )
            elif user.userType == "Parent":
                id = user.id
                email = user.username
                userType = user.userType
                request.session["uid"] = id
                print(id)
                request.session["type"] = userType
                request.session["email"] = email
                return HttpResponse(
                    "<script>alert('Login as Parent'); window.location='/parent_home'</script>"
                )

            else:
                return HttpResponse(
                    "<script>alert('Type Not Specified'); window.location='/log'</script>"
                )

        else:
            return HttpResponse(
                "<script>alert('Invalid Credentials'); window.location='/log'</script>"
            )
    return render(request, "login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("student_name")
        email = request.POST.get("student_email")
        mobile_number = request.POST.get("phone")
        password = request.POST.get("password")
        parentna = request.POST.get("parent_name")
        parentphn = request.POST.get("parent_phone")
        address = request.POST.get("address")
        image = request.FILES.get("image")
        if Login.objects.filter(username=email).exists():
            return HttpResponse(
                "<script>alert('Email already exists'); window.location='/user_reg'</script>"
            )
        else:
            student_user = Login.objects.create_user(
                username=email, 
                password=password,
                viewPass=password,
                email=email,
                first_name=username, 
                is_active=True,
                userType="Student",  
            )
            student_user.save()
            parent_user = Login.objects.create_user(
                username=parentna, 
                password=parentna+"123",  
                viewPass=parentna+"123",
                email=email,  
                first_name=parentna, 
                is_active=True,
                userType="Parent", 
            )
            parent_user.save()
            student_info = UserReg.objects.create(
                name=username,
                email=email,
                phone=mobile_number,
                address=address,
                loginid=student_user,  
                parent_name=parentna,
                parent_phone=parentphn, 
            )
            parent = ParentReg.objects.create(
                p_name=parentna,
                p_phone=parentphn,
                loginid=parent_user, userid=student_info,
            )
            parent.save()
            if image:
                student_info.image = image 
                student_info.save()
            return HttpResponse(
                "<script>alert('Successfully Registered'); window.location='/log'</script>"
            )
    return render(request, "Admin/add_students.html")


def guest_register(request):
    if request.method == "POST":
        hostelname = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        image = request.FILES["image"]
        if Login.objects.filter(username=email).exists():
            return HttpResponse(
                "<script>alert('Email already exists'); window.location='/hosteller_reg'</script>"
            )
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                viewPass=password,
                email=email,
                first_name=hostelname,
                is_active=1,
                userType="Guest",
            )
            new_user.save()
            if image:
                hostel_info = Hosteller_reg.objects.create(
                    name=hostelname,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    image=image,
                    loginid=new_user,
                )
                hostel_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
            else:
                hostel_info = Hosteller_reg.objects.create(
                    name=hostelname,
                    email=email,
                    phone=mobile_number,
                    address=address,
                    loginid=new_user,
                )
                hostel_info.save()
                return HttpResponse(
                    "<script>alert('Successfully Registered'); window.location='/log'</script>"
                )
    return render(request, "hostel_reg.html")


def user_index(request):
    return render(request, "Student/index.html")


def admin_index(request):
    return render(request, "Admin/index.html")


def hostel_index(request):
    return render(request, "Guest/index.html")

def parent_index(request):
    return render(request, "Parent/index.html")


def add_rooms(request):
    block = request.GET.get("bid")
    Bid = Blocks.objects.get(id=block)
    # view =Blocks.objects.filter(id=block)
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        adults = request.POST.get("adults")
        size = request.POST.get("size")
        rent_type = request.POST.get("rent_type")
        room_no = request.POST.get("room_no")
        images = request.FILES.getlist(
            "images"
        )  # Adjusted to getlist to handle multiple files
        description = request.POST.get("description")

        print("No IMAGES ", images)

        # Create the room instance but don't commit to database yet
        if images:
            room = Rooms(
                name=name,
                price=price,
                room_no=room_no,
                image=images[0],
                image2=images[1],
                image3=images[2],
                description=description,
                no_of_adults=adults,
                size=size,
                type=rent_type,
                block=Bid,
            )
            room.save()
            return HttpResponse(
                f"<script>alert('Successfully Added'); window.location='/add_rooms?bid={block}'</script>"
            )

    return render(request, "Admin/add_rooms.html", {"block": Bid})


def add_blocks(request):
    blocks = Blocks.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        block_no = request.POST.get("block_no")
        no_of_rooms = request.POST.get("no_of_rooms")
        images = request.FILES["images"]  # Adjusted to getlist to handle multiple files
        description = request.POST.get("description")

        # Create the block instance but don't commit to database yet
        block = Blocks(
            name=name,
            block_no=block_no,
            no_of_rooms=no_of_rooms,
            image=images,
            description=description,
        )
        block.save()  # Save the block to get an ID
    return render(request, "Admin/add_block.html", {"blocks": blocks})


def udp(request):
    change = Login.objects.filter(id=5,is_active=1)
    return HttpResponse("Success")


def delete_block(request):
    return HttpResponse("<scripts>alert('Deleted');window.location='/add_blocks'")


def view_room(request):
    view_room = Rooms.objects.all()

    return render(request, "Admin/view_rooms.html", {"view_room": view_room})


def add_events(request):
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        start_time = request.POST.get("stime")
        end_time = request.POST.get("etime")
        description = request.POST.get("description")
        images = request.FILES["image"]

        # Create the event instance but don't commit to database yet
        event = Events(
            name=name,
            date=date,
            image=images,
            start_time=start_time,
            end_time=end_time,
            description=description,
        )
        event.save()
        return HttpResponse(
            f"<script>alert('Event successfully added'); window.location='/add_events'</script>"
        )

    return render(request, "Admin/add_events.html")


def add_fees_structure(request):
    view = Fees_structure.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("price")

        event = Fees_structure(
            desc=name,
            price=amount,
        )
        event.save()
        return HttpResponse(
            f"<script>alert('New Fees Added'); window.location='/add_fees_structure'</script>"
        )

    return render(request, "Admin/add_fees_structure.html", {"view": view})


def view_event(request):
    events = Events.objects.all()
    return render(request, "Admin/view_event.html", {"events": events})


def add_mezz_details(request):
    if request.method == "POST":
        day = request.POST.get("day")
        breakfast = request.POST.get("BreakFast")
        lunch = request.POST.get("Lunch")
        dinner = request.POST.get("Dinner")

        # Create the event instance but don't commit to database yet
        event = Mess_food(
            day=day,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
        )
        event.save()  # Save the event to get an ID
        return HttpResponse(
            f"<script>alert('Mess details added'); window.location='/add_mezz_details'</script>"
        )

    return render(request, "Admin/add_mezz_details.html")


def view_users(request):
    users = UserReg.objects.all()
    return render(request, "Admin/view_users.html", {"users": users})


def delete_user(request):
    uid = request.GET.get("uid")
    print("uid", uid)
    delet=Login.objects.filter(id=uid).delete()
    # print(delet,"888888888888888888888888888")

    return HttpResponse("<script>alert('Deleted!'); window.location='/view_users'</script>")


def view_students(request):
    users = UserReg.objects.all()
    return render(request, "Student/viewroomhoste.html", {"users": users})


def user_view_blocks(request):
    uid = request.session["uid"]
    userid = UserReg.objects.get(loginid=uid).id


    print("99999999999",userid)


    
    user_login = UserReg.objects.get(id=userid)  # Fetch user login object
    print(user_login)

    # Check if the user is already a hosteller
    if Hosteller.objects.filter(uid_id=userid).exists():
        return HttpResponse("<script>alert('You are already assigned to a hostel!'); window.location='/user_home'</script>")

    # If not a hosteller, fetch available blocks
    blocks = Blocks.objects.all()
    return render(request, "Student/view_blocks.html", {"blocks": blocks})

    # except Login.DoesNotExist:
    #     return HttpResponse("User not found", status=404)


def user_view_room(request):
    bid = request.GET.get("bid")  # Store the bid value
    print("uuuuuuuuuuuuuuuuuuuuuuuuuu")
    if bid:  # Ensure bid is not None
        view_room = Rooms.objects.filter(type="Monthly Rent", block__id=bid)
    else:
        view_room = Rooms.objects.filter(type="Monthly Rent")  # Default case

    return render(request, "Student/view_rooms.html", {"view_room": view_room})



from datetime import datetime


from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from .models import UserReg, Rooms, Room_booking, Mess_food, Fees_structure

def view_more(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    rid = request.GET.get("rid")
    Rid = Rooms.objects.get(id=rid)
    view = Rooms.objects.filter(id=rid)

    food = Mess_food.objects.all()
    fees = Fees_structure.objects.all()

    # Count existing bookings for this room
    existing_bookings = Room_booking.objects.filter(rid=Rid).count()
    print(existing_bookings)
    # Get max allowed adults for the room
    max_adults = int(Rid.no_of_adults) if Rid.no_of_adults else 0
    print(max_adults)

    if request.POST:
        if existing_bookings >= max_adults:
            return HttpResponse(
                f"<script>alert('Room is fully booked!');window.location='/view_more?rid={rid}'</script>"
            )

        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        price = request.POST.get("price")

        check_out_date = datetime.strptime(check_out, "%m/%d/%Y")
        formatted_check_out = check_out_date.strftime("%Y-%m-%d")

        check_in_date = datetime.strptime(check_in, "%m/%d/%Y")
        formatted_check_in = check_in_date.strftime("%Y-%m-%d")

        date_diff = check_out_date - check_in_date
        days_between = date_diff.days

        amount = int(days_between) * int(price)

        insert = Room_booking.objects.create(
            check_in=formatted_check_in,
            check_out=formatted_check_out,
            uid=Uid,
            rid=Rid,
            amount=price,
            type="Monthly",
        )
        insert.save()

        return HttpResponse(
            f"<script>alert('Booked Successfully');window.location='/view_more?rid={rid}'</script>"
        )

    return render(request, "Student/view_more.html", {"view": view, "food": food, "fees": fees})



def make_payment(request):
    bid = request.GET.get("bid")
    if request.method == "POST":
        Bid = Room_booking.objects.filter(id=bid).update(pay_status="Paid")
        return HttpResponse(
            "<script>alert('Payment Success');window.location='/user_view_bookings'</script>"
        )

    return render(request, "Student/payment.html")


def delete_room(request):
    rid = request.GET.get("rid")
    delete_roo = Rooms.objects.filter(id=rid).delete()
    return HttpResponse(
        f"<script>alert('Room Details Deleted');window.location='/view_room'</script>"
    )


def view_booking(request):
    bookings = Room_booking.objects.filter(type="Daily")
    bookings2 = Room_booking.objects.filter(type="Monthly")
    return render(
        request, "Admin/view_bookings.html", {"Daily": bookings, "Monthly": bookings2}
    )


def update_bookings(request):
    bid = request.GET.get("bid")
    status = request.GET.get("status")

    if status == "approve":
        bookings = Room_booking.objects.filter(id=bid).update(status="approved")
        return HttpResponse(
            f"<script>alert('Booking Details Updated');window.location='/view_booking'</script>"
        )

    elif status == "decline":
        bookings = Room_booking.objects.filter(id=bid).update(status="declined")
        return HttpResponse(
            f"<script>alert('Booking Details Updated');window.location='/view_booking'</script>"
        )


def add_hosteller(request):
    uid = request.GET.get("uid")
    bid = request.GET.get("bid")
    Uid = UserReg.objects.get(id=uid)
    Bid = Room_booking.objects.get(id=bid)

    insert = Hosteller.objects.create(uid=Uid, bid=Bid, status="Hosteller")
    insert.save()
    up = Room_booking.objects.filter(id=bid).update(status="Hosteller")

    return HttpResponse(
        f"<script>alert('Hosteller Added');window.location='/view_booking'</script>"
    )


def adm_view_hosteller(request):
    adm_view = Hosteller.objects.all()
    return render(request, "Admin/view_hosteller.html", {"view": adm_view})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Attendance, UserReg

def add_attendance(request):
    uid = request.GET.get("uid")
    Uid = get_object_or_404(UserReg, id=uid)  # Handle invalid user IDs

    if request.method == "POST":
        date = request.POST["date"]

        # Check if attendance already exists for this user on the selected date
        if Attendance.objects.filter(uid=Uid, date=date).exists():
            return HttpResponse(
                "<script>alert('Attendance already marked for this date!'); window.location = '/adm_view_hosteller'</script>"
            )

        # Insert new attendance record
        Attendance.objects.create(uid=Uid, date=date, status="Present")

        return HttpResponse(
            "<script>alert('Attendance Marked Successfully'); window.location = '/adm_view_hosteller'</script>"
        )

    return render(request, "Admin/add_attendance.html", {"uid": Uid})




def view_attendance(request):
    attendance_records = Attendance.objects.all().order_by('-date')  # Fetch all attendance records ordered by date
    print(attendance_records)
    return render(request, "Admin/view_attendance.html", {"attendance_records": attendance_records})


from django.shortcuts import render
from .models import Attendance, ParentReg

def p_view_att(request):
    # Get logged-in parent's session ID
    login_id = request.session.get("uid")
    print(login_id)
    dataid=ParentReg.objects.get(loginid=login_id).userid
    print(dataid)
    if not login_id:
        return render(request, "Parent/p_view_att.html", {"attendance_records": []})  # No session, return empty

    # Fetch parent record using login ID
    parent = ParentReg.objects.filter(loginid=login_id).first()

    if not parent or not parent.userid:
        return render(request, "Parent/p_view_att.html", {"attendance_records": []})  # No linked student

    # Filter attendance records by the associated student ID
    attendance_records = Attendance.objects.filter(uid=parent.userid).order_by('-date')

    return render(request, "Parent/p_view_att.html", {"attendance_records": attendance_records})



def view_mess_details(request):
    mess = Mess_food.objects.all()
    return render(request, "Admin/view_mess_details.html", {"view": mess})
# =======================================================================
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from datetime import datetime
from .models import Mess_food, UserReg, Food_count

def stu_view_mess_details(request):
    uid = request.session["uid"]
    user = UserReg.objects.get(loginid=uid)

    # Get start and end dates for the current week (Monday to Sunday)
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    # Check if user already added meal preferences for this week
    existing_entries = Food_count.objects.filter(uid=user, Date__range=[start_of_week, end_of_week]).exists()

    if existing_entries:
        return render(request, "Student/view_mess_details.html", {
            "mess_with_dates": [],
            "message": "You have already submitted your meal preferences for this week."
        })

    # Generate menu with dates starting from today
    mess = list(Mess_food.objects.all())
    mess_with_dates = [(today + timedelta(days=i), mess[i]) for i in range(len(mess))]

    if request.method == "POST":
        for i, mess_entry in enumerate(mess):
            messid = str(mess_entry.id)  # Convert ID to string for matching input names
            
            # ✅ Ensure the correct date starts from today
            date_value = today + timedelta(days=i)  

            # Check if an entry for this user and date already exists
            existing_entry = Food_count.objects.filter(uid=user, Date=date_value, messid=mess_entry).first()

            if existing_entry:
                # ✅ Update existing record
                existing_entry.Breakfast = "Off" if f"breakfast_{messid}" in request.POST else "On"
                existing_entry.Lunch = "Off" if f"lunch_{messid}" in request.POST else "On"
                existing_entry.Dinner = "Off" if f"dinner_{messid}" in request.POST else "On"
                existing_entry.save()
            else:
                # ✅ Insert new record starting from today
                Food_count.objects.create(
                    Date=date_value,
                    uid=user,
                    messid=mess_entry,
                    Breakfast="Off" if f"breakfast_{messid}" in request.POST else "On",
                    Lunch="Off" if f"lunch_{messid}" in request.POST else "On",
                    Dinner="Off" if f"dinner_{messid}" in request.POST else "On",
                )
            return redirect('/stu_view_mess_details')
    return render(request, "Student/view_mess_details.html", {"mess_with_dates": mess_with_dates})





# =======================================================================
from django.shortcuts import render
from django.utils.timezone import now
from .models import Fee_payment, UserReg

def payment(request):
    uid = request.session.get("uid")  # Get the user ID from session
    if not uid:
        return render(request, "error.html", {"message": "User not logged in"})

    user = UserReg.objects.get(loginid=uid)
    
    # Get the first day and last day of the current month
    today = now().date()
    first_day_of_month = today.replace(day=1)
    
    # Check if payment exists for this user in the current month
    existing_payment = Fee_payment.objects.filter(uid=user, date__gte=first_day_of_month).first()
    
    if existing_payment:
        return render(request, "payment_status.html", {"payment": existing_payment})
    
    # If no payment exists, show payment form
    return render(request, "Student/make_payment.html", {"user": user})

    
    

def add_food_count(request):
    if request.method == "POST":
        uid = request.session["uid"]
        user = UserReg.objects.get(loginid=uid)

        for key in request.POST:
            if key.startswith("messid"):
                messid = request.POST[key]
                mess = Mess_food.objects.get(id=messid)

                # Get meal preferences
                breakfast = request.POST.get(f"breakfast_{messid}", "On")
                lunch = request.POST.get(f"lunch_{messid}", "On")
                dinner = request.POST.get(f"dinner_{messid}", "On")

                # Save to the database
                Food_count.objects.create(
                    Date=now().date(),
                    uid=user,
                    messid=mess,
                    Breakfast=breakfast,
                    Lunch=lunch,
                    Dinner=dinner,
                )

        # return redirect("/stu_view_mess_details")  # Redirect after saving

    return render(request, "Student/view_mess_details.html")

def user_view_events(request):
    events = Events.objects.all()
    return render(request, "Student/view_event.html", {"events": events})
def parent_view_events(request):
    events = Events.objects.all()
    return render(request, "Parent/parent_view_events.html", {"events": events})


def user_profile(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        mobile_number = request.POST.get("mobile_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        image = request.FILES.get("image")

        if image:
            user_info = UserReg.objects.filter(loginid_id=uid).update(
                name=username,
                email=email,
                phone=mobile_number,
                address=address,
            )
            up_image = UserReg.objects.get(loginid=uid)
            up_image.image = image
            up_image.save()

            set_pass = Login.objects.get(id=uid)
            print("Passwored : ", set_pass)
            set_pass.set_password(password)
            set_pass.viewPass = password
            set_pass.save()

            return HttpResponse(
                "<script>alert('Profile Updated'); window.location='/user_profile'</script>"
            )
        else:
            user_inf = UserReg.objects.filter(loginid_id=uid).update(
                name=username,
                email=email,
                phone=mobile_number,
                address=address,
            )
            set_pass = Login.objects.get(id=uid)
            print("Passwored : ", set_pass)
            set_pass.password = password
            set_pass.viewPass = password
            set_pass.save()

            return HttpResponse(
                "<script>alert('Profile Updated'); window.location='/user_profile'</script>"
            )

    return render(request, "Student/profile.html", {"uid": Uid})


def my_attendance(request):
    uid = request.session.get("uid")  # Safely get uid from session
    print("User ID from session:", uid)

    if not uid:
        return HttpResponse("User not logged in", status=403)  # Handle missing session data

    try:
        Uid = UserReg.objects.get(loginid=uid)  # Get the user object
        view = Attendance.objects.filter(uid=Uid.id)  # Filter attendance records
    except UserReg.DoesNotExist:
        return HttpResponse("User not found", status=404)

    return render(request, "Student/view_attendance.html", {"att": view})


def guest_view_event(request):
    events = Events.objects.all()
    return render(request, "Student/view_event.html", {"events": events})


def guest_view_room(request):
    view_room = Rooms.objects.filter(type="Daily Rent")

    return render(request, "Guest/view_rooms.html", {"view_room": view_room})


def guest_view_more(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)

    rid = request.GET.get("rid")
    Rid = Rooms.objects.get(id=rid)
    view = Rooms.objects.filter(id=rid)

    food = Mess_food.objects.all()
    
    fees=Fees_structure.objects.all()

    if request.POST:
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        price = request.POST.get("price")
        print("Price   =       =      =", price)

        check_out_date = datetime.strptime(check_out, "%m/%d/%Y")
        formatted_check_out = check_out_date.strftime("%Y-%m-%d")

        check_in_date = datetime.strptime(check_in, "%m/%d/%Y")
        formatted_check_in = check_in_date.strftime("%Y-%m-%d")

        date_diff = check_out_date - check_in_date
        days_between = date_diff.days

        print(f"The difference between check-in and check-out is: {days_between} days")

        amount = int(days_between) * int(price)

        insert = Room_booking.objects.create(
            check_in=formatted_check_in,
            check_out=formatted_check_out,
            gid=Uid,
            rid=Rid,
            amount=amount,
            type="Daily",
        )
        insert.save()
        return HttpResponse(
            f"<script>alert('Booked Successfully');window.location='/guest_payment?rid={rid}'</script>"
        )

    return render(request, "Guest/view_more.html", {"view": view, "food": food,"fees":fees})


def guest_view_bookings(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)

    bookings = Room_booking.objects.filter(type="Daily", gid=Uid)
    print(bookings, "Bookings")
    return render(request, "Guest/guest_bookings.html", {"bookings": bookings})


def guest_add_feed(request):
    uid = request.session["uid"]
    Uid = Hosteller_reg.objects.get(loginid=uid)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        feed = Feedback.objects.create(
            type="Guest", gid=Uid, rating=rating, comment=comment
        )
        feed.save()
        return HttpResponse(
            "<script>alert('feedback Added');window.location='/guest_view_room'</script>"
        )
    return render(request, "Guest/add_feedback.html")


def user_add_feed(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("review")

        feed = Feedback.objects.create(
            type="User", uid=Uid, rating=rating, comment=comment
        )
        feed.save()
        return HttpResponse(
            "<script>alert('feedback Added');window.location='/guest_view_room'</script>"
        )

    return render(request, "Student/add_feedback.html")


def add_admin(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        new_user = Login.objects.create_user(
            username=email,
            password=passw,
            viewPass=passw,
            email=email,
            is_active=1,
            userType="User",
        )
    return render(request, "Admin/add_admin.html")


def user_view_bookings(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)

    bookings = Room_booking.objects.filter(type="Monthly", uid=Uid)
    print(bookings, "Bookings")
    return render(request, "Student/user_bookings.html", {"bookings": bookings})


def user_apply_leave(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    if request.method == "POST":

        fromdate = request.POST["fromdate"]
        todate = request.POST["todate"]
        no_of_days = request.POST["no_of_days"]
        reason = request.POST["reason"]

        leave = Leave.objects.create(
            uid=Uid,
            fromdate=fromdate,
            todate=todate,
            no_of_days=no_of_days,
            reason=reason,
        )
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Requested');window.location='/user_view_bookings'</script>"
        )

    return render(request, "Student/leave_page.html")


def adm_view_leave(request):
    view = Leave.objects.all()
    return render(request, "Admin/view_leave_requests.html", {"view": view})


def leave_status(request):
    lid = request.GET.get("lid")
    status = request.GET.get("status")

    if status == "approve":
        leave = Leave.objects.get(id=lid)
        leave.status = "Approved"
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Request Approved');window.location='/adm_view_leave'</script>"
        )
    elif status == "reject":
        leave = Leave.objects.get(id=lid)
        leave.status = "Rejected"
        leave.save()
        return HttpResponse(
            "<script>alert('Leave Request Rejected');window.location='/adm_view_leave'</script>"
        )
    elif status == "delete":
        leave = Leave.objects.get(id=lid)
        leave.delete()
        return HttpResponse(
            "<script>alert('Leave Request Deleted');window.location='/adm_view_leave'</script>"
        )


def user_leave_request(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    view = Leave.objects.filter(uid=Uid)
    return render(request, "Student/leave_page.html", {"view": view})


def update_mess_details(request):
    mid = request.GET.get("mid")
    view = Mess_food.objects.get(id=mid)
    if request.method == "POST":
        day = request.POST.get("day")
        breakfast = request.POST.get("BreakFast")
        lunch = request.POST.get("Lunch")
        dinner = request.POST.get("Dinner")

        # Create the event instance but don't commit to database yet
        event = Mess_food.objects.filter(id=mid).update(
            day=day,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
        )  # Save the event to get an ID
        return HttpResponse(
            f"<script>alert('Mess details updated'); window.location='/view_mess_details'</script>"
        )

    return render(request, "Admin/update_mess_details.html", {"view": view})


def delete_mess_food(request):
    mid = request.GET.get("mid")
    event = Mess_food.objects.filter(id=mid).delete()

    return HttpResponse(
        f"<script>alert('Mess details Deleted'); window.location='/view_mess_details'</script>"
    )


def deleteEvent(request):
    eid = request.GET.get("eid")
    event = Events.objects.filter(id=eid).delete()

    return HttpResponse(
        f"<script>alert('Event Deleted'); window.location='/view_event'</script>"
    )


def update_Event(request):
    eid = request.GET.get("eid")
    view = Events.objects.get(id=eid)
    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")
        start_time = request.POST.get("stime")
        end_time = request.POST.get("etime")
        description = request.POST.get("description")
        images = request.FILES["image"]

        # Create the event instance but don't commit to database yet
        if images:
            event = Events.objects.filter(id=eid).update(
                name=name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
            up_image = Events.objects.get(id=eid)
            up_image.image = images
            up_image.save()

            return HttpResponse(
                f"<script>alert('Event Updated'); window.location='/view_event'</script>"
            )
        else:
            event = Events.objects.filter(id=eid).update(
                name=name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
            )
            return HttpResponse(
                f"<script>alert('Event Updated'); window.location='/view_event'</script>"
            )
    return render(request, "Admin/update_event.html", {"i": view})


def adm_view_feedback(request):
    view = Feedback.objects.all()
    return render(request, "Admin/view_feedback.html", {"view": view})


def delete_feed(request):
    fid = request.GET.get("fid")
    dele = Feedback.objects.filter(id=fid).delete()
    return HttpResponse(
        f"<script>alert('Feedback Deleted'); window.location='/adm_view_feedback'</script>"
    )


def guest_payment(request):
    bid = request.GET.get("bid")
    if request.method == "POST":
        Bid = Room_booking.objects.filter(id=bid).update(pay_status="Paid")
        return HttpResponse(
            "<script>alert('Payment Success');window.location='/guest_view_room'</script>"
        )
    return render(request, "Guest/payment.html")


def modify_fees(request):
    fid = request.GET.get("fid")
    status = request.GET.get("status")
    
    view=Fees_structure.objects.get(id=fid)
    print("Modified",view)
    if status == "update":
        if request.POST:
            name = request.POST.get("name")
            amount = request.POST.get("price")

            event = Fees_structure.objects.filter(id=fid).update(
                desc=name,
                price=amount,
            )
            event.save()
            return HttpResponse(
                f"<script>alert('New Fees Updated'); window.location='/add_fees_structure'</script>"
            )
            
    else:
        dele=Fees_structure.objects.filter(id=fid).delete()
        return HttpResponse(
            f"<script>alert('Fees Deleted'); window.location='/add_fees_structure'</script>"
        )
        
    return render(request, "Admin/modify_fees.html",{"view": view})
# =====================================================


def assign_student_to_room(request):
    if request.method == "POST":
        room_id = request.POST.get("room")
        student_id = request.POST.get("student")

        try:
            room = Rooms.objects.get(id=room_id)
            student = Hosteller_reg.objects.get(id=student_id)

            # Check if the room already has 3 students
            if RoomMembers.objects.filter(room=room).count() >= 3:
                return HttpResponse("<script>alert('This room is already full!'); window.location='/assign_room'</script>")

            # Assign student to room
            RoomMembers.objects.create(room=room, student=student)
            return HttpResponse("<script>alert('Student assigned successfully!'); window.location='/assign_room'</script>")

        except Rooms.DoesNotExist:
            return HttpResponse("<script>alert('Selected room does not exist!'); window.location='/assign_room'</script>")
        except Hosteller_reg.DoesNotExist:
            return HttpResponse("<script>alert('Selected student does not exist!'); window.location='/assign_room'</script>")

    # Fetch available rooms and students
    rooms = Rooms.objects.all()
    assigned_students = RoomMembers.objects.values_list('student', flat=True)
    students = Hosteller_reg.objects.exclude(id__in=assigned_students)

    return render(request, "Admin/assign_room.html", {"rooms": rooms, "students": students})

from django.shortcuts import render, redirect
from .models import Complaint
from django.utils import timezone

def add_complaint(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        student_id = request.session.get("uid")  # Get student ID from session

        if student_id and subject and message:
            Complaint.objects.create(
                student_id=student_id,
                subject=subject,
                message=message,
                date_submitted=timezone.now(),
                status="Pending"
            )
            return redirect("view_complaints")  # Redirect after submission

    return render(request, "Student/add_complaint.html")

from django.shortcuts import render
from django.utils.timezone import now
from .models import Food_count

def view_meal_counts(request):
    # Get the selected date from the request (default to today)
    selected_date = request.GET.get("date", now().date())

    # Count the number of users who opted out of each meal
    breakfast_count = Food_count.objects.filter(Date=selected_date, Breakfast="Off").count()
    lunch_count = Food_count.objects.filter(Date=selected_date, Lunch="Off").count()
    dinner_count = Food_count.objects.filter(Date=selected_date, Dinner="Off").count()

    return render(request, "Admin/meal_counts.html", {
        "selected_date": selected_date,
        "breakfast_count": breakfast_count,
        "lunch_count": lunch_count,
        "dinner_count": dinner_count,
    })

def dpp(request):
    Fee_payment.objects.all().delete()
    return render(request, "login.html")


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *

def add_rentfee(request):
    uid = request.GET.get("uid")
    Uid = get_object_or_404(UserReg, id=uid)
    if request.method == "POST":
        month = request.POST["month"]
        rent = request.POST["rent_fee"]
        additional = request.POST["additional_fee"]
        if Fee_payment.objects.filter(uid=Uid, month=month).exists():
            return HttpResponse("<script>alert('Rent Fee Already Added For This Month!'); window.location='/adm_view_hosteller'</script>")
        Fee_payment.objects.create(
            uid=Uid,
            Rentfee=rent,
            addt_fee=additional,
            month=month,
            total=int(rent) + int(additional)
        )
        return HttpResponse("<script>alert('Rent Fee Added Successfully'); window.location='/adm_view_hosteller'</script>")
    return render(request, "Admin/add_rentfee.html", {"uid": Uid})




def user_fee_structure(request):
    uid = request.session["uid"]
    Uid = UserReg.objects.get(loginid=uid)
    view = Fee_payment.objects.filter(uid=Uid)
    return render(request, "Student/view_feestructure.html", {"fee": view})



from django.shortcuts import render, HttpResponse
from .models import Fee_payment

def student_addpayment(request):
    # ✅ Get the payment details from the URL
    id = request.GET.get("id")
    total_amount = request.GET.get("total_amount")
    
    # ✅ Fetch the student fee record
    student_fee = Fee_payment.objects.get(id=id)
    
    # ✅ Handle if "Amount" is None (first time payment)
    if student_fee.Amount is None:
        student_fee.Amount = 0
    
    # ✅ Prevent if the student has already paid the full amount
    if student_fee.Amount >= int(total_amount):
        return HttpResponse(
            "<script>alert('You have already paid the full amount.');window.location='/user_fee_structure'</script>"
        )
    
    # ✅ Handle POST request (when student makes payment)
    if request.method == "POST":
        # ✅ Amount entered by student in form
        amount = int(request.POST["amount"])
        
        # ✅ Calculate the remaining balance
        remaining_amount = int(total_amount) - student_fee.Amount
        
        # ✅ Prevent overpayment
        if amount > remaining_amount:
            return HttpResponse(
                f"<script>alert('You cannot pay more than the remaining amount of {remaining_amount}₹.');window.location='/user_fee_structure'</script>"
            )
        
        # ✅ Add the paid amount to the existing Amount
        student_fee.Amount += amount
        
        # ✅ Calculate Remaining Balance
        rem_amt = int(total_amount) - student_fee.Amount
        
        # ✅ Store the Remaining Balance (THIS IS WHERE I INSERT IT IN DATABASE)
        student_fee.rem_amt = rem_amt
        
        # ✅ Check if the full payment has been done
        if student_fee.Amount >= int(total_amount):
            student_fee.pay_status = "Paid"
        else:
            student_fee.pay_status = "Partially Paid"
        
        # ✅ Save the payment to the database
        student_fee.save()
        
        # ✅ Success Message after Payment
        return HttpResponse(
            f"<script>alert('Payment of {amount}₹ successful. Remaining balance is {rem_amt}₹');window.location='/user_fee_structure'</script>"
        )
    
    # ✅ Pass Data to Template
    context = {
        "student_fee": student_fee,
        "remaining_amount": int(total_amount) - student_fee.Amount,
        "total_amount": total_amount
    }
    
    # ✅ Render Payment Page
    return render(request, "Student/add_fee_payment.html", context)




def parentview_fee_structure(request):
    login_id = request.session.get("uid")
    print(login_id)
    dataid=ParentReg.objects.get(loginid=login_id).userid
    print(dataid)
    view = Fee_payment.objects.filter(uid=dataid)
    return render(request, "Parent/parent_fee_structure.html", {"fee": view})



def all_feepayments(request):
    view = Fee_payment.objects.all()
    return render(request, "Admin/fee_payments.html", {"fee": view})



