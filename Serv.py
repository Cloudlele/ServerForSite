from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import pypyodbc



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

    # GET sends back a Hello world message
    def do_GET(self):
        DataDic = dict()
        DataMass = []
        if self.path == '/data':
            cursor = self.connetToDB().cursor()
            self._set_headers()
            SQLQuery = ("""Select Books.ID_Book, Books.Title, Books.Years, Books.Count_Download, Books.Rating, Author.Name, Author.Surname
                        From Books
                        Join BooksAuthor on Books.ID_Book = BooksAuthor.Code_Books
                        Join Author on BooksAuthor.Code_Author = Author.ID_Author""")
            cursor.execute(SQLQuery)
            result = cursor.fetchall()
            self.connetToDB().close()
            for i in result:
                DataDic['ID_Books'] = str(i[0])
                DataDic['Title'] = str(i[1])
                DataDic['Years'] = str(i[2])
                DataDic['Count_Download'] = str(i[3])
                DataDic['Rating'] = str(i[4])
                DataDic['Author'] = str(i[5]) + ' ' + str(i[6])
                DataMass.append(DataDic)
                DataDic = {}
            data = json.dumps(DataMass)
            self.wfile.write(bytes(str(data).encode()))

    # POST echoes the message adding a JSON field
    def do_POST(self):
        content_len = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_len).decode('utf-8')
        print(post_body.strip().split())
        iter = int()
        for id, i in enumerate(post_body.split()):
            if 'name' in i:
                iter = id
            if id == iter + 1:
                print(i)

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
