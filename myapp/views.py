from django.shortcuts import render
from django.http import HttpResponse
import matplotlib
#import talib
#import nsepython
#from nsepython import *
import time
import queue
from threading  import Thread
from yahoo_fin.stock_info import *
from asgiref.sync import async_to_sync,sync_to_async
# Create your views here.
def stockpicker(request):
    stockpicker=tickers_nifty50() 
    print(type(stockpicker))
    return render(request,'stockpicker.html',{'stockpicker':stockpicker})

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True
#def stocktracker(request):
#    stock_picker=request.GET.getlist('stock_picker')
#    print(stock_picker)
#    data={}
#    available_index=tickers_nifty50() 
#    for i in stock_picker:
#        if i in available_index:
#            pass
#        else:
#            return HttpResponse("Error")
#        
#    for i in stockpicker:
#        details=get_quote_table(i)
#        data.update(details)
#
#    print(data)
#    return render(request,'stocktracker.html',{'details':details})

async def stocktracker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stockpicker = request.GET.getlist('stockpicker')
    #stockshare=str(stockpicker)[1:-1]
    #stockpicker=request.GET.getlist('stockpicker')
    print(stockpicker)
    data={}
    available_index=tickers_nifty50() 
    for i in stockpicker:
        if i in available_index:
            pass
        else:
            return HttpResponse("Error")
    n_threads=len(stockpicker)
    thread_list=[]
    que=queue.Queue()
    start=time.time()     
    #for i in stockpicker:
    #    result=get_quote_table('i')
    #    data.update({i:result})
    for i in range(n_threads):
        thread=Thread(target=lambda q,arg1:q.put({stockpicker[i]:get_quote_table(arg1)}),args=(que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result=que.get()
        data.update(result)
    end=time.time()
    time_taken=end-start
    print(time_taken)
    print(data)
    print(type(data))
    return render(request,'stocktracker.html',{'data':data,'room_name':'track'})