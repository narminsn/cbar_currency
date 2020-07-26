from flask import Flask, request, jsonify, render_template
from request import parse_data
from datetime import date, datetime, timedelta
from manage import Currency_diff, Currency_time
from manage import db

app = Flask(__name__)

time_today = date.today().strftime('%d.%m.%Y')

time_yesterday = datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y')

url_today = f"https://www.cbar.az/currencies/{time_today}.xml"
url_yesterday = f"https://www.cbar.az/currencies/{time_yesterday}.xml"

try:
    data = parse_data(url_today)
    time = {'start_time': time_today, 'end_time': time_today}

except:
    data = parse_data(url_yesterday)
    time = {'start_time': time_yesterday, 'end_time': time_yesterday}


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == "GET":
        # db.session.query(Currency_time).delete()
        # db.session.commit()

        time_list = Currency_time.filter()

        if time_list:

            start = (time_list.start_time).strftime('%d.%m.%Y')
            end = time_list.end_time.strftime('%d.%m.%Y')

            time_db = {'start_time': start, 'end_time': end}

            currency = Currency_diff.all()
            context = {
                'data': currency,
                'time': time_db
            }
        else:
            context = {
                'data': data,
                'time': time
            }


    else:

        date1 = request.form.get('date1')
        date2 = request.form.get('date2')
        url1 = f"https://www.cbar.az/currencies/{date1}.xml"
        url2 = f"https://www.cbar.az/currencies/{date2}.xml"

        data1 = parse_data(url1)
        data2 = parse_data(url2)

        list_data = []
        time_list = Currency_time.filter()

        if time_list:
            db.session.delete(time_list)
            db.session.commit()
            cur_time = Currency_time(start_time=date1, end_time=date2)
            cur_time.save()

            time_db = {'start_time': date1, 'end_time': date2}

        else:
            cur_time = Currency_time(start_time=date1, end_time=date2)
            cur_time.save()
            time_db = {'start_time': date1, 'end_time': date2}




        for index, val in enumerate(data2):
            diff = val['value'] - data1[index]['value']
            if diff > 0:
                icon = "glyphicon glyphicon-arrow-up"
            elif diff < 0:
                icon = "glyphicon glyphicon-arrow-down"
            else:
                icon = "glyphicon glyphicon-minus"

            obj = {
                'name': val['name'],
                'code': val['code'],
                'value': val['value'],
                'difference': icon,
                'id': index

            }
            list_data.append(obj)

            curr = Currency_diff.query.filter_by(code=val['code']).first()
            print('SDFGHJ',curr)
            if curr:
                db.session.delete(curr)
                db.session.commit()

            new_cur_diff = Currency_diff(name=val['name'], code=val['code'], value=val['value'], difference=icon,
                                         )
            new_cur_diff.save()

            context = {
                'data': list_data,
                'time': time_db

            }



    return render_template('index.html',context=context)


app.run(debug=True, host='0.0.0.0', port=5000)
