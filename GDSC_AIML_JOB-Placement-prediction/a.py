from flask import Flask,request,render_template
import numpy as np
import pickle


with open('placement.pkl','rb') as model_file :
    model = pickle.load(model_file)
app = Flask(__name__, template_folder='H:/GDSC_AIML_JOB-Placement-prediction/template')


@app.route('/')
def index():
    return render_template('web_page_job_prediction.html')

@app.route('/prediction',methods=['POST'])
def prediction():

    result = None
    # get data from form
    ssc_b = request.form['secondary_school_board']
    ssc_p = request.form['secondary_school_percentage']
    hsc_b = request.form['higher_school_board']
    hsc_s = request.form['higher_school_subject']
    hsc_p = request.form['higher_school_percentage']
    dg_p = request.form['degree_percentage']
    ug_d = request.form['undergrad_degree']
    w_ex = request.form['work_experience']
    spc = request.form['specialisation']
    emp_t = request.form['emp_test_percentage']
    mba_p = request.form['mba_percentage']
    input_list = [ssc_b, ssc_p, hsc_b, hsc_s, hsc_p, dg_p, ug_d, w_ex, spc, emp_t, mba_p]
    int_list = [ssc_p,hsc_p,dg_p,emp_t,mba_p]
    converted_data = [float(x) for x in int_list]
    if ssc_b == 'Others':
        converted_data.append(1)
    else:
        converted_data.append(0)

    if hsc_b == 'Others':
        converted_data.append(1)
    else:
        converted_data.append(0)

    if hsc_s == 'Science':
        converted_data += [0,1]
    elif hsc_s == 'Commerce':
        converted_data += [1,0]
    else:
        converted_data += [0,0]

    if ug_d == 'Others':
        converted_data += [1,0]
    elif ug_d == 'Sci&Tech':
        converted_data += [0,1]
    else:
        converted_data += [0,0]

    if w_ex == 'Yes':
        converted_data.append(1)
    else:
        converted_data.append(0)

    if spc == 'Mkt&HR':
        converted_data.append(1)
    else:
        converted_data.append(0)


    print(converted_data)
    single_pred = np.array(converted_data).reshape(1, -1)

    prediction = model.predict(single_pred)


    if prediction[0] == 1:
        result ="Your chances of placement are significantely high."
    else:
        result ="Your chances of placement seems low.You must focus on ur skill to strengthen ur chances."
    return render_template('web_page_job_prediction.html',result=result)

# python main
if __name__ == "__main__":
    app.run(debug=True)