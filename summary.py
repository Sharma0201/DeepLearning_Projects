#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from transformers import pipeline
from http.server import BaseHTTPRequestHandler, HTTPServer
import time


# In[ ]:

#summarizer pipeline
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
hostName = "127.0.0.1"
serverPort = 12345


# In[ ]:

#function to convert passage to summary
def recieve_text_to_summarize(passage):
    word_count = len(passage.split())
    summary = (summarizer(passage, min_length=5, max_length=word_count, do_sample=False))
    return summary[0]["summary_text"]


# In[ ]:

#map for cmd string to function pointer
cmd_to_function_map = {
    "summarize": recieve_text_to_summarize 
}


# In[ ]:

#http server, catering the microservice request
class MyServer(BaseHTTPRequestHandler):
#handking the GET request
    def do_GET(self):
        print("in get")
        summary = cmd_to_function_map["summarize"]("""The promise of deep learning is to discover rich, hierarchical models that represent probability""")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>" + summary + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
#handling the POST request  
    def do_POST(self):
        print("in post")
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # reading the data
        post_data_de = post_data.decode("utf-8") #convert string in byte form to str form
        print(post_data_de)
        #if post_data_de.count("summarize")>0:
        print(post_data_de[0:9])
        if post_data_de[0:9] == "summarize": #check if summarizer string is present
            print("inside summarize")
            summary = cmd_to_function_map["summarize"](post_data_de[12:]) #nlp function call
            print(summary)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>" + summary + "</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))
        else:
            print("summarize not presnt")
        #print(post_data)


# In[ ]:
#main method

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


# In[ ]:




