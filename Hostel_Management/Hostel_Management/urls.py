"""Hostel_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('user_reg/',views.user_register),
    path('hosteller_reg/',views.guest_register),
    path('log/',views.log),
    path('user_home/',views.user_index),
    path('parent_home/',views.parent_index),
    path('admin_home/',views.admin_index),
    path('hostel_home/',views.hostel_index),
    path('add_rooms/',views.add_rooms),
    path('add_blocks/',views.add_blocks),
    path('add_events/',views.add_events),
    path('udp/',views.udp),
    path('delete_block/',views.delete_block),
    path('view_room/',views.view_room),
    path('view_event/',views.view_event),
    path('add_mezz_details/',views.add_mezz_details),
    path('view_users/',views.view_users),
    path('delete_user/',views.delete_user),
    path('user_view_blocks/',views.user_view_blocks),
    path('user_view_room/',views.user_view_room),
    path('view_more/',views.view_more),
    path('view_students/',views.view_students),

    path('delete_room/',views.delete_room),
    path('view_booking/',views.view_booking),
    path('update_bookings/',views.update_bookings),
    path('add_hosteller/',views.add_hosteller),
    path('adm_view_hosteller/',views.adm_view_hosteller),
    path('add_attendance/',views.add_attendance),
    path('view_mess_details/',views.view_mess_details),
    path('user_view_events/',views.user_view_events),
    path('user_profile/',views.user_profile),
    path('my_attendance/',views.my_attendance),
    path('guest_view_event/',views.guest_view_event),
    path('guest_view_room/',views.guest_view_room),
    path('guest_view_more/',views.guest_view_more),
    path('guest_view_bookings/',views.guest_view_bookings),
    path('guest_add_feed/',views.guest_add_feed),
    path('user_add_feed/',views.user_add_feed),
    path('user_view_bookings/',views.user_view_bookings),
    path('make_payment/',views.make_payment),
    path('user_apply_leave/',views.user_apply_leave),
    path('adm_view_leave/',views.adm_view_leave),
    path('leave_status/',views.leave_status),
    path('user_leave_request/',views.user_leave_request),
    path('delete_mess_food/',views.delete_mess_food),
    path('update_mess_details/',views.update_mess_details),
    path('deleteEvent/',views.deleteEvent),
    path('update_Event/',views.update_Event),
    path('adm_view_feedback/',views.adm_view_feedback),
    path('delete_feed/',views.delete_feed),
    path('guest_payment/',views.guest_payment),
    path('add_fees_structure/',views.add_fees_structure),
    path('modify_fees/',views.modify_fees),
    path('assign_student_to_room/',views.assign_student_to_room),
    path('view_attendance/',views.view_attendance),
    path('parent_view_events/',views.parent_view_events),
    path('p_view_att/',views.p_view_att),
    path('add_complaint/',views.add_complaint),
    path('stu_view_mess_details/',views.stu_view_mess_details),
    # path('add_food_count/',views.add_food_count),
    path('dpp/',views.dpp),
    path('view_meal_counts/',views.view_meal_counts),
    path('payment/',views.payment),
    path('add_rentfee/',views.add_rentfee),
    path('user_fee_structure/',views.user_fee_structure),
    path('student_addpayment/',views.student_addpayment),
    path('parentview_fee_structure/',views.parentview_fee_structure), 
    path('all_feepayments/',views.all_feepayments), 
]
