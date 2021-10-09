
theUrl = 'http://127.0.0.1:5000/laermliste'
window.larmliste = new Promise(res => {
    return res(httpGet(theUrl))
})  
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}



