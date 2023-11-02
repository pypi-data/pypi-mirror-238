
# InfinityDB NoSQL DBMS REST Access

The infinitydb.access module provides a REST interface to the APIs
defined in the server by means of PatternQueries.
Each access point looks like:

`https://myserver.com:37411/infinitydb/data/my/db/"my.interface"/"myquery"?action=execute-query`

 Where my/db is the name of a database in the server, "my.interface"
 is the name of an interface in the server, and "myquery" is
 appended to the interface to uniquely identify the query.
 There can be JSON request content and response content as well.
 The user name and password are provided in the authentication
 header: 
 
 `Authorization: Basic <base64 credentials>`
 
 The actual access is done through the module's convenience
 functions. Also, the data representation of 'Items' is
 more general than JSON, so there are functions to
 convert from JSON to Python dicts and deal with
 tuples.
 
 See [boilerbay.com](https://boilerbay.com) for more.
 
