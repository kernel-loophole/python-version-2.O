
from csv import excel
from datetime import date
import os
import re
import shutil
from turtle import color
from types import coroutine
from numpy import size

from sympy import E, N
import excel2json
from excel2json import convert_from_file
from venv import create
from itsdangerous import json
import pandas as pd
import openpyxl as xl
from openpyxl import workbook
import sys

from xlsm2json import excel2json

sys.setrecursionlimit(50000)
import pprint
import exceltojson
import xlwings as xw
from xlwings.constants import DeleteShiftDirection
import openpyxl
from openpyxl.utils.cell import coordinate_from_string
import re
from openpyxl.styles import Alignment, Font,Border,Side,PatternFill
from openpyxl.utils import get_column_letter
import pandas as pd
import json
import os
import warnings
from tqdm import tqdm
import os
import re
import pandas as pd
import openpyxl as xl
from openpyxl import workbook
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from fuzzywuzzy import fuzz, process
warnings.simplefilter(action='ignore', category=FutureWarning)

def excel2json(file,sheet,parent,sgCol):
    global mainData
    global main
    global commentTableStart
    main = xw.Book(file).sheets[sheet]
    mainData = main.range("A1").expand("table").value
    commentTableStart = [i for i,v in enumerate(mainData[0]) if v == "Comments"]
    if len(commentTableStart) == 0:
        commentTableStart = [0,0]
    else:
        commentTableStart = [0,commentTableStart[0]]
    data = []
    for line in tqdm(range(len(mainData))):
        for col in range(len(mainData[line])):
            if mainData.cell(line,col).value:
                data.append(createObj(line,col,0,parent,sgCol))
    return data

def getRangedValue(range):
    r = range.split(":")
    rangeData=[]
    for row in mainData[r[0]:r[1]]:
        rangeData.append([c.value for c in row])
        df = pd.DataFrame(rangeData).fillna("")
    return df.to_dict(orient="records")
calcDic = {"ביטוח חיים":["O42:Q46","S42:U46","S50:U54",],
"ביטוח אובדן כושר עבודה":["P43:AH52","P55:Z63",],
"ביטוח אחריות מקצועית":["P44:AE62"],
"ביטוח בריאות":["P45:AD53","P143:X152","P155:X161",],
"ביטוח דירה":["O42:Y81","O83:Q86",],
"ביטוחי רכב":["Y47:AC64","Y67:AC78","Y82:AC89","Y93:AA97","Y100:AA117","AE47:AG53","AE56:AG61","AE65:AG70","AE74:AG79","AE82:AG86","AE91:AG118","AI47:AK53","AI56:AK60","AI65:AK70","AH74:AK79","AI82:AK87","AI91:AK124","AM47:AO113","AQ47:AS1317"],
"ביטוח מחלות קשות":["O42:AE53"],
"ביטוח משכנתא":["S42:U46","S48:U102","W42:Y46","W48:Y54"],
'ביטוח נסיעות לחו"ל' :[ "Q50:S61","Q64:S75","Q78:S83"],
"ביטוח סיעודי" :[ "Q41:AE65"],
"ביטוח עסק" :[ "Q43:AG55","Q57:AF68",],
"ביטוח תאונות אישיות":["O45:S60"],
"הלוואות לכל-מטרה וחוץ-בנקאיות":["P32:R41"],
"הלוואות משכנתא":["P37:S47"],
}

MacroText = """Sub Create_Value_File()

    Dim sFilename As String
    Dim sFullPath As String
    sFilename = "ValueFile.xlsx" 'You can give a nem to save
     'Displaying the saveas dialog box
    sFullPath = Application.GetSaveAsFilename(ThisWorkbook.Path & "\" & sFilename, _
    "Excel files,*.xlsx", 1, "Select your folder and filename")
 
    'User didn't save a file
    If sFullPath = "False" Then Exit Sub
    
    'wApplication.DisplayAlerts = False
    Dim xRet As Boolean
    xRet = IsWorkBookOpen(sFilename)
    
     If xRet Then
        MsgBox "The Value file is open! Please close it for overwrite action", vbInformation, "File Is Open"
        Exit Sub
    End If
    
    Dim SourceSheet As Worksheet
    Set SourceSheet = Worksheets("Main")
    
    SourceSheet.Copy
    
    Dim DestSheet As Worksheet
    Set DestSheet = ActiveSheet
    
    With DestSheet.UsedRange
        .Value = SourceSheet.UsedRange.Value
        
    End With
    Set wbNew = ActiveWorkbook
    BreakAllLinks wbNew

    For Each cell In DestSheet.UsedRange
        
        If (Not IsEmpty(cell)) And IsNumeric(cell) And (InStr(cell.NumberFormat, ".")) <> 0 Then
            cell.Value = Round(cell.Value, Len(cell.NumberFormat) - InStr(cell.NumberFormat, "."))
            cell.Select
        End If
    Next
    
    On Error Resume Next
    For Each shp In DestSheet.Shapes
        shp.Select
        Debug.Print (shp.TextFrame2.HasText = msoFalse)
        If shp.TextFrame2.HasText = msoTrue Then
            If shp.TextFrame2.TextRange.Characters.Text = "Create Final File" Then
                shp.Delete
            
            'Exit For
            End If
        End If
    Next
    DestSheet.UsedRange.Find("*factors Wizard*", LookIn:=xlValues).Value = ""
    On Error GoTo 0
    
    
    wbNew.SaveAs sFullPath
    wbNew.Close True
    
    

End Sub

Sub BreakAllLinks(ByVal wb As Object)
    Dim Link As Variant, LinkType As Variant
    
    For Each LinkType In Array(xlLinkTypeExcelLinks, xlOLELinks, xlPublishers, xlSubscribers)
        If Not IsEmpty(wb.LinkSources(Type:=LinkType)) Then
            For Each Link In wb.LinkSources(Type:=LinkType)
                wb.BreakLink Name:=Link, Type:=LinkType
            Next Link
        End If
    Next LinkType
    wb.UpdateLinks = xlUpdateLinksNever
End Sub


Function IsWorkBookOpen(Name As String) As Boolean
    Dim xWb As Workbook
    On Error Resume Next
    Set xWb = Application.Workbooks.Item(Name)
    IsWorkBookOpen = (Not xWb Is Nothing)
End Function

Sub createButton(param As String)
    Worksheets("Main").Activate
    Dim cl As Range
    Dim btn As Shape
    Dim first As Range
    Dim second As Range
    
    Set cl = Range(param)
    Set first = Range(param).Offset(0, 1)
    Set second = Range(param).Offset(2, 1)
    Range(first, second).Merge
    Range(first, second).Value = "A link for downloading the factors wizard:"
    Range(first, second).Font.Color = vbBlue
    Range(first, second).Font.Size = 16
    Range(first, second).Font.Bold = True
    Set btn = ActiveSheet.Shapes.AddShape(msoShapeActionButtonCustom, cl.Left, cl.Top, 50, 55)
    btn.TextFrame.Characters.Text = "Create Final File"
    btn.TextFrame.HorizontalAlignment = xlHAlignCenter
    btn.TextFrame.VerticalAlignment = xlVAlignCenter
    btn.OnAction = "Create_Value_File"
    

End Sub
"""

