from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import numpy as np
from .utils import anova2

# Create your views here.

r,c,n, alphaG, facteur1, facteur2 = 0,0,0,0.05, "facteur1", "facteur2"

def anova_view(request):
    if request.method == 'POST':
        global r,c,n, alphaG, facteur1, facteur2
        row_count = r #int(request.POST.get('row_count'))
        column_count = c #int(request.POST.get('column_count'))
        replication_count = n #int(request.POST.get('replication_count'))
        #facteur1 = request.POST.get('facteur1')
        #facteur2 = request.POST.get('facteur2')
        alpha = alphaG#float(request.POST.get('alpha'))
        #data = [[[] for j in range(column_count)] for i in range(row_count)]
        data = []
        for i in range(row_count):
            row = []
            for j in range(column_count):
                col = []
                for k in range(replication_count):
                    value = float(request.POST.get(f'X{i}{j}{k}'))
                    print(request.POST.get(f'X{i}{j}{k}'))
                    col.append(value)
                row.append(col) 
            data.append(row)
        try:
            
                    #data[i][j].append(float(request.POST.get(f'X{i}{j}{k}')))

            print(data)
            calc_anova = anova2.ANOVA2WR(data,row_count,column_count,replication_count, facteur1, facteur2, alpha)
            print(calc_anova.SST)
            context = {
                        "calc_anova":calc_anova,
                        "rmoins":r-1,
                        "cmoins":c-1,
                        "rcmoins":(r-1)*(c-1),
                        "rcnmoins":r*c*(n-1),
                        "rcnmoins1":r*c*n-1
                    }
            return render(request,"result.html",context)
        except(ZeroDivisionError):
            template = loader.get_template('result.html')
            context = {
                "message" : "Veuillez remplir les entrees du tableau correctement",
              'row_count': range(r),
                    'column_count': range(c),
                    'replication_count': range(n),
                    'facteur1': facteur1,
                    'facteur2': facteur2,
                    'alpha': alphaG,
                    'r': r,
                    'c': c,
                    'n':replication_count,
                    'fac1' : facteur1[0],
                    'fac2' : facteur2[0],
                    'rplus': r+1,
                    'cplus': c+1,
                                        
            }
            """  except (ValueError, TypeError):
            template = loader.get_template('input.html')
            row_count = int(request.POST.get('row_count'))
            column_count = int(request.POST.get('column_count'))
            replication_count = int(request.POST.get('replication_count'))
            
            context = {
                "message" : "Veuillez remplir toutes les données correctement",
                'row_count': range(row_count),
                    'column_count': range(col_count),
                    'replication_count': range(replication_count),
                    'facteur1': facteur1,
                    'facteur2': facteur2,
                    'alpha': alpha,
                    'r': row_count,
                    'c': col_count,
                    'n':replication_count,
                    'fac1' : facteur1[0],
                    'fac2' : facteur2[0],
                    'rplus': row_count+1,
                    'cplus': col_count+1,
                                        
            }"""
            
            return render(request , 'input.html', context) 
        
            
    else:
        return HttpResponse('Invalid Request')

def index(request):
    template = loader.get_template('input.html')
    context = {
        "message" : ""
    }
    return render(request, 'form_test_parameter.html', context)

def home(request):
    return render(request, 'index.html')


def validate_params(request):
    
    if request.method == 'POST':
        try:
            
            row_count = int(request.POST.get('row_count'))
            col_count = int(request.POST.get('col_count'))
            replication_count = int(request.POST.get('replication_count'))
            global r,c,n,alphaG, facteur1, facteur2
            r,c,n= row_count,col_count,replication_count
            if(row_count*col_count*(replication_count-1) <= 10) and ((row_count-1)*(col_count-1) <= 10) and ((col_count-1)*(row_count-1) != 0  ) and (replication_count >1):
                facteur1 = request.POST.get('facteur1')
                facteur2 = request.POST.get('facteur2')
                alpha = float(request.POST.get('alpha'))
                alphaG =alpha
                template = loader.get_template('input.html')
                
                context = {
                    'row_count': range(row_count),
                    'column_count': range(col_count),
                    'replication_count': range(replication_count),
                    'facteur1': facteur1,
                    'facteur2': facteur2,
                    'alpha': alpha,
                    'r': row_count,
                    'c': col_count,
                    'n':replication_count,
                    'fac1' : facteur1[0],
                    'fac2' : facteur2[0],
                    'rplus': row_count+1,
                    'cplus': col_count+1,
                    
                }
                
                return render(request, 'input.html', context)
            else:
                template = loader.get_template('form_test_parameter.html')
                context = {
                    "message" : "Veuillez entrer les valeurs de r,c et n correspondant aux combinaisons suivantes :",
                    'e1':"{ r=2, c=2, n=2 }, \n ",
                    'e2':"{ r=2, c=3, n=2 }, \n ",
                    'e3':"{ r=2, c=4, n=2 }, \n ",
                    'e4':"{ r=3, c=2, n=2 }, \n ",
                    'e5':"{ r=4, c=2, n=2 }, \n ",
                    'e6':"{ r=2, c=5, n=2 }, \n ",
                    'e7':"{ r=3, c=3, n=2 }, \n ",
                    'e8':"{ r=5, c=2, n=2 }, \n ",
                    'e9':"{ r=2, c=2, n=3 }, \n ",
                                            
                }
                return render(request , 'form_test_parameter.html', context)
                  
        except (ValueError, TypeError):
            template = loader.get_template('form_test_parameter.html')
            context = {
                "message" : "Veuillez remplir le formulaire correctement",
                'e1':"",
                'e2':"",
                'e3':"",
                'e4':"",
                'e5':"",
                'e6':"",
                'e7':"",
                'e8':"",
                'e9':"",
                                        
            }
            
            
            return render(request , 'form_test_parameter.html', context)

    else:
        
        pass
            
            
    
        
        