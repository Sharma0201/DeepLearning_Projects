#!/usr/bin/env python
# coding: utf-8

# In[15]:


from transformers import pipeline
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


# In[2]:


question_and_answer = pipeline("question-answering")


# In[27]:


hostName = "127.0.0.1"
serverPort = 3128


# In[8]:


mcontext = """You never saw such a commotion in all your life as when my Uncle Podger undertook to do a job. A picture would be waiting to be put up and Uncle Podger would say: ‘Oh, you leave that to me. Don’t you worry about that? I’ll do all that. Now you go and get me my hammer. You bring me the rule Tom, and I shall want the step – ladder and I had better have a kitchen chair too and Jim, you run round to Mr. Goggles and tell him Pa’s kind regards and hopes his leg’s better and will he lend him his spirit level? And don’t you go, Martha, because I shall want somebody to hold me the light, and when the girl comes back, she must go out again for a bit of picture – cord and Tom you come here I shall want you to hand me up the picture.’ And then he would lift up the picture and drop it and it would come out of the frame, and he would try to save the glass and cut himself and then he would spring round the room, looking for his handkerchief. He could not find his handkerchief, because it was in the pocket of the coat he had taken off, and he did not know where he had put the coat. The entire house had to leave off looking for his tools and start looking for his coat, while he would dance round and hinder them. ‘Doesn’t anybody in the whole house knows where my coat is? Six of you! You can’t find a coat!’ Then he’d get up and find that he had been sitting on it, and would call out. ‘Oh, you can give it up! I’ve found it myself now.’ When half an hour had been spent in tying up his finger, and a new glass had been got, and the tools, and the ladder, and the chair, and the candle had been brought, he would have another go, the whole family, including the girl and the charwoman, standing round in a semi-circle, ready to help. Two people would have to hold him there, and a fourth would hand him a nail, and a fifth would pass him up the hammer, and he would take hold of the nail, and drop it. “There!’ he would say, in an injured tone, ‘now the nail’s gone’. We would all have to go down on our knees and grovel for it, while he would stand on the chair, and grunt, and want to know if he was to be kept there all the evening. The nail would be found at last, but by that time he would have lost the hammer. “Where’s the hammer? Seven of you gaping round there and you don’t know what I did with the hammer?’ We would find the hammer and then he would have lost sight of the mark he had made on the wall. Each of us had to get up on the chair beside him and see if we could find it, and we would each discover it in a different place and he would call us all fools. And he would take the rule, and re-measure and find that he wanted half thirty – one and three-eighths inches from the corner, and would try to do it in his head, and go mad. And we would all try to do it in our heads and all arrive at different results, and the original number would be forgotten, and Uncle Podger would have to measure it again. He would use a bit of string this time and at the critical moment, when he was leaning over the chair at an angle of forty – five, and trying to reach a point on the wall, the string would slip, and down he would slide on the piano, a really fine musical effect being produced by the suddenness with which his head and body struck all the notes at the same time. At last, Uncle Podger would get the spot fixed again and put the point of the nail on it with his left hand and take the hammer in his right hand. And, with the first blow, he would smash his thumb, and drop the hammer with a yell, on somebody’s toes. Aunt Maria would observe that the next time Uncle Podger was going to hammer a nail into the wall;. she would go and spend a week with her mother while it was being done. ‘You women you make such a fuss over everything,’ Uncle Podger would reply. “I like doing a little job of this sort.’"""


# In[9]:


mquestion="""Give two words to describe Uncle Podger."""


# In[32]:


def QnA_function(context,question):
    result = question_and_answer(question=question, context=context)
    print("Answer:", result['answer'])
    print("Score:", result['score'])
    return result['answer']


# In[18]:


QnA_function(mcontext,mquestion)


# In[33]:


class MyServer(BaseHTTPRequestHandler):
    def do_POST(self):
        print("in POST") 
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        post_data_de = post_data.decode("utf-8")
        print(post_data_de)
        data = json.loads(post_data_de)
        m_context = data["context"]
        m_question = data["question"]
        answer = QnA_function(m_context,m_question)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
            #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>" + answer + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
        


# In[ ]:


if __name__ =="__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


# In[ ]:




