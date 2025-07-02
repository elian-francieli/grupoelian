Class Teste.RestPing Extends %CSP.REST
{

Parameter HandleCors = 1;

ClassMethod Ping() As %Status
{
    Set %response.ContentType = "application/json"
    Do %response.Write("{""result"":""Pong""}")
    Quit $$$OK
}

}