def colnum(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


class NoSN(Exception):
    pass



def createObj(line,col,distance,parent,sgCol):
    commentIndex = 0
    if line >= int(commentTableStart[0]):
        commentIndex = commentTableStart[1]

    


    values = [c.value for c in [mainData.cell(line, i) for i in [i for i in range(col-distance, col)]] if c.value]
    if len(values) > 1:
        sn= values[0]
        name = values[1]
    else :
        if mainData.cell(line,col).value ==None:
            sn =""
            if len(values) > 0:
                name = values[0]
            else:
                name = ""
        else:
            sn=""
            name=""

    return {
        "Parent": str(parent),
    "serial_number": str(sn),
    "name": name,
    "Celladdress": main.cell(line,col).coordinate,
    "value": mainData.cell(line,col).value,
    "suggestion": str(mainData.cell(line,sgCol).value or "") if sgCol else "",
    "extra" : mainData.cell(line,col-1).value,
    "comments" : str(mainData.cell(line,commentIndex+1).value or "") if commentIndex else "",
    "comments_srno" : str(mainData.cell(line,commentIndex).value or "") if commentIndex else "",
    "editable_cell" : True if main.cell(line,col).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False
        }

def wizard(row,col,sgCol,distance):
    # print(mainData.cell(row,col))
    valueCell = mainData.cell(row,col)
    refCell = mainData.cell(row,col-1)
    
    destinationCell = mainData.cell(row,sgCol)
    destinationCell.font = Font(color="FF000080")
    destinationCell.alignment = Alignment(horizontal="center", vertical="center")

    passed= []


    def checkNormalize(valueCell,vdx,col=col ):
        index, name = tuple([i for i in main.range((valueCell.row,valueCell.column-2),(valueCell.row,valueCell.column-distance)).value if i])
        return df.loc[(normalizeDF['name'] == name) & (normalizeDF['col']==col)&(normalizeDF['id']==index),vdx].values[0]
        

    def errorCell(destinationCell=destinationCell):
        destinationCell.value = 'Cannot be rated'
        outlines(destinationCell)
        destinationCell.fill = PatternFill("solid", start_color="FFFFFF99")


    def outlines(destinationCell=destinationCell):
        destinationCell.border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))
    try:
        if type(refCell.value) in [float,int]:
            if (refCell.value > 0 )& (refCell.value < 1):
                destinationCell.value = "Do nothing - cannot be controlled"
                outlines(destinationCell)
            else:
                errorCell(destinationCell)
                
        if type(refCell.value) == str:
            if ((len(refCell.value.strip()) > 1) and any([True for s in   ["<","<<",'<<<',">",">",">"] if s in refCell.value.strip()])):            
                destinationCell.value = "Do nothing - cannot be controlled"
                outlines(destinationCell)
                destinationCell.fill = PatternFill("solid", start_color="FFfff2cc")
            elif ("שנת" in refCell.value) or (refCell.value.replace(' ','') == "<text>") or ("X" in refCell.value) :
                destinationCell.value = "Do nothing - cannot be controlled"
                outlines(destinationCell)
            elif refCell.value.strip() == "כן=5 / לא=0":
                # print(valueCell)
                if valueCell.value == 5:
                    destinationCell.value = "Do nothing, already perfect"
                    outlines(destinationCell)
                elif valueCell.value == 0:
                    destinationCell.value = "Turn your quality variable to Yes"
                    outlines(destinationCell)
            elif "-" in refCell.value:
                destinationCell.value = f"Improve website capability by {round(valueCell.value/int(refCell.value.split('-')[-1]),2)}"
                outlines(destinationCell)
            elif refCell.value.strip() == "NT":   
                outlines(destinationCell)
                try:
                    destinationCell.value = "Improve website capability by " + str(round(checkNormalize(valueCell,vdx='max')/valueCell.value,2))
                except:
                    errorCell(destinationCell)
            elif refCell.value.strip() == "NVT":   
                outlines(destinationCell)
                try:
                    destinationCell.value = "Improve website capability by " + str(round(checkNormalize(valueCell,vdx='min')/valueCell.value,2))
    
                except:
                    errorCell(destinationCell)
            elif refCell.value.strip() == "N":   
                outlines(destinationCell)
                if str(valueCell.value) == "0":
                    outlines(destinationCell)
                    destinationCell.value = 'Your quality parameter should be maximized'
                else:
                    try:
                        rate = checkNormalize(valueCell,idx="min")/valueCell.value
                        if rate == 1:
                            destinationCell.value = "Do nothing, already perfect"
                        else:
                            destinationCell.value = "Multiply your quality variable by " + str(round(rate,2))
                    except:
                        destinationCell.value = 'Your quality parameter should be maximized'
            elif refCell.value.strip() in ["NV","VN"]:
                outlines(destinationCell)
                if str(valueCell.value) == "0":
                    destinationCell.value = 'Your quality parameter should be minimized'
                else:
                    try:
                        rate = checkNormalize(valueCell,vdx='min')/valueCell.value
                        if rate == 1:
                            destinationCell.value = "Do nothing, already perfect"
                        else:
                            destinationCell.value = "Multiply your quality variable by " + str(round(rate,2))
                    except:
                        destinationCell.value = 'Your quality parameter should be minimized'
    except:
        errorCell(destinationCell)
        

