from django.shortcuts import render, redirect
from materiallist.models import Materials,Transactions
from materiallist.forms import TransactionForm,MaterialsForm
from materiallist.serializers import Transactserializers
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime

from django.utils.safestring import mark_safe

# Create your views here.
def home_view(request):
    return HttpResponseRedirect("/master_page")


def material_List(request):

    material = Materials.objects.all()
    return render(request, "material_list.html", {"material": material})


def master_Page(request):
    material = Materials.objects.all()
    return render(request, "master_page.html", {"material": material})


def create_Material(request):

    # import pdb;pdb.set_trace()
    material = Materials.objects.values_list("Material_Code", flat=True)
    materials = list(material)
    if request.method == "POST":
        form = MaterialsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            form.instance.Material_Code = request.POST["Material_Code"]
            form.instance.Material_Descriptions = request.POST["Material_Name"]
            form.instance.Material_Location = request.POST["Material_Location"]
            form.instance.Unit_of_Measurement = request.POST["Unit_of_Measurement"]
            form.instance.Maximum_Level = request.POST["Maximum_Level"]
            form.instance.Minimum_Level = request.POST["Minimum_Level"]
            form.instance.Re_order_Level = request.POST["Re_order_Level"]
            form.instance.Quantity = request.POST["Quantity"]

            form.save()

            return HttpResponseRedirect("/material_list")

        else:
            print(form.errors)
    else:
        form = MaterialsForm()
        return render(
            request, "create_material.html", {"form": form, "materials": materials}
        )


def material_Update(request, id):

    material = Materials.objects.get(id=id)

    form = MaterialsForm(
        initial={
            "Material_Code": material.Material_Code,
            "Material_Name": material.Material_Name,
            "Material_Location": material.Material_Location,
            "Unit_of_Measurement": material.Unit_of_Measurement,
            "Maximum_Level": material.Maximum_Level,
            "Minimum_Level": material.Minimum_Level,
            "Re_order_Level": material.Re_order_Level,
            "Quantity": material.Quantity,
        }
    )

    if request.method == "POST":
        form = MaterialsForm(request.POST, instance=material)

        if form.is_valid():

            try:
                form.save()
                return HttpResponseRedirect("/material_list")

            except Exception as e:
                return Response(status=404)

    else:

        return render(
            request,
            "create_material.html",
            {"form": form, "mat_id": material.id, "material": material},
        )


def material_View(request, id):
    # import pdb;pdb.set_trace()
    material = Materials.objects.get(id=id)
    transaction = Transactions.objects.filter(Material_Name_id=material.id)

    return render(
        request, "main_list.html", {"material": material, "transaction": transaction}
    )

"""this function is used for  view the trasaction list """
def transact_list(request):
    # pylint: disable=no-member
    transact = Transactions.objects.all()
    context = {"transact": transact}
    return render(request, "transact_list.html", context)

""" this function is used for create a new transaction"""
def create_method(request):
    # import pdb; pdb.set_trace()
    doc_unique = Transactions.objects.values_list("Document_Number", flat=True)
    doc_unique = list(doc_unique)
    # pylint: disable=no-member
    material_name = Materials.objects.all()
    # results=MaterialsInventory.objects.all()
    mydict = {}

    for data in material_name:
        mydict[data.Material_Name] = data.Quantity

    # import pdb;pdb.set_trace()
    if request.method == "POST":
        # pylint: disable=no-member
        get_selected_material_id = (
            Materials.objects.filter(Material_Name=request.POST.get("Material_Names"))
            .values_list("id", flat=True)
            .first()
        )

        saverecord = Transactions()# pylint: disable=no-member
        saverecord.Transaction_Type = request.POST.get("Transaction_Type")
        print(saverecord.Transaction_Type)

        if request.POST.get("Received_From") == "":
            saverecord.Received_From = None
        else:
            saverecord.Received_From = request.POST.get("Received_From")
        if request.POST.get("Number_Of_Received") == "":
            saverecord.Number_Of_Received = None
        else:
            saverecord.Number_Of_Received = request.POST.get("Number_Of_Received")

        if request.POST.get("Issue_To") == "":
            saverecord.Issue_To = None
        else:

            saverecord.Issue_To = request.POST.get("Issue_To")

        if request.POST.get("Number_Of_Issued") == "":
            saverecord.Number_Of_Issued = None
        else:
            no_of_issued = request.POST.get("Number_Of_Issued")
            saverecord.Number_Of_Issued = int(no_of_issued)
        saverecord.Balance = request.POST.get("Balances")
        print(saverecord.Balance)
        saverecord.Material_Name_id = get_selected_material_id
        Date = request.POST.get("Date")
        saverecord.Date = datetime.strptime(Date, "%m/%d/%Y").strftime('%Y-%m-%d')
        saverecord.Document_Number = request.POST.get("Document_Number")
        Verification_Date = request.POST.get("Verification_Date")
        saverecord.Verification_Date = datetime.strptime(Verification_Date, "%m/%d/%Y").strftime('%Y-%m-%d')
        saverecord.Verified_By = request.POST.get("Verified_By")
        saverecord.save()

        return redirect("/transact_list")

    
    return render(
        request,
        "create_transact.html",
        {
            "mat_name": material_name,
            "TransactInventory": mydict,
            "doc_id": doc_unique,
        },
    )

""" this function is used for update transaction list """
def update_method(request, id):
    # pylint: disable=no-member
    transact = Transactions.objects.get(id=id)
    form = TransactionForm(instance=transact)
    # pylint: disable=no-member
    material_id = Transactions.objects.filter(id=id)[0].Material_Name_id
    selected_material_id = Materials.objects.filter(id=material_id)[0].Material_Name

    if request.method == "POST":

        if request.POST["Transaction_Type"] == "Received From":
            received_from = request.POST.getlist("Received_From")[0]
            number_of_received = request.POST.getlist("Number_Of_Received")[0]
            issue_to = None
            number_of_issued = None

        else:
            issue_to = request.POST.getlist("Issue_To")[0]
            number_of_issued = request.POST.getlist("Number_Of_Issued")[0]
            received_from = None
            number_of_received = None
        
        Date_field = request.POST["Date"] 
        convert_date_field = datetime.strptime(Date_field, "%m/%d/%Y").strftime('%Y-%m-%d')
        Verify_Date = request.POST["Verification_Date"]
        covert_verify_date = datetime.strptime(Verify_Date, "%m/%d/%Y").strftime('%Y-%m-%d')

        form = TransactionForm(request.POST, instance=transact)
        # pylint: disable=no-member
        material_id = Materials.objects.filter(Material_Name=selected_material_id)[0].id
        # pylint: disable=no-member
        Transactions.objects.filter(
            Document_Number=request.POST["Document_Number"]
        ).update(
            Transaction_Type = request.POST["Transaction_Type"],
            Received_From = received_from,
            Number_Of_Received = number_of_received,
            Issue_To = issue_to,
            Number_Of_Issued = number_of_issued,
            Balance = request.POST["Balance"],
            Material_Name_id = material_id,
            Date = convert_date_field,
            Verification_Date = covert_verify_date,
            Verified_By = request.POST["Verified_By"],
        )
        return redirect("/transact_list")
    
    mat = Transactserializers(transact).data
    context = {
        "form": form,
        "id": material_id,
        "mat": mat,
        "selected_material_id": selected_material_id,
    }
    return render(request, "create_transact.html", context)