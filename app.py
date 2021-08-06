from flask import Flask,render_template,request,jsonify
import requests as req
import json

app = Flask(__name__)

def getdata():
    link = 'https://api.nbp.pl/api/exchangerates/tables/a/?format=json'
    datadict = req.get(link).json()[0]
    datanbp = datadict['rates']
    data_date = datadict['effectiveDate']
    return [datanbp,data_date]

@app.route('/')
def formdata(value="output",from_curr="",to_curr="",from_multi=""):
    data_to_form=getdata()
    data_values = data_to_form[0]
    data_date = data_to_form[1]
    return render_template('currencyexchange.html',data_to_form=data_values,data_date=data_date,value=value,
                           from_curr=from_curr,to_curr=to_curr,from_multi=from_multi)

@app.route('/',methods=['POST'])
def formdatapost():
    from_currency = float(request.form.get('from_currency'))
    print(from_currency)
    to_currency = float(request.form.get('to_currency'))
    from_multiple = float(request.form.get('from_multiple'))
    datanbp=getdata()[0]
    if from_currency == 1:
        from_code=['PLN']
    else:
        from_code = [i['code'] for i in datanbp if i['mid'] == from_currency]
    if to_currency == 1:
        to_code = ['PLN']
    else:
        to_code = [i['code'] for i in datanbp if i['mid'] == to_currency]
    return formdata((from_multiple*float(from_currency))/float(to_currency),from_code[0],to_code[0],from_multiple)


if __name__ == '__main__':
    app.run()