def excel_to_json(filename):
    wb = xl.load_workbook(filename)
    ws = wb.active
    df = pd.DataFrame(ws)
    if not filename.endswith('.json'):
        
        with open(filename + '.json', 'w') as f:
            json.dump(df.to_json(), f)
    else:
        return df.to_json()
def read_from_workbook(filename):
    wb = xl.load_workbook(filename)
    ws = wb.active
    df = pd.DataFrame(ws)
    return df
def excel_coloring(df,filename):
    wb = xl.load_workbook(filename)
    ws = wb.active
    ws.title = 'Colored'
    
  
def display_data(df):
    print(df.all)
    
def get_column_data(df,column_name):
    return df[column_name]    
    


def make_remove(df,filename):
    
        
        
    
    count=0
    wb = xl.load_workbook(filename,read_only=False,data_only=True,keep_vba=True)
    ws = wb.active
    counter=0
    make_bold=[]
    for j in ws.columns:
        for i in j:
            # print(ws.cell(row=i.row, column=i.column).value)
            if ws.cell(row=i.row, column=i.column).value=="Global-Patent-Pending                                                                לוחות דרושים - פרילנסרים                             אם האתר לא כאן - האתר לא קיים!":
                
                ws.cell(row=i.row, column=i.column).value="Global-Patent-Pending"+"\n"+"לוחות דרושים - שכירים"
                ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
                
                append_str=str(i.coordinate[0])+str(i.coordinate[1])
                for k in append_str:
                    if k.isdigit():
                        append_str=append_str.replace(k,"")
                make_bold.append(append_str)
    # for i in make_bold[::]:
    #     print("colum is change",i)
    #     for j in ws[i]:
    #         if j.value =="Global-Patent-Pending                                                                לוחות דרושים - שכירים                              אם האתר לא כאן - האתר לא קיים!":
    #             # print(i.value.strip())
    #             print("in the if")  
    #             check_str=i.value.split()
    #             print(check_str)
                
                
    #             # print("final str is :")
              
    #             j.fill = xl.styles.PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
    #             j.value=check_str[0]
    #             j.font = xl.styles.Font(size=25,color="FFFFFF")
    #             j.alignment = xl.styles.Alignment(horizontal='center', vertical='center')
            
    #         # print(check_str)
    #         # print(i.value)   
    
    
    try:
        for i in ws['E']:
            
            if i.value != None:
                # print(i.value)
                check_digit=i.value
                if check_digit.isdigit():
                    
                    ws.cell(row=i.row, column=i.column).font = xl.styles.Font(bold=True)
                    # ws.cell(row=i.row, column=i.column).fill = xl.styles.PatternFill(fgColor="8B4513", bgColor="8B4513", fill_type="solid")      
                    # ws.row_dimensions[i.row].height = 30
                else:
                    ws.cell(row=i.row, column=i.column).font = xl.styles.Font(bold=True)
                    ws.cell(row=i.row, column=i.column).fill = xl.styles.PatternFill(fgColor="FFFFFF", bgColor="FFFFFF", fill_type="solid")
                    ws.row_dimensions[i.row].height = 30
                
            else:
                # ws.row_dimensions[i.row].height = 12
                continue
                # ws.cell(row=i.row, column=i.column).fill = xl.styles.PatternFill(fgColor="FF0000", bgColor="FF0000", fill_type="solid")
        
    except :
        print("error while loading the file")
    for i in ws['AJ']:
        if i.value=="הערות לטופס והמלצות לשיפורו: ":
            replace_str=i.value.split()
            i.value=replace_str[0]
            # print(replace_str)
                       
            
    
    for i in ws['E']:
            
        if i.value =="Global-Patent-Pending                                                                לוחות דרושים - שכירים                              אם האתר לא כאן - האתר לא קיים!":
            # print(i.value.strip())
            
            check_str=i.value.split()
            final_str=""                                                                                                                                                                                                                                                                                            
            final_str=check_str[0]+"\n"+"לוחות דרושים - שכירים"
                
            # print("final str is :")
            # print(final_str)
            i.fill = xl.styles.PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
            i.value=final_str
            i.font = xl.styles.Font(size=25,color="FFFFFF")
            i.alignment = xl.styles.Alignment(horizontal='center', vertical='center')
           
            # print(check_str)
            # print(i.value)   
            break
    counter=0
        
    for j in ws.rows:
        for i in j:
            # print(ws.cell(row=i.row, column=i.column).value)
            if ws.cell(row=i.row, column=i.column).value=="הערות לטופס והמלצות לשיפורו: ":
                counter+=1
                print(ws.cell(row=i.row, column=i.column).value)
                
                ws.cell(row=i.row, column=i.column).value=" והמלצות "
                # ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row, end_column=i.column+1)
                # # ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                # ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
                
                append_str=str(i.coordinate[0])+str(i.coordinate[1])
                for k in append_str:
                    if k.isdigit():
                        append_str=append_str.replace(k,"")
                make_bold.append(append_str)
    print(counter)
    counter=0
    for j in ws.rows:
        
        for i in j:
            
            # print(ws.cell(row=i.row, column=i.column).value)
            if ws.cell(row=i.row, column=i.column).value=="אבג":
                
                get_column_name=ws.cell(row=i.row+1, column=i.column)
                get_column_name=get_column_name.coordinate[0::]
                

                print("chaning is ",get_column_name)
                counter+=1
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+1, end_column=i.column+2)
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row, end_column=i.column+2)
                
                
                get_column_name=ws.cell(row=i.row, column=i.column+1)
                get_column_name=get_column_name.coordinate[0::]
                print(get_column_name)
                
                
                # ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+1, end_column=i.column+2)
                ws[get_column_name].fill=PatternFill(fgColor="FFFFFF", bgColor="7030A0", fill_type="solid")
                # # ws.cell(row=i.row, column=i.column+1).font=Font(size=11,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column+1).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
                # # ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                # ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
            if ws.cell(row=i.row, column=i.column).value=="דהו" :
                counter+=1
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+2, end_column=i.column+2)
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row, end_column=i.column+2)
                
                
                # ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+2, end_column=i.column+2)
                get_column_name=ws.cell(row=i.row, column=i.column+1)
                get_column_name=get_column_name.coordinate[0::]
                print(get_column_name)
                ws[get_column_name].fill=PatternFill(fgColor="FFFFFF", bgColor="FFFFFF", fill_type="solid")
                # ws[get_column_name].font=Font(size=11,color="7030A0")
                # # ws.cell(row=i.row, column=i.column+1).font=Font(size=11,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column+1).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
                # # ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                # ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
            if ws.cell(row=i.row, column=i.column).value=="dd/mm/yy":                
                get_column_name=ws.cell(row=i.row+1, column=i.column)
                get_column_name=get_column_name.coordinate[0::]
                

                print("chaning is ",get_column_name)
                counter+=1
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+1, end_column=i.column+2)
                ws[get_column_name].fill=PatternFill(fgColor="FFFFFF", bgColor="7030A0", fill_type="solid")
                # ws.cell(row=i.row, column=i.column+1).font=Font(size=11,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column+1).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
                # # ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                # ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
            if ws.cell(row=i.row, column=i.column).value=="tt:tt":
                counter+=1
                
                ws.merge_cells(start_row=i.row, start_column=i.column, end_row=i.row+2, end_column=i.column+2)
                get_column_name=ws.cell(row=i.row, column=i.column+1)
                get_column_name=get_column_name.coordinate[0::]
                print(get_column_name)
                ws[get_column_name].fill=PatternFill(fgColor="FFFFFF", bgColor="FFFFFF", fill_type="solid")
                ws[get_column_name].font=Font(size=11,color="7030A0")
                # ws.cell(row=i.row, column=i.column+1).font=Font(size=11,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column+1).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid")
                # # ws.cell(row=i.row, column=i.column).fill=PatternFill(fgColor="7030A0", bgColor="7030A0", fill_type="solid") 
                # ws.cell(row=i.row, column=i.column).font=Font(size=25,color="FFFFFF")
                # ws.cell(row=i.row, column=i.column).alignment=Alignment(horizontal='center',vertical='center')
                
                append_str=str(i.coordinate[0])+str(i.coordinate[1])
                for k in append_str:
                    if k.isdigit():
                        append_str=append_str.replace(k,"")
                make_bold.append(append_str)
    print(counter)
    # for i in ws.rows:
    #     for j in i:
        
    #         if j.value =='הבהרות למשתנים':
    #             print(j.row)
    column_list=[]
    
    
    for i in ws.columns:
        
        for j in i:
            
            if j.value =="הערות /הבהרות האתר" or j.value=="הערות /הבהרות למשתנים":
                
                
                append_str=str(j.coordinate[0])+str(j.coordinate[1])
                for k in append_str:
                    if k.isdigit():
                        append_str=append_str.replace(k,"")
                column_list.append(append_str)
    
    intergers_list=['0','1','2','3','4','5','6','7','8','9']
    for i in column_list:
        
        if i.endswith('0') or i.endswith('1') or i.endswith('2') or i.endswith('3') or i.endswith('4') or i.endswith('5') or i.endswith('6') or i.endswith('7') or i.endswith('8') or i.endswith('9'):
           continue
        else:
            for i in ws[i]:
                if i.value != None:
                    ws.cell(row=i.row, column=i.column).font = xl.styles.Font(bold=True)
                    ws.row_dimensions[i.row].height = 30
                
                
                else:
                    continue
                    
        
 
        
    # print("following sheets are appended with color")
    # print(wb.sheetnames)
    # print("file is update")
    # print("file is saved")
    wb.save(filename)
