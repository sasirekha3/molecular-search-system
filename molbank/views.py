from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import molbank, status
from .forms import addForm, advancedSearchForm, loginForm, simpleSearchForm, rangeSearchForm
from django.contrib import messages
from django.contrib.auth.models import User,Permission
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.core.mail import send_mail
from django.contrib.auth.backends import *
from django.template.defaulttags import register
from indigo import *
import psycopg2
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from openpyxl import Workbook
from django.conf import settings
from django.core.files.storage import FileSystemStorage,Storage
from collections import namedtuple
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

#just for testing
import pprint
def sample_func(request):
	print("hello world!! this is a sample functions")
	pprint.pprint(request.user.get_all_permissions())
	perm = {}
	if request.user.has_perm('molbank.c_add'):
		print("has perm add")
		perm['add']=True
	if request.user.has_perm('molbank.c_delete'):
		print("has perm delete")
		perm['delete']=True
	if request.user.has_perm('molbank.c_view'):
		print("has perm view")
		perm['view']=True



@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter
def index(List, i):
	return List[int(i)]

def namedtuplefetchall(cursor):
	"Return all rows from a cursor as a namedtuple"
	desc = cursor.description
	nt_result = namedtuple('Result', [col[0] for col in desc])
	return [nt_result(*row) for row in cursor.fetchall()]

@login_required()
def index(request):
	print("hi")
	conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
	cur = conn.cursor()
	cur.execute('SET search_path TO bingo')
	cur.execute('select sample_code, \"Smiles\" from molbank_allplates')
	# molecule_list = molbank.objects.raw('select sample_code, \"Smiles\" from molbank_allplates')
	molecule_list = namedtuplefetchall(cur)
	# molecule_list = molbank.objects.raw('select * from molbank_molbank')
	cml_dict = {}
	indigo = Indigo()
	for mol in molecule_list:
		mol_obj = indigo.loadMolecule(mol.Smiles)
		mol_obj.layout()
		line = mol_obj.cml()
		line = line.replace('\n', '')
		cml_dict[mol.sample_code] = line
	paginator = Paginator(molecule_list,50)
	page = request.GET.get('page')
	mols = paginator.get_page(page)
	conn.closed
	print("bye")
	return render(request,'molbank/index.html',{'mols':mols,'pill':'show_mols', 'cml_dict':cml_dict,'username':request.user.username})


