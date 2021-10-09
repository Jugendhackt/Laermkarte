theUrl = 'http://localhost:5000/laermliste'
a = httpGet(theUrl)
console.log(a)





function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}



