from django.shortcuts import render,redirect
from django.contrib import messages
import openai
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from .models import Code

 
# Create your views here.
def home(request):
    #api = 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
    lang_list=[' c', 'abap', 'abnf', 'actionscript', 'ada', 'agda', 'al', 'antlr4', 'apacheconf', 'apex', 'clike', 'csharp', 'css', 'csv', 'excel-formula', 'fortran', 'go','html', 'java', 'javascript', 'json', 'markdown', 'markup', 'markup-templating', 'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sas', 'sass', 'typescript', 'wgsl', 'wiki', 'xml-doc']
    if request.method == "POST":
        code = request.POST['code']
        langauge = request.POST['lang']
        if langauge == 'Select Programing language':
            messages.success(request,"Hey, You forgot to Pick a programming languae")
            return render(request,'chatai/home_page.html',{"lang_list":lang_list,"code":code,"langauge":langauge}) 
        
        else:
            OPENAI_API_KEY = "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"
            openai.api_key = "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"
            openai.Model.list()
        
            try:
                response =openai.Completion.create(
                         engine = 'gpt-3.5-turbo-instruct',
                         prompt =f"Respond only with code. Fix this{langauge} code:{code}",
                         temperature =0,
                         max_tokens = 1000,
                         top_p=1.0,
                         frequency_penalty =0.0,
                         presence_penalty  = 0.0,
                    )
                response =(response["choices"][0]["text"]).strip() 
                record = Code(question = code,code_answer=response,langauge=langauge,user=request.user)
                record.save()
                return (request,'chatai/home_page.html',{"lang_list":lang_list,response:"response",langauge:"langauge"})
                    

            except Exception as e:
                print(e)
                return render(request,'chatai/home_page.html',{"lang_list":lang_list,e:"code",langauge:"langauge"})
        
    return render(request,'chatai/home_page.html',{"lang_list":lang_list})


def suggest(request):
    lang_list=[' c', 'abap', 'abnf', 'actionscript', 'ada', 'agda', 'al', 'antlr4', 'apacheconf', 'apex', 'clike', 'csharp', 'css', 'csv', 'excel-formula', 'fortran', 'go','html', 'java', 'javascript', 'json', 'markdown', 'markup', 'markup-templating', 'php', 'powershell', 'python', 'regex', 'ruby', 'rust', 'sas', 'sass', 'typescript', 'wgsl', 'wiki', 'xml-doc']
    if request.method == "POST":
        code = request.POST['code']
        langauge = request.POST['lang']
        if langauge == 'Select Programing language':
            messages.success(request,"Hey, You forgot to Pick a programming languae")
            return render(request,'chatai/suggest.html',{"lang_list":lang_list,"code":code,"langauge":langauge}) 
        
        else:
            OPENAI_API_KEY = "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"
            openai.api_key = "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"
            openai.Model.list()
        
            try:
                response =openai.Completion.create(
                         engine = 'gpt-3.5-turbo-instruct',
                         prompt =f"Respond only with code. {code}",
                         temperature =0,
                         max_tokens = 1000,
                         top_p=1.0,
                         frequency_penalty =0.0,
                         presence_penalty  = 0.0,
                    )
                response =(response["choices"][0]["text"]).strip() 
                record = Code(question = code,code_answer=response,langauge=langauge,user=request.user)
                record.save()
                return (request,'chatai/suggest.html',{"lang_list":lang_list,response:"response",langauge:"langauge"})
                
                    

            except Exception as e:
                print(e)
                return render(request,'chatai/suggest.html',{"lang_list":lang_list,e:"code",langauge:"langauge"})
        
    return render(request,'chatai/suggest.html',{"lang_list":lang_list})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have succesfully logged in ")
            return redirect('home_page')
        else:
            messages.error(request,"Error Logging In. Please retypr password")
            return redirect('home_page')
    else:
        return render(request,'chatai/home_page.html')
    
def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect('home_page')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,"You have Registered Congrats")
            return redirect('home_page')
    else:
        form =SignUpForm()
        
    return render(request,'chatai/register.html',{"form":form})

def past(request):
	if request.user.is_authenticated:
		code = Code.objects.filter(user_id=request.user.id)
		return render(request, 'chatai/past.html', {"code":code})	
	else:
		messages.success(request, "You Must Be Logged In To View This Page")
		return redirect('home')


def delete_past(request, Past_id):
	past = Code.objects.get(pk=Past_id)
	past.delete()
	messages.success(request, "Deleted Successfully...")
	return redirect('past')