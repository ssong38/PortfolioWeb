#looking at tutorial on Youtube
#"Cite" https://www.youtube.com/watch?v=A_bs6M_P_7U&index=10&list=PLei96ZX_m9sWQco3fwtSMqyGL-JDQo28l
#The whole bootstrap templates is from https://startbootstrap.com/template-overviews/stylish-portfolio/
#The index.html is modified by my self
import xml.etree.ElementTree as ET

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo

#This dictionary will take all of file information according to version
dicttest ={}
#This dictionary will take all of version message according to version
versionmessage = {}
#This dictionary will be passed into index.html
webdict = {}
# This dictionary will store information according to the assignment
finaldict = {}

#process data
def processlist():
    '''
    This function is to process XML file and store them into dicttest according to the version
    Generally speaking, this keys of dicttest will be version. The value of dicttest will be another array(dict)
    Then it will take all of file of the certain version submission.
    :return:
    '''
    tree =ET.ElementTree(file='/Users/AMsong/Desktop/cs242portfolio/data/svn_list.xml')
    root = tree.getroot()
    name = ''
    size = 0
    commit = 0
    author = 'ssong38'
    date = 0
    file1 = ''

    for i in range(len(root[0])):
        subnode = root[0][i]
        file1 = root[0][i].attrib['kind']
        size = 0
        if file1 == 'dir':
            for i in range(len(subnode)):
                if subnode[i].tag == 'name':
                    name = subnode[i].text
                if i == 1:
                    commit = subnode[i].attrib['revision']
                    for child in subnode[1]:
                        if child.tag == 'author':
                            author = child.text
                        elif child.tag == 'date':
                            date = child.text
        else:
            for i in range(len(subnode)):
                if subnode[i].tag == 'name':
                    name = subnode[i].text
                if subnode[i].tag == 'size':
                    size = subnode[i].text
                if i == 2:
                    commit = subnode[i].attrib['revision']
                    for child in subnode[2]:
                        if child.tag == 'author':
                            author = child.text
                        elif child.tag == 'date':
                            date = child.text
        if commit not in dicttest.keys():
            dict1 = {}
            dicttest[commit] = []
            dict1[name] = {}
            dict1[name]['size'] = size
            dict1[name]['author'] = author
            dict1[name]['date'] = date
            dict1[name]['filetype'] = file1
            dicttest[commit].append(dict1)
        else:
            dict1={}
            dict1[name] = {}
            dict1[name]['size'] = size
            dict1[name]['author'] = author
            dict1[name]['date'] = date
            dict1[name]['filetype'] = file1
            dicttest[commit].append(dict1)

def processlog():
    '''
    This function is to handle log.xml. This file contains submission message.
    It's too annoying to put all of information into one dict.
    Therefore, I put all of message information into a new dict
    The key of dict is the version of submission. The value of dict is the message coming with each submission
    :return:
    '''
    tree =ET.ElementTree(file='/Users/AMsong/Desktop/cs242portfolio/data/svn_log.xml')
    root1 = tree.getroot()

    for i in range (len(root1)):
        root2 = root1[i]
        version = root2.attrib['revision']
        message = root2[3].text
        versionmessage[version] = message

def produceText():
    '''
    In this function, we have built two dicts.
    The first one is finaldict - categrized according to the homework
    The second one is webdict - I modified format of finaldict and add message into this webdict
    The goal of webdict is to build easy format for website to query
    :return:
    '''
    for i in dicttest:
        if dicttest[i][0].keys()[0][0:13] not in finaldict.keys():
            finaldict[dicttest[i][0].keys()[0]] = {}
            finaldict[dicttest[i][0].keys()[0]][i] = dicttest[i]
        else:
            #print dicttest[i][0].keys()[0]
            finaldict[dicttest[i][0].keys()[0][0:13]][i] = dicttest[i]

    for i in finaldict:
        print i
        assiname = i
        webdict[assiname] = {}
        #webdict[assiname].append('Assignment Name: ' + str(assiname))

        for j in finaldict[i]:
            versionname = j
            webdict[assiname][str(versionname)] = {}
            webdict[assiname][str(versionname)]['message'] = 'Version Messgae: ' + str(versionmessage[versionname])
            webdict[assiname][str(versionname)]['file'] = []
            webdict[assiname][str(versionname)]['file'].append(['filename','date','filetype','author','size'])
            for z in range(len(finaldict[i][j])):
                filename = finaldict[i][j][z].keys()[0]
                date = finaldict[i][j][z][filename]['date']
                filetype = finaldict[i][j][z][filename]['filetype']
                author = finaldict[i][j][z][filename]['author']
                size = finaldict[i][j][z][filename]['size']
                webdict[assiname][str(versionname)]['file'].append([filename,date,filetype,author,size])

        print webdict.keys()


