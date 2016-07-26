' VBA Script for getting data from NIWA data into an Excel worksheet
'
' Requires https://github.com/VBA-tools/VBA-JSON/blob/b6108e88f956f36397fe82cd805233898e734a73/JsonConverter.bas
' to convert JSON file to Dictionary object

Public Sub ReadJsonURL()
    Set MyRequest = CreateObject("WinHttp.WinHTTPRequest.5.1")
    MyRequest.Open "GET", "URL goes here", True
    MyRequest.SetCredentials “username”, “password”, HTTPREQUEST_SETCREDENTIALS_FOR_SERVER
    MyRequest.Send
    
    If MyRequest.waitForResponse(15) = True Then
        ReadJson (MyRequest.ResponseText)
    Else
        MsgBox "Failed to read data from URL"
    End If
    
End Sub
Public Sub ReadJSONFile()
    Dim FSO As New FileSystemObject
    Dim JsonTS As TextStream
    Dim JsonText As String
    
    ' Read .json file
    Set JsonTS = FSO.OpenTextFile(“filename.json", ForReading)
    JsonText = JsonTS.ReadAll
    JsonTS.Close
    
    ReadJson (JsonText)
    
End Sub

Private Sub ReadJson(sData As String)

Dim Parsed As Dictionary

' Parse json to Dictionary
' "values" is parsed as Collection
' each item in "values" is parsed as Dictionary
Set Parsed = JsonConverter.ParseJson(sData)

Dim arrPaste() As Variant
Total = Parsed("data").Count

ReDim arrPaste(1 To Total, 1 To 2)
iRow = 1

For Each skey In Parsed("data").Keys
    arrPaste(iRow, 1) = skey
    If skey <> "values" Then
        arrPaste(iRow, 2) = Parsed("data")(skey)
    End If
    iRow = iRow + 1
Next

With Sheets(1)
    .Range(.Cells(1, 1), .Cells(Total, 2)) = arrPaste
End With

Total2 = Parsed("data")("values").Count

ReDim arrPaste(1 To Total2, 1 To 2)
iRow = 1

For Each skey In Parsed("data")("values").Keys
    arrPaste(iRow, 1) = skey
    arrPaste(iRow, 2) = Parsed("data")("values")(skey)

    iRow = iRow + 1
Next

With Sheets(1)
    .Range(.Cells(Total + 2, 1), .Cells(Total + 1 + Total2, 2)) = arrPaste
End With

End Sub
