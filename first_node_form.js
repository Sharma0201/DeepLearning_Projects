var http = require('http');
var formidable = require('formidable');
var fs = require('fs');
const axios = require('axios');
const { StringDecoder }  = require('string_decoder');


//create a server using http module

http.createServer(function (req, res) {
	var summary_data = '';
	const decoder = new StringDecoder('utf8');
	//form file upload concept
  if (req.url == '/' && req.method.toLowerCase()=="post") {
	  console.log("/fileupload");
    var form = new formidable.IncomingForm();
	//form parser
    form.parse(req, function (err, fields, files) {
		//var oldpath = files.filetoupload.path;
		
		//res.writeHead(200, { 'Content-Type': 'application/json' });
      //res.end(JSON.stringify({ fields, files }, null, 2));
	  var data =  fields.description;
	  var radio_input = fields.input_type;
	  //console.log(radio_input);
	  //console.log("hello world");
	  //console.log(decoder.write(data));
	  //console.log(data);
		//opening and reading the uploaded file
		/*fs.readFile(oldpath, 'utf8' , (err, data) => {
		  if (err) {
			console.error(err)
			return
		  }
		  */
		  //post request to nlp server
		  console.log(data);
		  axios
			  .post('http://127.0.0.1:12345', "summarize : " + data)
			  .then(res => {
				console.log(`statusCode: ${res.status}`)
				console.log(res.data)
				//data recieved from nlp endpoint
				summary_data = res.data
			  })
			  .catch(error => {
				console.error(error)
			  })
		
     // res.write('File uploaded');
	  //as nodejs is async, it calls the nlp endpoint and move to res.end(), because of it, we were not able to post the the summary data on the web page, hence to sync it, we are waiting till the summary data is not empty
	 var _flagCheck = setInterval(function() {
			if (summary_data !== '') {
				clearInterval(_flagCheck);
				//ressponse to web client
				res.writeHead(200, {'Content-Type': 'text/html'});
				res.write(summary_data); // the function to run once all flags are true
				res.end();
			}
		}, 100); // interval set at 100 milliseconds

	  
	  
      
    });
  } 
  //html form, uploading txt file and post it to server
  else if(req.url=="/QnA" && req.method.toLowerCase()=="get")
  {
	 console.log("In QnA server");
	 fs.readFile("QnA.html",function(error,pgResp)
	 {
		 res.writeHead(200,{'Content-Type':'text/html'});
		 res.write(pgResp);
		 return res.end();
	 })
  }
  else {
	  console.log("/ request");
    //res.writeHead(200, {'Content-Type': 'text/html'});
	fs.readFile("index.html", function (error, pgResp) {
		res.writeHead(200, { 'Content-Type': 'text/html' });
		res.write(pgResp);
		return res.end();
	});
   /* res.write('<form action="fileupload" method="post" enctype="multipart/form-data">');
    res.write('<input type="file" name="filetoupload"><br>');
    res.write('<input type="submit">');
    res.write('</form>');
    res.end();*/
  }
}).listen(8080); 