def processdata():
    '''
    This function is to call three sub-functions
    :return:
    '''
    processlist()
    processlog()
    produceText()



#This is web part
#Now I only have main page
app = Flask(__name__)

# This is to initialize our mongo database(Mlab)
app.config['MONGO_DBNAME'] = 'connect_to_portfolio'
app.config['MONGO_URI'] = 'mongodb://cs242portfolio:SSl930429@ds141410.mlab.com:41410/connect_to_portfolio'

mongo = PyMongo(app)

@app.route('/')
def index():
    '''
    This is our main page function. Due to the setting, I have to search on mongodb to show all of comment on main page every time.
    :return:
    '''
    #return render_template('index.html')
    #processdata()
    feedback = mongo.db.feedbacks
    res1 = feedback.find({'page': 'Main'})
    tempres = list(res1)
    return render_template('index.html' , arr = tempres, showornot = 0)

@app.route('/feedback_page')
def index1():
    '''
    This is for feedback page
    :return:
    '''
    feedback = mongo.db.feedbacks
    res1 = feedback.find()
    tempres = list(res1)
    feedwomain = []

    for i in tempres:
        if i['page'] != 'Main':
            feedwomain.append(i)

    return render_template('feedback.html' , arr = feedwomain )


@app.route('/add')
def add():
    '''
    This is to initialize our MongoDB collection portfolio. Call it once is enough.
    Below is our data content:
                                data = {
                                'assignmentName' : assignmentName,
                                'version' : version,
                                'message' : message,
                                'filename' : filename,
                                'date' : date,
                                'filetype' : filetype,
                                'author' : author,
                                'size': size
                            }
    :return:
    '''
    processdata()
    portfolio = mongo.db.portfolios
    for i in webdict:
        assignmentName = i;
        for j in webdict[i]:
            version = j
            message = ''
            for z in webdict[i][j]:
                if z == 'message':
                    message = webdict[i][j][z]
            for z in webdict[i][j]:
                filename = ''
                date = ''
                filetype = ''
                size = ''
                author = ''

                if z == 'file':
                    for ii in webdict[i][j][z]:
                        if ii[0]!= 'filetype' and ii[1] != 'date' and ii[2]!='filetype' and ii[3]!='author' and ii[4] != 'size':
                            for jj in range(len(ii)):
                                if jj == 0:
                                    filename = ii[jj]
                                elif jj == 1:
                                    date = ii[jj]
                                elif jj == 2:
                                    filetype = ii[jj]
                                elif jj == 3:
                                    author = ii[jj]
                                elif jj == 4:
                                    size = ii[jj]

                            data = {
                                'assignmentName' : assignmentName,
                                'version' : version,
                                'message' : message,
                                'filename' : filename,
                                'date' : date,
                                'filetype' : filetype,
                                'author' : author,
                                'size': size
                            }

                            portfolio.insert(data)

    return "initial mongoDB is finished!"

@app.route('/post_feedback', methods=['POST'])
def post_feedback():
    '''
    This is postfeedback. This function is for mainpage and childpage's comment area. We will store comment into
    MongoDB collections feedback. By default, when you post a comment, the comment will be saved into DB.
    :return:
    '''
    #Process the redtag word before storing data to the database
    redtaglist = []
    replacetaglist = []

    redlist = mongo.db.redlists
    res1 = redlist.find()
    tempres = list(res1)

    print request.form['mess'][0]

    for i in tempres:
        redtaglist.append(i['reg_tag_word'])
        replacetaglist.append(i['replace_word'])

    orgi_mess = request.form['mess']
    for i in range(len(redtaglist)):
        orgi_mess = orgi_mess.replace(redtaglist[i], replacetaglist[i])

    feedback = mongo.db.feedbacks
    feedback.insert({"name": request.form['name'], "message": orgi_mess, "page": request.form['subject']})
    if request.form['subject'] == 'Main':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index1'))