def get_index_value(df,column_name):
    return df.index.get_level_values(column_name)

    
def fatch_column_data(df,column_name):
    return df[column_name]
def json_file_production_from_excel(filename):
    df = read_from_workbook(filename)
    df.to_json("data.json")
    print("data.json is created")
def remove_null_from_json(filename):
    remove_str=[]
    with open(filename) as f:
        data = json.load(f)
        print(data)
        for i in data:
            if i.values() == None:
               print(i)
            for j in i:
                if i[j] == None:
                    print(j)
                    
                if j == None:
                    remove_str.append(i)
                    data.remove(i)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, sort_keys=True)
def json_to_excel(filename):
    df = pd.read_json(filename)
    df.to_excel(filename+".xlsx")
    print("data.xlsx is created")
def copy_files(source_file,destination_file):
    shutil.copy(source_file,destination_file)
    print("file is copied")

def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}
   

if __name__ == "__main__":
    input("enter to start")
    dir = os.getcwd()
    files  = [file for file in os.listdir(dir) if (file.endswith(".xlsm")) and "$" not in str(file)]
    print(len(files),"number of files found ")
    print("Processing the files")
    if len(files) == 0:
        print("no  excel file found in the directory")
        print("please check the current directory")
    # if len(files) > 0:
    #     print(len(files)," excel files found in the directory")
    #     print("following excel files are found in the directory")
    #     print(files)
    # if len(files) > 0:
    #     for file in tqdm(files):
    #         print(file)
    #         wb = openpyxl.load_workbook(file, read_only=False, keep_vba=False)
    #         wbData = openpyxl.load_workbook(file, data_only=True,read_only=False, keep_vba=False)
    #         sheetMain = [name for name in wb.sheetnames if name.lower() == 'main'][0]
    #         sheetNormalize = [name for name in wb.sheetnames if name.lower() == 'normalize'][0]
    #         main = wb[sheetMain]
    #         mainData = wbData[sheetMain]
    #         wbnormalize = wb[sheetNormalize]
    #         normalizeData = wbData[sheetNormalize]
    #         if 'startRow' in globals():
    #             del startRow
    #         if 'distance' in globals():
    #             del distance
    #         if 'lastl' in globals():
    #             del lastl
    #         if 'startl' in globals():
    #             del startl
    #         if 'ndistance' in globals():
    #             del ndistance

    #         #making Normalize Sheet usable
    #         endl = []
    #         for row in normalizeData.rows:
    #             header = False
    #             for cell in row:
    #                 if cell.value != None:
    #                     if str(cell.value).lower() == "max":
    #                         endl.append(cell.column+1)
    #                         if not ('ndistance' in globals()):
    #                             ndistance = cell.column+1 - 2
    #                         if not ('startl'  in globals()):
    #                             startl = cell.row +1
    #                         header=True
                        
    #             if header:
    #                 break

    #         c = None
    #         lrow = normalizeData.max_row
    #         while c == None:
    #             lrow -=1
    #             c = normalizeData.cell(lrow,endl[0]-1).value
                

    #         lnds =[]
    #         rows=[-1,]

    #         for col in endl:
    #             ndf = []
                
    #             for i in range(startl-1,lrow):

    #                 l = [a.value for a in [normalizeData.cell(i,c) for c in range(col-ndistance,col)] if a.value]
    #                 if (len(l) < 3) & (len(l) > 0):
    #                     x={}
    #                     x['max']= ""
    #                     x['avg']= ""
    #                     x['min']= ""
    #                     try:
    #                         x['name']= l[-1]
    #                     except:
    #                         x['name']= ""
    #                         x['id'] = ""
    #                     try:
    #                         x['id'] = l[-2]
    #                     except:
    #                         x['id']=""
    #                     x['row'] = i
    #                     x['col'] = int(col)
    #                     ndf.append(x)
                    
    #                 if len(l) > 3:
    #                     x={}
    #                     try:
    #                         x['max']= l[-1]
    #                     except:
    #                         x['max']= ""
    #                     try:
    #                         x['avg']= l[-2]
    #                     except:
    #                         x['avg']= ""
    #                     try:
    #                         x['min']= l[-3]
    #                     except:
    #                         x['min']= ""
    #                     try:
    #                         x['name']= l[-4]
    #                     except:
    #                         x['name']= ""
    #                         x['id'] = ""
    #                     try:
    #                         x['id'] = l[-5]
    #                     except:
    #                         x['id']=""
    #                     x['row'] = i
    #                     x['col'] = int(col)
    #                     ndf.append(x)

    #             df = pd.DataFrame.from_dict(ndf)
                
    #             lnds.append(df)
    #         df = pd.concat(lnds)
            
    #         normalizeDF = df
        
    #         #finding Anchors
    #         dataCol=[]
    #         suggestionCols=[]
    #         header = False
    #         comments = False
    #         extraComments = False
    #         suggestions = False
    #         calc = False
    #         for row in main.rows:
    #             rowValue = [v for v in row if v.value]
    #             if rowValue:
    #                 if calc == False:
    #                     for cell in rowValue:
    #                         if any([t for t in calcDic.keys() if fuzz.ratio(str(cell.value),t) > 95]):
    #                             calcTbls = calcDic[[t for t in calcDic.keys() if fuzz.ratio(str(cell.value),t) > 95][0]]
    #                     if [c for c in rowValue if "מחשבון" in str(c.value).replace(" ",'')] :
    #                         calc = [c for c in rowValue if "מחשבון" in str(c.value).replace(" ",'')][0].row
    #                         calc=True
                        
    #                 if header == False:
    #                     if [c for c in rowValue if (fuzz.ratio(str(c.value),'דירוג הרייטינג היחסי הכולל') > 95)]:

                            
    #                         dataCol= [c.column for c in rowValue if (c.data_type=="f") & (c.border.outline == True) ]
    #                         counfOfValueCols = dataCol
    #                         if not ('startRow' in globals()):
                                
    #                             startRow = row[0].row
    #                         if not ('distance' in globals()):
    #                             if len(dataCol) > 0:
    #                                 distance = dataCol[0] - 2
    #                             else:
    #                                 distance = 0
    #                             # distance = dataCol[0] - 2
    #                         header = True
    #                 if comments == False:
    #                     for cell in rowValue:
    #                         if len(re.findall("הערות",str(cell.value))) & len(re.findall("הבהרות",str(cell.value))) > 0:
    #                             if main.cell(cell.row+1,cell.column-1).value == None :
    #                                 commentTableStart= (cell.row+1,cell.column)
    #                             else:
    #                                 commentTableStart= (cell.row+1,cell.column-1)
    #                             break
    #                             comments = True
    #                 if extraComments == False:
    #                     for cell in rowValue:
    #                         if len(re.findall("הערות",str(cell.value))) & (len(re.findall("לטופס",str(cell.value))) > 0 or len(re.findall("לקובץ",str(cell.value))) > 0) :
    #                             lastl= cell.row -1
    #                             extcomments= cell.column+1
    #                             extraComments = True
    #                 if suggestions == False:
    #                     if [c for c in rowValue if (fuzz.ratio(str(c.value),"Website & Service improvement Guide") > 80)]:
    #                         suggestionCols= [c.column for c in rowValue if (fuzz.ratio(str(c.value),"Website & Service improvement Guide") > 80)]
    #                         suggestions = True

    #         #getting Last Line
    #         if 'lastl' not in globals():
    #             lastl = main.max_row
            
    #         rating_data=[]
    #         for col in dataCol:
    #             dataCells = [cell[0].row for cell in main.iter_rows(min_col=col,max_col=col, min_row=startRow) if cell[0]]
    #             datalist={}
    #             try:
    #                 l0 = list(set([coordinate_from_string(a)[1] for a in re.findall(r"[a-zA-Z]+\d+",main.cell(startRow,col).value)]))
    #             except:
    #                 print([coordinate_from_string(a)[1] for a in re.findall(r"[a-zA-Z]+\d+",main.cell(startRow,col).value)])
    #                 break
    #             l0 = [c for c in l0 if main.cell(c,col).value != None]
    #             l0.sort()
    #             mainLevels={}
    #             for i in range(len(l0)):
    #                 mainLevels[i+1] = {}
    #                 if i+1 < len(l0):
    #                     mainLevels[i+1]['data'] = (int(re.findall('\d+',str(main.cell(l0[i],col).value))[0])+1, int(re.findall('\d+',str(main.cell(l0[i+1],col).value))[0])-1)
    #                     mainLevels[i+1]['sum'] = re.findall('\d+',str(main.cell(l0[i],col).value))[0]
    #                 else :
    #                     mainLevels[i+1]['data'] = (int(re.findall('\d+',str(main.cell(l0[i],col).value))[0])+1,lastl)
    #                     mainLevels[i+1]['sum'] = re.findall('\d+',str(main.cell(l0[i],col).value))[0]

    #             datalist[0] = {
    #                 "Parent": 0,
    #             "serial_number": 0,
    #             "name": next((mainData.cell(startRow,i).value for i in [i for i in range(col-distance,col)] if mainData.cell(startRow,i).value)),
    #             "Celladdress": main.cell(startRow,col).coordinate,
    #             "value": mainData.cell(startRow,col).value,
    #             "suggestion": "",
    #             "extra" : "",
    #             "comments" : "",
    #             "comments_srno" : "",
    #             "editable_cell" : True if main.cell(startRow,col).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False
    #                 }
    #             for l in l0:
    #                 itemNumber = l0.index(l)+1
    #                 datalist[itemNumber] = createObj(line=l,col=col,distance=distance,parent=0,sgCol=int(suggestionCols[dataCol.index(col)]))
    #             rating_data.append(datalist)
    #             desiredRow = list(mainLevels.items())[0][1]['sum']
    #             desiredRow_last = list(mainLevels.items())[-1][1]['data'][1]
    #             for sn,data in mainLevels.items():
    #                 itemNumber +=1
    #                 datalist[itemNumber] = createObj(line=int(data['sum']),col=col,distance=distance,parent=sn,sgCol=int(suggestionCols[dataCol.index(col)]))
    #                 # desiredRow = int(data['sum'])
    #                 # print(int(data['sum']), col)
    #                 wizard(col=col,row=int(data['sum']),distance=distance,sgCol=int(suggestionCols[dataCol.index(col)]))
    #                 for i in range(data['data'][0],data['data'][1]):
    #                     # print(mainData.cell(i,col).value)
    #                     if mainData.cell(i,col).value or mainData.cell(i,col).value == 0:
    #                         try:
    #                             itemNumber +=1
    #                             wizard(col=col,row=i,distance=distance,sgCol=int(suggestionCols[dataCol.index(col)]))
    #                             datalist[itemNumber] = createObj(line=i,col=col,distance=distance,parent=datalist[itemNumber-1]['serial_number'],sgCol=int(suggestionCols[dataCol.index(col)]))
    #                         except NoSN:
    #                             itemNumber -=1
    #                             pass
    #         fillers = {}
    #         for row in main.iter_rows(min_row=lastl):
    #             rowValue = [c for c in row if c.data_type == "s" ]
    #             for c in rowValue:
    #                 if "שם" in c.value:
    #                     fillers['name'] = {"value":main.cell(c.row,c.column+1).value, "editable":True if main.cell(c.row,c.column+1).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}
    #                 elif "תאריך" in c.value:
    #                     fillers['date'] = {"value":main.cell(c.row,c.column+1).value, "editable":True if main.cell(c.row,c.column+1).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}
    #                 elif "תפקיד" in c.value:
    #                     fillers['position'] = {"value":main.cell(c.row,c.column+1).value, "editable":True if main.cell(c.row,c.column+1).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}
    #                 elif "שעה" in c.value:
    #                     fillers['time'] = {"value":main.cell(c.row,c.column+1).value, "editable":True if main.cell(c.row,c.column+1).fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}
    #         commentsn={}
    #         for row in main.iter_rows(min_row=lastl+1):
    #             done=False
    #             for cell in row:
    #                 if not done :
    #                     if cell.fill.start_color.index == 'FFFFFF99':
    #                         if cell.value != None:
    #                             if int(cell.value):
    #                                 commentsn[cell.value] ={
    #                                     "value":str(main.cell(cell.row,cell.column+1).value or ""),
    #                                     "editable":True
    #                                 }
    #                             done=True
                                

    #         dnormalize=[]
    #         col =0
    #         for index, row in normalizeDF.iterrows():
    #             noId=False
    #             noName=False
    #             dobjects = {}
    #             try:            
    #                 if row['col'] != str(col):
    #                     new = True
    #                 else:
    #                     new = False 
    #             except:
    #                 print('ee')

    #             try:
    #                 cells = [normalizeData.cell(int(row['row']),int(i)) for i in range(int(row['col'])-int(ndistance),int(row['col']))]
    #             except:
    #                 print(row)
    #                 print('er')

    #             try:
    #                 snCell = [cell for cell in cells if cell.value == row['id']][0]
    #             except:
                    
    #                 try:
    #                     snCell = [cell for cell in cells if cell.value == row['name']][0]
    #                     noName =True
    #                 except:
    #                     noName =True
    #                     noId=True
    #             try:
    #                 nameCell= [cell for cell in cells if cell.value == row['name']][0]
    #             except:
    #                 try:
    #                     nameCell= [cell for cell in cells if cell.value == row['id']][0]
    #                     noId=True
    #                 except:
    #                     noId=True
    #                     noName =True
    #             if snCell.font.bold or new:
    #                 dobjects[index]={"parent":0,
    #                                 "serial_number":"" if noId else snCell.value,
    #                                 "name":"" if noName else nameCell.value,
    #                                 "celladdress":nameCell.coordinate,
    #                                 "min" :{"celladdress": cells[-3].coordinate,
    #                                         "value": cells[-3].value,
    #                                         "editable":True if cells[-3].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False},
    #                                 "avg":{"celladdress": cells[-2].coordinate,
    #                                         "value": cells[-2].value,
    #                                         "editable":True if cells[-2].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False},
    #                                 'max':{"celladdress": cells[-1].coordinate,
    #                                         "value": cells[-1].value,
    #                                         "editable":True if cells[-1].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}
    #                             }
    #             else:
    #                 dobjects[i]={
    #                             "parent":pid,
    #                                 "serial_number":"" if noId else snCell.value,
    #                                 "name":"" if noName else nameCell.value,
    #                                 "celladdress":nameCell.coordinate,
    #                                 "min" :{"celladdress": cells[-3].coordinate,
    #                                         "value": cells[-3].value,
    #                                         "editable":True if cells[-3].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False},
    #                                 "avg":{"celladdress": cells[-2].coordinate,
    #                                         "value": cells[-2].value,
    #                                         "editable":True if cells[-2].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False},
    #                                 'max':{"celladdress": cells[-1].coordinate,
    #                                         "value": cells[-1].value,
    #                                         "editable":True if cells[-1].fill.start_color.index in ['FFFFFF99','FFC7FEBA'] else False}}
    #             pid = row['id']
    #             dnormalize.append(dobjects)           



    #         try:
    #             version = re.findall('\d.*',str(main.cell(2,2).value))[0]
    #         except:
    #             version =""
    #         jsonD = {"Version":version,
    #                 "formFiller" : fillers,
    #                 "generalComments" : commentsn,
    #                 "rating_data": rating_data,
    #                 "normalize":dnormalize,
    #                 }
    #         if calc :
    #             calcdict = {}
    #             calcdict['gui'] = {}
    #             for row in main.iter_rows(min_row=calc, max_row=startRow, max_col=dataCol[0]+1):
    #                 for cell in row:
    #                     if cell.value != None:
    #                         if str(cell.value).replace(" ","") != "מחשבון":
    #                             if main.cell(cell.row-1,cell.column) != None :
    #                                 if str(main.cell(cell.row-1,cell.column).value).replace(" ","") != "מחשבון" :
    #                                     if cell.fill.start_color.index != "00000000":
    #                                         calcdict['gui'][main.cell(cell.row-1,cell.column).value]=cell.value
                
    #             r =0
    #             for rng in calcTbls:
    #                 calcdict[r]= getRangedValue(rng)
    #                 r+=1
    #                 jsonD['calc'] = calcdict
    
            
                    
    #         if any([name for name in wb.sheetnames if name.lower() == 
    #                 'companies']):
    #             sheetcompanies = [name for name in wb.sheetnames if name.lower() == 'companies'][0]
    #             df = pd.DataFrame(wbData[sheetcompanies].values)
    #             df.columns = df.iloc[0,:]
    #             df = df.iloc[1:,:]
    #             df.set_index(list(df)[0])
    #             dlist= []
    #             df= df.reset_index(drop=True)
    #             for index, row in df.iterrows():
    #                 if len([c for c in row.values[1:] if c]) ==0:
    #                     dlist.append(index)
    #             df = df.drop(df.index[dlist])
    #             jsonD['companies'] = df.to_dict(orient="records")
                
    #         if any([name for name in wb.sheetnames if name.lower() == 'dbase']):
    #             sheetDBASE = [name for name in wb.sheetnames if name.lower() == 'dbase'][0]
    #             df = pd.DataFrame(wbData[sheetDBASE].values)
    #             jsonD['dbase'] = df.dropna(axis=1,how='all'  ).dropna(axis=0,how="all").to_dict(orient='records')
            
    #         if len(dataCol) ==1 :
    #             argo = 0
    #             while argo < lastl:
    #                 for row in mainData.iter_rows(min_row=int(mainLevels[1]['sum']), max_row=lastl, min_col=2,max_col=suggestionCols[0]):
    #                     if row[0].row == lastl:
    #                         break
    #                     for cell in row:
    #                         if len(str(cell.value).strip()) <1:
    #                             c.value=None                  
    #                     if all([c.value == None for c in row]) :
    #                         mainData.move_range(f"B{row[0].row +1 }:{get_column_letter(dataCol[0])}{lastl}", rows=-1)
    #                         mainData.move_range(f"{get_column_letter(suggestionCols[0])}{row[0].row +1 }:{get_column_letter(suggestionCols[0])}{lastl}", rows=-1)
    #                         mainData.move_range(f"{get_column_letter(commentTableStart[1])}{row[0].row +1 }:{get_column_letter(commentTableStart[1]+1)}{lastl}", rows=-1)
                            
    #                         lastl -=1
                            
    #                         break
    #                 argo = row[0].row

    #         places = []
    #         for m in suggestionCols:
    #             for row in mainData.iter_rows(min_row=lastl-2,min_col=m,max_col=m):
    #                 for cell in row:
    #                     if cell.value != None:
    #                         if "A link for downloading the" in str(cell.value):
    #                             # print(cell.row, colnum(m))
    #                             # mainData.merge_cells(f"{colnum(m)}{cell.row}:{colnum(m)}{cell.row + 2}")
    #                             places.append(f"{colnum(m -1)}{cell.row}")
    #         desiredCols = []
    #         for col in mainData.iter_cols(min_row=1, max_col=mainData.max_column, max_row=mainData.max_row):
    #             for cell_ in col:
    #                 if 'FFC7FEBA' in str(cell_.fill)[int(str(cell_.fill).find("rgb='")) + 5:int(str(cell_.fill).find("rgb='")) + 13]:
    #                     if col not in desiredCols:
    #                         desiredCols.append(col)
    #         for col_ in desiredCols:
    #             for item in col_:
    #                 if str(item.value).strip() == '+':
    #                     mainData[str(item.coordinate)] = ""

    #         if not os.path.isdir('./output'):
    #             os.mkdir('./output')
            
    #         if not os.path.isdir('./output/tmp'):
    #             os.mkdir('./output/tmp')

    #         with open(f"./output/{file.replace('.xlsm','.json')}",'w') as f:
    #             f.write(json.dumps(jsonD, indent=4))

    #         wbData.save(f'./output/tmp/tmp.xlsx')
    #         wbData.close()
    #         wb.close()
    #         book=openpyxl.load_workbook(f'./output/tmp/tmp.xlsx')
    #         book = xw.Book(f'./output/tmp/tmp.xlsx')
    #         sheet = book.sheets(sheetMain)
    #         merged = []
    #         for item in sheet.range((desiredRow, 1), (500, counfOfValueCols[0])):
    #             if item.merge_cells == True:
    #                 if sheet.range(item.address).merge_area not in merged:
    #                     merged.append(sheet.range(item.address).merge_area)
    #                     sheet.range(sheet.range(item.address).merge_area).unmerge()
    #                 # print(item.address)

    #             # print(items)
    #         # print(merged)

    #         xlmodule = book.api.VBProject.VBComponents.Add(1)
    #         xlmodule.CodeModule.AddFromString(MacroText)
            
    #         if len(counfOfValueCols) == 1:
    #             rng = sheet.range((desiredRow, 1), (desiredRow_last, counfOfValueCols[0])).value
    #             totalDeleted = 0
    #             for i, row in enumerate(rng):
    #                 i = i + int(desiredRow) - totalDeleted
    #                 if all(elem is None for elem in row):
    #                     for x in [chr(i_) for i_ in range(ord('A'), ord(colnum(counfOfValueCols[0] + 1)))]:
    #                         sheet.range(f'{x}{i}').api.Delete(DeleteShiftDirection.xlShiftUp)
    #                     totalDeleted += 1

    #         # for unmergedCell in merged:
    #         #     print(unmergedCell)
    #         #     print(unmergedCell.offset(0,totalDeleted))
    #         #     sheet.range(unmergedCell).offset(0, -totalDeleted).merge()
    #         #     print('***'*40)
    #         macro = book.macro("module1.createButton")
    #         for place in places:
    #             # print('PLACE', place)
    #             macro(place)



    #         book.save(f'{dir}/output/{file}')
    #         book.close()


    check=0
    if  not os.path.isdir('./output/'):
        
        os.mkdir("./output/")
    if not os.path.isdir('./output/update_json'):
        os.mkdir('./output/update_json')
        
    if os.path.isdir('./output/'):
        
        if not os.path.isdir('./output/final_output'):
            os.mkdir("./output/final_output")
            check=0
        for i in files:
            shutil.copy(f'{i}', f'./output/final_output/{i}')
    
    folder_name="./output/final_output"
    l=os.listdir(folder_name)
    print(l)
    check  = [file for file in l if (file.endswith(".xlsm")) and "$" not in str(file)]
    print(check)
    for i in tqdm(check):
        
    
        try:
            make_remove(read_from_workbook(r'./output/{0}'.format(i)), r'./output/{0}'.format(i))
        except Exception as e:
            print("follwoing file is corrupted",i)
            print(e)    
            continue
        try:
            excel_data=pd.read_excel(r'./output/{0}'.format(i),sheet_name="Main")
        except:
            excel_data=pd.read_excel(r'./output/{0}'.format(i),sheet_name="MAIN")
            pass
                    
        json_str=excel_data.to_json(orient='records')
            
        if len(json_str)>0:
                
            with open(r'./output/update_json/{0}.json'.format(i[::4]),'w') as f:
                json.dump(json.loads(json_str),f,indent=4,sort_keys=True)
            with open(r'./output/update_json/{0}.json'.format(i[::4]),'r') as f:
                data = json.load(f)
                data = remove_empty_elements(data)
            with open(i[::4]+".json",'w') as f:
                json.dump(data,f,indent=4,sort_keys=True)
                # print(data)
        
        # print("json file is created")
        # print("json file is saved")
    print("files are modified")
    input("enter to exit")