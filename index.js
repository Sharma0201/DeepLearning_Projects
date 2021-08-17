function print(val)
{
	document.getElementById('demo').innerHTML = 'Hello'+ val;
}
function button_helper(mycallback)
{
	let str = ' world';
	mycallback(str);
}

function validator_()
{

	let x = document.getElementById("input").value;
	console.log(x);
	if(isNaN(x) || x<1 || x>10)	
	{
		alert("please insert the numerical value");
		console.log("here");
		
	}
	else
	{
		
		console.log("there");
		
	}
}

let x = document.getElementById('radio_summ');
x.addEventListener("click",summary_radio());
let y = document.getElementById('radio_qna');
y.addEventListener("click",QnA_radio())

function summary_radio()
{
	document.getElementById('demo').innerHTML = "summary";
}