@app.route('/post_redwordlist', methods=['POST'])
def post_redwordlist():
    '''
    This is postfeedback. This function is for mainpage and childpage's comment area. We will store comment into
    MongoDB collections feedback. By default, when you post a comment, the comment will be saved into DB.
    :return:
    '''
    redlist = mongo.db.redlists
    redwords = request.form['redtag']
    replacewords = request.form['replacetag']
    print type(redwords)
    redwordlist = redwords.split(',')
    replacewordlist = replacewords.split(',')
    print redwordlist
    print replacewordlist
    for i in range(len(redwordlist)):
        redlist.insert({"reg_tag_word": redwordlist[i], "replace_word": replacewordlist[i]})
    return redirect(url_for('index'))

@app.route('/findassignment/<assignment>',methods=['GET'])
def get_assignment_list(assignment):
    '''
    This function is for main page - assignment list. Every time, when you click a learn more button under the assignment,
    You will go to the corresponding page of the assignment with all of file in that assignment.
    :param assignment:
    :return:
    '''
    portfolio = mongo.db.portfolios
    res = portfolio.find({'assignmentName': assignment})
    array = list(res)
    return render_template('sub.html', i = assignment, arr = array, showornot = 0)

@app.route('/find_feedback/<page>',methods=['GET'])
def get_feedback_list(page):
    '''
    This is the search comment function. We need to give a page varible, since it will search a certain page comment.
    :param page:
    :return:
    '''
    ff = 0
    inputSentence =  request.args.get('searchfeedback')
    if inputSentence != '':
        ff = 1
        array1 = []
        tempres = []
        portfolio = mongo.db.portfolios
        res = portfolio.find({'assignmentName': page})
        array = list(res)
        feedback = mongo.db.feedbacks
        queryword = inputSentence
        temparray = queryword.split(',')
        res1 = feedback.find({'page': page})
        tempres = list(res1)
        print tempres

        if len(tempres) != 0:
            for mm in tempres:
                count = 0
                for nn in temparray:
                    if nn in mm['message']:
                        count = count + 1
                        if count == len(temparray):
                            array1.append(mm)
                    else:
                        break
        print array1

    if page == "Main":
        #return render_template('index.html', i = page, arr = array, arr1 = array1, showornot = ff)
        return render_template('index.html', arr = tempres, arr1 = array1, showornot = ff)
    else:
        return render_template('sub.html', i = page, arr = array, arr1 = array1, showornot =ff)



###Below are several test functions.
@app.route('/test')
def test():
    '''
    This is to test layout html
    :return:
    '''
    return render_template('/layout/layout1.html')

@app.route('/test1')
def test1():
    '''
    This is to test the basic homework website
    :return:
    '''
    return render_template('sub.html')

@app.route('/test2')
def test2():
    '''
    This is to test index page.
    :return:
    '''

    feedback = mongo.db.feedbacks_test
    res1 = feedback.find({'page': 'Main'})
    tempres = list(res1)
    return render_template('test.html' , arr = tempres, showornot = 0)


@app.route('/post_feedback_test', methods=['POST'])
def post_feedback_test():
    '''
    This one is to test post feedback. Also helps test index html. The comment database is different from the database which actually save the comments
    :return:
    '''
    #Process the redtag word before storing data to the database
    redtaglist = []
    replacetaglist = []

    redlist = mongo.db.redlists
    res1 = redlist.find()
    tempres = list(res1)

    print request.form['mess'][0]

    for i in tempres:
        redtaglist.append(i['reg_tag_word'])
        replacetaglist.append(i['replace_word'])

    orgi_mess = request.form['mess']
    print orgi_mess
    print '&#13;&#10' in orgi_mess
    for i in range(len(redtaglist)):
        orgi_mess = orgi_mess.replace(redtaglist[i], replacetaglist[i])

    feedback = mongo.db.feedbacks_test
    feedback.insert({"name": request.form['name'], "message": orgi_mess, "page": request.form['subject']})
    return redirect(url_for('test2'))


if __name__ == "__main__":
    app.run(debug = True)
