from django.http import JsonResponse
from django.db.models import Sum
from accounts.models import Role, User
from stocks.models import Product
from sales.models import Sales
from expenses.models import Expenses, ExpenseCategory

def roles_graph(request):
    dataset = User.objects.values('username','groups')
    groups = [data['groups'] for data in dataset]

    category = []
    val = []
    gp = {}
    for g in groups:
         gp.setdefault(g,0)
         gp[g] +=1
    for team, count in gp.items():
        name = [d['name'] for d in Role.objects.filter(id=team).values()]
        category.append(name)
        val.append(count)
    chart = {
        'chart': {
            'type': 'column',
            'borderWidth': 0.1
        },
        'title': {'text': 'Number of users per Role'},
        'yAxis': {
            'title': {'text': 'Number of Users'}},
        'xAxis': {
            'categories': category
        },
        'series': [{
            'name': 'Roles',
            'data': list(zip(category, val))
        }],
        'plotOptions': {
            'column': {
                'colorByPoint': 'true'
            }
        },
    }
    return JsonResponse(chart)

def stocks_graph(request):
    dataset = Product.objects.values('name','stock_level')
    chart = {
        'chart': {
            'type': 'column',
            'borderWidth': 0.1
        },
        'title': {'text': 'Stock Level By Product'},
        'yAxis': {
            'title': {'text': 'Level of Product'}},
        'xAxis': {
            'categories': [data['name'] for data in dataset]
        },
        'series': [{
            'name': 'Products',
            'data': list(map(lambda row: {'name': row['name'], 'y': row['stock_level']}, dataset))
        }],
        'plotOptions': {
            'column': {
                'colorByPoint': 'true'
            }
        }
    }
    return JsonResponse(chart)

def sales_graph(request):
    dataset = Sales.objects.values('name','total_amount').annotate(total=Sum('total_amount'))
    category = []
    total = 0.0
    values = []
    for data in dataset:
        if not data['name'] in category:
            category.append(data['name'])
            for data['name'] in dataset:
                total += data['total']
            values.append(total)

    chart = {
        'chart': {
            'type': 'pie',
            'borderWidth': 0.1
        },
        'title': {'text': 'Total Revenue By Product'},
        'yAxis': {
            'title': {'text': 'Total Amounts'}},
        'xAxis': {
            'categories': category
        },
        'series': [{
            'name': 'Products',
            'data':  list(zip(category, values))
        }]
    }
    return JsonResponse(chart)

def expenses_graph(request):
    dataset = Expenses.objects.values('category','amount').annotate(total=Sum('amount'))
    category = []
    total = 0.0
    values = []
    for data in dataset:
        if not data['category'] in category:
            category.append(str(ExpenseCategory.objects.get(id=int(data['category']))))
            for data['category'] in dataset:
                total += data['total']
            values.append(total)
    chart = {
        'chart': {
            'type': 'pie',
            'borderWidth': 0.1
        },
        'title': {'text': 'Total Expenses By Category'},
        'yAxis': {
            'title': {'text': 'Total Amounts'}},
        'xAxis': {
            'categories': category
        },
        'series': [{
            'name': 'Expenses',
            'data': list(zip(category, values))
        }]
    }
    return JsonResponse(chart)
