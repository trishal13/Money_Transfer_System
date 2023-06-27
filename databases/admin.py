from django.contrib import admin

from databases.models import Users, Payments, MESSAGES, Queries
# Register your models here.

class Databases_Users_Admin(admin.ModelAdmin):
    list_display=('id','Name','Aadhar','Mobile','Email','Date_Of_Birth','Account_Number','IFSC','Bank_Name','User_ID','Password','MPIN','Status','Balance','Unique_Key','Active_Status')
    search_fields=('id','Name','Aadhar','Mobile','Email','Date_Of_Birth','Account_Number','IFSC','Bank_Name','User_ID','Password','MPIN','Status','Balance','Unique_Key','Active_Status')

class Databases_Payments_Admin(admin.ModelAdmin):
    list_display=('id','Sender','Reciever','Amount','Date_time','Reference_Number','Payment_Status')
    search_fields=('id','Sender','Reciever','Amount','Date_time','Reference_Number','Payment_Status')

class Databases_Messages_Admin(admin.ModelAdmin):
    list_display=('id','From','To','Message','Date_time')
    search_fields=('id','From','To','Message','Date_time')

class Databases_Queries_Admin(admin.ModelAdmin):
    list_display=('id','From','Query','Date_time','Query_Status')
    search_fields=('id','From','Query','Date_time','Query_Status')

admin.site.register(Users,Databases_Users_Admin)
admin.site.register(Payments,Databases_Payments_Admin)
admin.site.register(MESSAGES,Databases_Messages_Admin)
admin.site.register(Queries,Databases_Queries_Admin)
