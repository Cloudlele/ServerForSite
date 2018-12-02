from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import pypyodbc
import cgi



class Server(BaseHTTPRequestHandler):

    def connetToDB(self):
        connection = pypyodbc.connect(driver='{SQL Server}', server='DESKTOP-7GE22QK\SQLEXPRESS',
                                      database='Library')
        return connection

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()


    def do_GET(self):
        DataDic = dict()
        DataMass = []
        if self.path == '/data':
            cursor = self.connetToDB().cursor()
            self._set_headers()
            SQLQuery = ("""Select Books.ID_Books, Books.Title, Books.Years, Books.Count_Downloads, Books.Description ,Books.Rating, Author.Name, Author.Surname, Books.src
                        From Books
                        Join BooksAuthor on Books.ID_Books = BooksAuthor.Code_Books
                        Join Author on BooksAuthor.Code_Author = Author.ID_Author""")
            cursor.execute(SQLQuery)
            result = cursor.fetchall()
            self.connetToDB().close()
            for i in result:
                DataDic['id'] = str(i[0])
                DataDic['name'] = str(i[1])
                DataDic['year'] = str(i[2])
                DataDic['numOfDownloads'] = str(i[3])
                DataDic['short_description'] = str(i[4])
                DataDic['numOfLikes'] = str(i[5])
                DataDic['author'] = str(i[6]) + ' ' + str(i[7])
                DataDic['src'] = str(i[8])
                DataMass.append(DataDic)
                DataDic = {}
            data = json.dumps(DataMass)
            self.wfile.write(bytes(str(data).encode()))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        DataDic = dict()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Begin the response

        # print('Client: {}\n'.format(self.client_address))
        # print('User-agent: {}\n'.format(
        #     self.headers['user-agent']))
        # print('Path: {}\n'.format(self.path))
        # print('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                print('\tUploaded {} as {!r} ({} bytes)\n'.format(field, field_item.filename, file_len))
            else:
                # Regular form value
                print('\t{}={}\n'.format(
                    field, form[field].value))
                DataDic[field] = form[field].value
        print(DataDic)
        login = str()
        password = str()
        email = str()
        leng = len(DataDic)



        """++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"""

        if leng == 3:
            for key, value in DataDic.items():
                if key == 'login':
                    login = value
                if key == 'psw':
                    password = value
                if key == 'email':
                    email = value
            connection = pypyodbc.connect(driver='{SQL Server}', server='DESKTOP-7GE22QK\SQLEXPRESS',
                                          database='Library')
            cursor = connection.cursor()
            SQLQuery = ('INSERT INTO Client(User_Login, User_Password, Email, Code_Rank) VALUES(' + "'" + login + "'"
                        + ',' + "'" + password + "'" + ',' + "'" + email + "'" + ',' + "'1' )")
            try:
                cursor.execute(SQLQuery)
                connection.commit()
                self.send_response(201)
                self.send_header('Content-Type',
                                 'text/plain; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
            except:
                self.send_response(406)
                self.send_header('Content-Type',
                                 'text/plain; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
            connection.close()
            """____________________________________________________________________"""

        elif leng == 2:
            for key, value in DataDic.items():
                if key == 'login':
                    login = value
                if key == 'psw':
                    password = value







def run(server_class=HTTPServer, handler_class=Server, port=8080):
        host_name = socket.gethostbyname(socket.gethostname())
        server_address = (host_name, port)
        print(server_address)
        httpd = server_class(server_address, handler_class)
        print('Starting httpd on port %d :' % port)
        httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
