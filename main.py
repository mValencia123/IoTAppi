import jinja2
import pdfkit
from wsgiref.simple_server import make_server
import falcon
import json
from datetime import datetime

class TXTEmployee:
    def on_post(self, req, resp):
        doc = str(req.bounded_stream.read().decode("utf-8"))
        doc = json.loads(doc)
        print(doc["email"])
        with open("./output/employees.txt","r") as f:
            for item in f.readlines():
                list_info_employe = item.split(",")
                if list_info_employe[13] == doc["email"] :
                    # Generate txt
                    with open("./output/template.txt","r") as template:
                        temp = " ".join(template.readlines())  
                        tmp = temp.format(name = list_info_employe[0],
                            middlename = list_info_employe[1],
                            lastname = list_info_employe[2],
                            position = list_info_employe[3],
                            company = list_info_employe[4],
                            street = list_info_employe[5],
                            numExt = list_info_employe[6],
                            numInt = list_info_employe[7],
                            town = list_info_employe[8],
                            city = list_info_employe[9],
                            state = list_info_employe[10],
                            codigoPostal = list_info_employe[11],
                            telephone = list_info_employe[12],
                            email = list_info_employe[13],
                            birthday = list_info_employe[14],
                            age = list_info_employe[15])
                        with open(f'./output/{list_info_employe[13]}.txt',"x") as fc:
                            fc.write(tmp)
        resp.text = "{\"status\" : 200}"

class PDFEmployee:
    def on_post(self, req, resp):
        doc = str(req.bounded_stream.read().decode("utf-8"))
        doc = json.loads(doc)
        print(doc["email"])
        with open("./output/employees.txt","r") as f:
            for item in f.readlines():
                list_info_employe = item.split(",")
                if list_info_employe[13] == doc["email"] :
                    dict_info = {
                        'name' : list_info_employe[0],
                        'middlename' : list_info_employe[1],
                        'lastname' : list_info_employe[2],
                        'position' : list_info_employe[3],
                        'company' : list_info_employe[4],
                        'street' : list_info_employe[5],
                        'numExt' : list_info_employe[6],
                        'numInt' : list_info_employe[7],
                        'town' : list_info_employe[8],
                        'city' : list_info_employe[9],
                        'state' : list_info_employe[10],
                        'codigoPostal' : list_info_employe[11],
                        'telephone' : list_info_employe[12],
                        'email' : list_info_employe[13],
                        'birthday' : list_info_employe[14],
                        'age' : list_info_employe[15]
                    }
                    template_loader = jinja2.FileSystemLoader('./')
                    template_env = jinja2.Environment(loader=template_loader)

                    template = template_env.get_template('./output/template-html.html')
                    output_text = template.render(dict_info)

                    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
                    pdfkit.from_string(output_text, f'./pdf/{list_info_employe[13]}.pdf', configuration=config)
        resp.text = "{\"status\" : 200}"

class Employee:
    def on_delete(self, req, resp):
        doc = str(req.bounded_stream.read().decode("utf-8"))
        doc = json.loads(doc)
        print(doc["email"])
        new_text = ""
        with open("./output/employees.txt","r") as f:
            for item in f.readlines():
                list_info_employe = item.split(",")
                if list_info_employe[13] != doc["email"] :
                    new_text = item + new_text  
        with open("./output/employees.txt","w") as f:
            f.write(new_text)
        resp.text = "{\"status\" : 200}"
    
    def on_put(self, req, resp):
        doc = str(req.bounded_stream.read().decode("utf-8"))
        doc = json.loads(doc)
        print(doc["email"])
        new_text = ""
        with open("./output/employees.txt","r") as f:
            for item in f.readlines():
                list_info_employe = item.split(",")
                if list_info_employe[13] != doc["email"] :
                    new_text = item + new_text  
                else:
                    name = doc["name"]
                    middleName = doc["middlename"]
                    lastName = doc["lastname"]
                    position = doc["position"]
                    company = doc["company"]
                    street = doc["street"]
                    numExt = doc["numext"]
                    numInt = doc["numint"]
                    town = doc["town"]
                    city = doc["city"]
                    state = doc["state"]
                    codigoPostal = doc["codigopostal"]
                    telephone = doc["telephone"]
                    email = doc["email"]
                    birthday = doc["birthday"]
                    diff = datetime.today() - datetime.strptime(birthday, "%Y-%m-%d")
                    age = diff.days // 365
                    text = f'{name},{middleName},{lastName},{position},{company},{street},{numExt},{numInt},{town},{city},{state},{codigoPostal},{telephone},{email},{birthday},{age}\n'
                    new_text = text + new_text
        with open("./output/employees.txt","w") as f:
            f.write(new_text)
        resp.text = "{\"status\" : 200}"


    def on_post(self, req, resp):
        doc = str(req.bounded_stream.read().decode("utf-8"))
        doc = json.loads(doc)
        print(doc)
        name = doc["name"]
        middleName = doc["middlename"]
        lastName = doc["lastname"]
        position = doc["position"]
        company = doc["company"]
        street = doc["street"]
        numExt = doc["numext"]
        numInt = doc["numint"]
        town = doc["town"]
        city = doc["city"]
        state = doc["state"]
        codigoPostal = doc["codigopostal"]
        telephone = doc["telephone"]
        email = doc["email"]
        birthday = doc["birthday"]
        diff = datetime.today() - datetime.strptime(birthday, "%Y-%m-%d")
        age = diff.days // 365
        with open("./output/employees.txt","a") as f:
            f.write(f'{name},{middleName},{lastName},{position},{company},{street},{numExt},{numInt},{town},{city},{state},{codigoPostal},{telephone},{email},{birthday},{age}\n')
        resp.text = "{\"status\" : 200}"

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        list_info_employees = []
        with open("./output/employees.txt","r") as f:
            for item in f.readlines():
                list_info_employe = item.split(",")
                dict_info = dict({
                    'name' : list_info_employe[0],
                    'middlename' : list_info_employe[1],
                    'lastname' : list_info_employe[2],
                    'position' : list_info_employe[3],
                    'company' : list_info_employe[4],
                    'street' : list_info_employe[5],
                    'numExt' : list_info_employe[6],
                    'numInt' : list_info_employe[7],
                    'town' : list_info_employe[8],
                    'city' : list_info_employe[9],
                    'state' : list_info_employe[10],
                    'codigoPostal' : list_info_employe[11],
                    'telephone' : list_info_employe[12],
                    'email' : list_info_employe[13],
                    'birthday' : list_info_employe[14],
                    'age' : list_info_employe[15]
                })
                list_info_employees.append(dict_info)
        list_aux_info_employee = list(map(lambda x : json.dumps(x, indent = 4),list_info_employees))
        data = "[" + ",".join(list_aux_info_employee) + "]"
        data = data.replace("'","\"")
        
        resp.text = ("{open}\"status\" : 200, \"data\" : {employees}{close}".format(employees=data,open="{",close="}"))


app = falcon.App(cors_enable=True)
app.req_options.auto_parse_form_urlencoded = True
employee = Employee()
txt_employee = TXTEmployee()
pdf_employee = PDFEmployee()
app.add_route('/api/employees', employee)
app.add_route('/api/txt/employees', txt_employee)
app.add_route('/api/pdf/employees', pdf_employee)

if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()