def loginHTML(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			form1 = loginForm(request.POST)
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				print(user.password)
				return redirect("home")
			else:
				print("user unsuccessful")
				return redirect("login")
		return render(request,"molbank/login.html")
	else:
		return redirect("loadhome")


@login_required()
def logoutHTML(request):
	logout(request)
	return redirect("login")


@login_required()
def loadhome(request):
	return HttpResponse("/molbank/dummyhome.html")


@login_required()
def home(request):
	if not request.user.is_authenticated:
		return redirect('login')
	return render(request,"molbank/home.html",{'pill':'home','username':request.user.username})


@login_required()
def search_mol(request):
	# sample_func()
	return render(request,'molbank/search.html',{
		'form1': advancedSearchForm,
		'form2':simpleSearchForm,
		'form3':rangeSearchForm,
		'pill':'search',
		'username':request.user.username
	})
@login_required()
def simpleSearch(request):
	if request.method == 'POST':
		form1 = simpleSearchForm(request.POST)
		form2 = rangeSearchForm(request.POST)
		print(form1.is_valid())
		print(form1)
		if form1.is_valid():
			search_type=request.POST.get('simple_search_type')
			var = str(form1.cleaned_data['data'])
			conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
			cur = conn.cursor()
			cur.execute('SET search_path TO bingo')
			if int(search_type) == 5:
				cur.execute("select  * from molbank_allplates where \"Solution_PT_Barcode\" = '"+var+"'")
			elif int(search_type) == 6:
				cur.execute("select  * from molbank_allplates where \"Neat_sample_Barcode\" = '"+var+"'")
			elif int(search_type) == 3:
				cur.execute("select  * from molbank_allplates where sample_code = '"+var+"'")
			elif int(search_type) == 4:
				cur.execute("select  * from molbank_allplates where \"Molecular_Formula\" = '"+var+"'")
			elif int(search_type) == 1:
				cur.execute("select  * from molbank_allplates where \"Smiles\" = '"+var+"'")
			elif int(search_type) == 2:
				cur.execute("select  * from molbank_allplates where \"Name\" = '"+var+"'")
			molecule_list = namedtuplefetchall(cur)
			# pprint.pprint(molecule_list)
			cml_dict = {}
			indigo = Indigo()
			for mol in molecule_list:
				mol_obj = indigo.loadMolecule(mol.Smiles)
				mol_obj.layout()
				line = mol_obj.cml()
				line = line.replace('\n','')
				cml_dict[mol.sample_code] = line
			conn.closed
			return render(request,'molbank/search_results.html',{'molecule_list': molecule_list,'cml_dict': cml_dict,'mols':molecule_list,'username':request.user.username})
		elif form2.is_valid():
			search_type=request.POST.get('range_search_type')
			var_from = str(form2.cleaned_data['from_'])
			var_to = str(form2.cleaned_data['to_'])
			conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
			cur = conn.cursor()
			cur.execute('SET search_path TO bingo')
			print(var_from)
			print(var_to)
			if int(search_type) == 1:
				cur.execute("select  * from molbank_allplates where \"Molecular_Weight\" between "+var_from+" and "+var_to)
			elif int(search_type) == 2:
				cur.execute("select  * from molbank_allplates where \"CLogP\" between "+var_from+" and "+var_to)
			elif int(search_type) == 3:
				cur.execute("select  * from molbank_allplates where \"TPSA\" between "+var_from+" and "+var_to)
			molecule_list = namedtuplefetchall(cur)
			pprint.pprint(molecule_list)
			cml_dict = {}
			indigo = Indigo()
			for mol in molecule_list:
				mol_obj = indigo.loadMolecule(mol.Smiles)
				mol_obj.layout()
				line = mol_obj.cml()
				line = line.replace('\n','')
				cml_dict[mol.sample_code] = line
			conn.closed
			return render(request,'molbank/search_results.html',{'molecule_list': molecule_list,'cml_dict': cml_dict,'mols':molecule_list,'username':request.user.username})

	return render(request,'molbank/search_results.html',{'username':request.user.username})

@login_required()
def advancedSearch(request):
	if request.method == 'POST' or request.GET.get('page'):
		form1 = advancedSearchForm(request.POST)
	# print(form1.is_valid())
	conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
	cur = conn.cursor()
	cur.execute('SET search_path TO bingo')
	if form1.is_valid():
		var = str(form1.cleaned_data['text_smiles'])
		search_type=request.POST.get('search_type')
		#Substructure Search Results
		# if int(search_type) == 1:
		#     molecule_list = molbank.objects.raw("select * from molbank_molbank where \"SMILES\" operator(public.@) ('"+var+"','')::bingo.sub ORDER BY getsimilarity(\"SMILES\",'"+var+"','Tanimoto')")
		#     return render(request,'molbank/search_results.html',{'form': form1,'molecule_list': molecule_list})
		# func = {
		#     1: "('"+var+"','')::bingo.sub",
		#     2: "('"+var+"','')::bingo.exact",
		#     3: "(0.8, null, '"+var+"', 'Tanimoto')::bingo.sim",
		# }
		exact = {
			'1': 'ELE',
			'2': 'MAS',
			'3': 'STE',
			'4': 'FRA',
		}
		similarity = {
			'1': 'Tanimoto',
			'2': 'Tversky',
			'3': 'Euclid-Sub',
		}
		parameter = ''
		func = ''
		if int(search_type) == 1 or int(search_type) == 2:
			SubStructureSearch_type = request.POST.get('SubStructureSearch_type')
			if int(SubStructureSearch_type) == 2:
				parameter = 'RES'
			elif int(SubStructureSearch_type) == 3:
				rms = request.POST.get('rmsa')
				parameter = 'AFF ' + rms
			elif int(SubStructureSearch_type) == 4:
				rms = request.POST.get('rmsc')
				parameter = 'CONF ' + rms
			func = "('"+var+"','" + parameter + "')::bingo.sub"

		elif int(search_type) == 3:
			selected_list = form1.cleaned_data['ExactSearch_type']
			flag = 0
			for string in selected_list:
				flag = 1
				parameter = parameter + exact[string] + ' '
			if flag == 0:
				parameter = 'NONE'
			func = "('"+var+"','" + parameter + "')::bingo.exact"
		elif int(search_type) == 4:
			SimilaritySearch_type = request.POST.get('SimilaritySearch_type')
			parameter = similarity[SimilaritySearch_type]
			min_sim = request.POST.get('min_sim')
			func = "(" + min_sim + ", null, '" + var + "', '" + parameter + "')::bingo.sim"
		elif int(search_type) == 5:
			TautomerSearch_Switch = request.POST.get('TautomerSearch_Switch')
			parameter = 'TAU'
			selected_list = form1.cleaned_data['TautomerSearch_type']
			for string in selected_list:
				parameter = parameter + ' R' + string
			if int(TautomerSearch_Switch) == 1:
				func = "('"+var+"','" + parameter + "')::bingo.sub"
			elif int(TautomerSearch_Switch) == 1:
				func = "('" + var + "','" + parameter + "')::bingo.exact"
		#print(form1.cleaned_data['ExactSearch_type'])
		cur.execute("select * from molbank_allplates where \"Smiles\" operator(public.@) %s ORDER BY getsimilarity(\"Smiles\",'%s','Tanimoto')" % (func,var))
		molecule_list = namedtuplefetchall(cur)
		cml_dict = {}
		indigo = Indigo()
		for mol in molecule_list:
			mol_obj = indigo.loadMolecule(mol.Smiles)
			mol_obj.layout()
			line = mol_obj.cml()
			line = line.replace('\n','')
			cml_dict[mol.sample_code] = line
		paginator = Paginator(molecule_list,50)
		page = request.GET.get('page')
		mols = paginator.get_page(page)
		request.session['func'] = func
		request.session['var'] = var
		conn.closed
		return render(request, 'molbank/search_results.html', {
														   'molecule_list': molecule_list,
														   'cml_dict': cml_dict,
														   'username':request.user.username,
														   'mols':mols,'flag':'1',
														   })
	elif request.GET.get('page') and 'func' in request.session:
		func = request.session['func']
		var = request.session['var']
		cur.execute("select sample_code, \"Smiles\", \"IUPAC_Name\" from molbank_allplates where \"Smiles\" operator(public.@) %s ORDER BY getsimilarity(\"Smiles\",'%s','Tanimoto')" % (func,var))
		molecule_list = namedtuplefetchall(cur)
		cml_dict = {}
		indigo = Indigo()
		for mol in molecule_list:
			mol_obj = indigo.loadMolecule(mol.Smiles)
			mol_obj.layout()
			line = mol_obj.cml()
			line = line.replace('\n','')
			cml_dict[mol.sample_code] = line
		paginator = Paginator(molecule_list,50)
		page = request.GET.get('page')
		mols = paginator.get_page(page)
		conn.closed
		return render(request, 'molbank/search_results.html', {
														   'molecule_list': molecule_list,
														   'cml_dict': cml_dict,
														   'username':request.user.username,
														   'mols':mols,
														   })
	conn.closed
	return render(request,'molbank/search_results.html',{'username':request.user.username})




@login_required()
def add_mols(request):
	form = addForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		send_mail(
			'Subject here',
			'Here is the message.',
			'<from mail',
			['to'],
			fail_silently=False,
			)
		messages.success(request,"Successfully Uploaded the molecule")
	return render(request, 'molbank/add_mols.html', {'form': form,'pill':'add_mols','username':request.user.username})


@login_required()
def add(request):
	return render(request,"molbank/add_mols.html",{'username':request.user.username})


@login_required()
def uploadCSV(request):
	sample_func(request)
	if request.method == 'POST' and request.POST.get('myfile')!='' and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		if request.user.has_perm('molbank.is_admin'):
			fs = FileSystemStorage()
			if fs.exists(myfile):
				print(myfile, "  updated")
				fs.delete(myfile)
			else:
				f = status.create(myfile.name)
				f.save()
			filename = fs.save(myfile.name, myfile)
			uploaded_file_url = fs.url(filename)
			return render(request, 'molbank/uploadCSV.html',
						  {'uploaded_file_url': '/molbank' + uploaded_file_url, 'pill': 'uploadCSV','username':request.user.username})
		if request.user.has_perm('molbank.is_chem'):
			fs = FileSystemStorage()
			if fs.exists(myfile):
				print(myfile,"  updated")
				fs.delete(myfile)
			else:
				f = status.create(myfile.name)
				f.save()
			filename = fs.save(myfile.name, myfile)
			obj = status.objects.get(name=myfile.name)
			uploaded_file_url = fs.url(filename)
			var = fs.listdir('')
			obj.chemist = True
			obj.save()
			return render(request, 'molbank/uploadCSV.html',
						  {'uploaded_file_url': '/molbank' + uploaded_file_url, 'pill': 'uploadCSV','username':request.user.username})
		if request.user.has_perm('molbank.is_bio'):
			fs = FileSystemStorage()
			if fs.exists(myfile):
				print(myfile, "  updated")
				fs.delete(myfile)
			else:
				f = status.create(myfile.name)
				f.save()
			filename = fs.save(myfile.name, myfile)
			obj = status.objects.get(name=myfile.name)
			uploaded_file_url = fs.url(filename)
			var = fs.listdir('')
			obj.biologist = True
			obj.save()
			return render(request, 'molbank/uploadCSV.html',
						  {'uploaded_file_url': '/molbank' + uploaded_file_url, 'pill': 'uploadCSV','username':request.user.username})
		if request.user.has_perm('molbank.is_slab'):
			fs = FileSystemStorage()
			if fs.exists(myfile):
				print(myfile, "  updated")
				fs.delete(myfile)
			else:
				f = status.create(myfile.name)
				f.save()
			filename = fs.save(myfile.name, myfile)
			obj = status.objects.get(name=myfile.name)
			uploaded_file_url = fs.url(filename)
			var = fs.listdir('')
			obj.spectral = True
			obj.save()
			return render(request, 'molbank/uploadCSV.html',{'uploaded_file_url': '/molbank'+uploaded_file_url,'pill':'uploadCSV','username':request.user.username})
		return render(request, 'molbank/uploadCSV.html',{'error': 'You are not authorized to upload files','pill':'uploadCSV','username':request.user.username})
	return render(request, 'molbank/uploadCSV.html',{'pill':'uploadCSV','username':request.user.username})

@login_required()
def status_of_pending_files(request):
	if request.user.has_perm('molbank.is_admin'):
		user = 1
		#permissions
		print("PERMISSIONS:     { ")
		pprint.pprint(request.user.get_all_permissions())
		print("                 }")
		fs = FileSystemStorage()
		var = fs.listdir('')
		#listing of files
		print("FILES IN DIR :   { ")
		pprint.pprint(var[1])
		print("                  }")
		all = status.objects.all()
		return render(request, 'molbank/AdminUploadCSV.html',{'flag_pending':False,'pending': var[1],'flag':True,'pill':'uploadCSV', 'allstat': all, 'user':user,'username':request.user.username}) #flag is used for checking whether there are any pending files or not
	elif request.user.has_perm('molbank.is_chem'):
		user = 2
		print("PERMISSIONS:     { ")
		pprint.pprint(request.user.get_all_permissions())
		print("                 }")
		fs = FileSystemStorage()
		var = fs.listdir('')
		# listing of files
		print("FILES IN DIR :   { ")
		pprint.pprint(var[1])
		print("                  }")
		all = status.objects.all()
		return render(request, 'molbank/uploadCSV.html',
					  {'flag_pending':False,'pending': var[1], 'flag': True, 'pill': 'uploadCSV', 'allstat': all, 'user':user,'username':request.user.username})
	elif request.user.has_perm('molbank.is_bio'):
		user = 3
		print("PERMISSIONS:     { ")
		pprint.pprint(request.user.get_all_permissions())
		print("                 }")
		fs = FileSystemStorage()
		var = fs.listdir('')
		# listing of files
		print("FILES IN DIR :   { ")
		pprint.pprint(var[1])
		print("                  }")
		all = status.objects.all()
		return render(request, 'molbank/uploadCSV.html',
					  {'flag_pending':False,'pending': var[1], 'flag': True, 'pill': 'uploadCSV', 'allstat': all,'user':user,'username':request.user.username})
	elif request.user.has_perm('molbank.is_slab'):
		user = 4
		print("PERMISSIONS:     { ")
		pprint.pprint(request.user.get_all_permissions())
		print("                 }")
		fs = FileSystemStorage()
		var = fs.listdir('')
		# listing of files
		print("FILES IN DIR :   { ")
		pprint.pprint(var[1])
		print("                  }")
		all = status.objects.all()
		return render(request, 'molbank/uploadCSV.html',
					  {'flag_pending':False,'pending': var[1], 'flag': True, 'pill': 'uploadCSV', 'allstat': all, 'user':user,'username':request.user.username})
	return render(request, 'molbank/uploadCSV.html',{'flag': False,'pill':'uploadCSV','username':request.user.username})


@login_required()
def spectral_files(request):
    if request.user.has_perm('molbank.is_admin'):
        #permissions
        print("PERMISSIONS:     { ")
        pprint.pprint(request.user.get_all_permissions())
        print("                 }")
        fs = FileSystemStorage()
        var = fs.listdir('../media/spectralData')
        #listing of files
        print("FILES IN DIR :   { ")
        pprint.pprint(var[1])
        print("                  }")
        all = status.objects.all()
        return render(request, 'molbank/uploadCSV.html',{'pending': var[1],'flag_pending':True,'pill':'uploadCSV', 'allstat': all,'username':request.user.username}) #flag is used for checking whether there are any pending files or not
    return render(request, 'molbank/uploadCSV.html',{'flag_pending	': False,'pill':'uploadCSV','username':request.user.username})

@login_required()
def updateDB(request):
	if request.method == 'POST' and request.FILES['myfileDB']:
		myfileDB = request.FILES['myfileDB']
		if request.user.has_perm('molbank.is_admin'):
			conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
			cur = conn.cursor()
			cur.execute('SET search_path TO bingo')
			og_name = myfileDB.name
			name = og_name.replace(' ','_')
			name = name.replace('-', '_')
			# name = name.strip('.csv')
			fs = FileSystemStorage()
			filename = fs.save(name, myfileDB)
			# url = fs.url(filename)
			# create_query = molbank.objects.raw("create table " + name +
			#                                    " (Project varchar, Position_in_Array varchar, sub_project varchar, MTP_Plate_No varchar, Structure varchar, Solution_PT_Barcode int, Array_PT_Barcode varchar, Tray_PT_Barcode int, Neat_sample_Barcode int, Array_NS_Barcode int, Tray_NS_Barcode int, Smiles varchar, Sample_code varchar, Molecular_Weight float8, Molecular_Formula varchar, CLogP float8, Name varchar, NMR float8, Mass float8, HPLC_or_LCMS  float8, Solubility float8, No_of_Rings int, No_of_nitrogens int, No_of_Oxygens int, TPSA float8, No_of_Sulphur int, Sample_Weight_submitted varchar, Purity float8, IUPAC_Name varchar, Date_of_approval date, Date_of_Submission date, Scientist_name varchar, Reference_syn_or_bio varchar, Known_bio_activity varchar, Natural_or_Synthetic varchar, Physical_state varchar, Sample_in varchar, Sample_out varchar, Miscellaneous varchar, Optical_Rotation varchar, Institute varchar)")
			# copy_query = molbank.objects.raw("COPY " + name + " FROM '" + url + "' WITH CSV HEADER DELIMITER AS ',';")
			# print(create_query, copy_query)

			# with open(os.path.join(settings.MEDIA_ROOT, filename), 'r') as f:
			#     # Notice that we don't need the `csv` module.
			#     next(f)  # Skip the header row.
			#     cur.copy_from(f, 'molbank_allplates', sep=',')
			f = open(os.path.join(settings.MEDIA_ROOT, filename))
			cur.copy_expert(sql="""COPY molbank_allplates FROM STDIN WITH CSV HEADER DELIMITER AS ','""" , file=f)
			conn.commit()
			cur.close()
			print("og_name=",og_name.strip('.csv')+'.xlsx')
			obj = status.objects.filter(name=str(og_name.strip('.csv')+'.xlsx'))
			print(obj)
			if obj is not None:
				obj.delete()
				print(obj, "deleted.")
			print(obj)
			all = status.objects.all()
			conn.closed
			return render(request, 'molbank/AdminUploadCSV.html',
						  {'flag': True, 'pill': 'updateDB', 'allstat': all,'fname':myfileDB.name,'username':request.user.username})
		return render(request, 'molbank/uploadCSV.html',{'error': 'You are not authorized to upload files','pill':'updateDB','username':request.user.username})


# @login_required()
# def persist(request):
#     if request.method == 'POST':
#         filename = request.POST.get('filename')
#         newname = filename.replace(' ', '_')
#     #     UPDATE
#     #     C
#     #     SET
#     #     column1 = A.column1
#     #     , column2 = B.column2
#     #     , column3 = A.column1 + B.column2
#         # FROM
#         # A
#         # JOIN
#         # B
#         # ON
#         # A.id = B.id - - ??? not specified in question!
#         # WHERE
#         # C.id = A.id - -  ??? not specified in question!
#         # AND(C.column1, C.column2, C.column3)
#         # IS
#         # DISTINCT
#         # FROM
#         # (A.column1, B.column2, A.column1 + B.column2)
#
#
#
#         upsert_query = molbank.objects.raw("insert into AllPlates select * from " + newname +
#                                            " on conflict (Sample_code) do nothing")
#
#         # upsert_query = molbank.objects.raw("WITH upd AS (UPDATE molbank_molbank SET " +
#         #                                    "molbank_molbank. = sales_count + 1 WHERE id =(SELECT \"SAMPLE CODE\" FROM " +newname+ ") RETURNING *) INSERT INTO employees_log SELECT *, current_timestamp FROM upd;")
#         ############################


@login_required()
def report(request, report):
    # mol = molbank.objects.raw("select * from molbank_molbank where \"ID\" = '" + str(report) + "'")
    conn = psycopg2.connect("host=localhost dbname=vinay user=postgres password=password")
    cur = conn.cursor()
    cur.execute('SET search_path TO bingo')
    cur.execute("select * from molbank_allplates where sample_code = '%s'"%str(report))
    mol = namedtuplefetchall(cur)
    indigo = Indigo()
    mol_obj = indigo.loadMolecule(mol[0].Smiles)
    mol_obj.layout()
    line = mol_obj.cml()
    line = line.replace('\n', '')
    cml = line
    conn.closed
    print(mol[0])
    col_list = ['Project','Position in Array','sub project','MTP Plate No','Structure','Solution-PT Barcode','Array-PT Barcode','Tray-PT Barcode','Neat sample Barcode','Array NS Barcode','Tray NS Barcode','Smiles','Sample code','Molecular Weight','Molecular Formula','CLogP','Name','NMR (1H/ 13C)','Mass','HPLC/LCMS','Solubility','No. of Rings','No. of nitrogens','No. of Oxygens','TPSA','No. of Sulphur','Sample Weight submitted','Purity','IUPAC Name','Date of approval','Date of Submission','Scientist name','Reference (synthetic or biological)','Known biological activity','Natural/Synthetic','Physical state','Sample in','Sample out','Miscellaneous','Optical Rotation','Institute']
    return render(request, 'molbank/report.html', {'report': report, 'mol': mol[0], 'cml': cml, 'col_list': col_list,'username':request.user.username})
###############__________WRITE ERROR PAGE


# def csrf_failure(request, reason=""):
#     ctx = {'message': 'MOLBANK SECURITY: CSRF FAILURE'}
#     return render_to_response('molbank/csrf_failure.html', ctx)

# def my_custom_permission_denied_view(request,reason=""):
#     ctx = {'message': 'MOLBANK SECURITY: 403 forbidden'}
#     return render_to_response('molbank/403.html', ctx)

# def my_custom_permission_denied_view():
#     return redirect('molbank/403.html')

# def my_custom_page_not_found_view():
# 	return redirect('molbank/403.html')

def handler404(request, exception, template_name='404.html'):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request, exception, template_name='500.html'):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response

