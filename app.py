from flask import Flask, render_template, request
import pandas as pd
app = Flask(__name__)

data = pd.read_excel('josaa.xlsx')
data['Closing Rank']= data['Closing Rank'].astype('int')
clgs=data['Institute'].unique()
category=data['Seat Type'].unique()


@app.route('/')
def form():
    return render_template('home.html',texts=clgs,category=category)

# Define the route to handle form submission
@app.route('/process', methods=['POST'])
def process():
    # Retrieve form data
    gender = request.form.get('gender')
    home_state = request.form.get('text')
    
    category = request.form.get('category')
    open_rank = int(request.form.get('openRank'))
    copen_rank = int(request.form.get('openRankc'))
   
    uploaded_file = request.files['file']

    # Get the file extension
    file_extension = uploaded_file.filename.rsplit('.', 1)[-1].lower()

    # Check if it's a CSV file
    if file_extension == 'csv':
        input = pd.read_csv(uploaded_file)
        # Process the CSV file

    # Check if it's an Excel file
    elif file_extension in ['xls', 'xlsx']:
        input = pd.read_excel(uploaded_file,header=None)
        input.columns = ['institute','branch']
        # Process the Excel file
    
    else:
        return "Unsupported file format Please upload either csv or excel file"
    #print(data['Quota'].unique())
    if gender == 'Male' :
      gender = 'Gender-Neutral'
    else :
      gender = 'Female-only (including Supernumerary)'
    x=open_rank
    y=copen_rank
    open_rank =  int(open_rank - (open_rank/10))
    copen_rank =  int(copen_rank - (copen_rank/10))
    #print(copen_rank)
    mdata =  data[(data['Gender'] == gender)]
    rows=input.shape[0]
    predict = []
    for i in range (0,rows) :
      temp=0
      a=(mdata[(mdata['Institute'] == input.iloc[i]['institute']) & (mdata['Academic Program Name'] == input.iloc[i]['branch']) & ((mdata['Quota'] == 'AI')| (mdata['Quota'] == 'OS')) & (mdata['Seat Type'] == 'OPEN')]['Closing Rank'])
      
      b=mdata[(mdata['Institute'] == input.iloc[i]['institute']) & (home_state==input.iloc[i]['institute']) & (mdata['Academic Program Name'] == input.iloc[i]['branch']) & (mdata['Quota'] == 'HS') & (mdata['Seat Type'] == 'OPEN')]['Closing Rank']
      c=mdata[(mdata['Institute'] == input.iloc[i]['institute']) & (home_state==input.iloc[i]['institute']) & (mdata['Academic Program Name'] == input.iloc[i]['branch']) & (mdata['Quota'] == 'HS') & (mdata['Seat Type'] == category)]['Closing Rank']
      #print(i,b)
      d=mdata[(mdata['Institute'] == input.iloc[i]['institute']) & (mdata['Academic Program Name'] == input.iloc[i]['branch']) & ((mdata['Quota'] == 'AI')| (mdata['Quota'] == 'OS')) & (mdata['Seat Type'] == category)]['Closing Rank']
      if ( (a.shape[0]!=0) & (temp==0)) :
        if(int(a.values) >= open_rank) :
          predict.append(list(input.iloc[i]))
          temp=1
      if ((b.shape[0]!=0)& (temp==0)) :
        if(int(b.values) >= open_rank) :
          predict.append(list(input.iloc[i]))
          temp=1
      if ( (c.shape[0]!=0) & (temp==0)) :
        #print(c.values,copen_rank)
        if(int(c.values) >= copen_rank) :
          predict.append(list(input.iloc[i]))
          temp=1
      if ( (d.shape[0]!=0) & (temp==0)) :
        if(int(d.values) >= copen_rank) :
          predict.append(list(input.iloc[i]))
          temp=1
    
    output = pd.DataFrame(predict,columns=['Institute','Branch'])
    table_html = output.to_html(index=False)

      
 
    

    # Perform sorting or any other necessary operations on the data
    # Example: Sort the data based on the open rank category rank

    # Return the sorted data as a response
    # You can choose the appropriate response format, such as rendering a template or returning JSON data
    return render_template('result.html', gender=gender, category=category, open_rank=x, state=home_state,copen_rank=y,table=table_html)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
