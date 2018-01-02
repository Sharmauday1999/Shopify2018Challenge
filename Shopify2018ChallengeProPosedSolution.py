import json
import urllib

def initializeDictionaries(): #pulls JSON from URLs
    response1 = urllib.request.urlopen("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page=1")
    response2 = urllib.request.urlopen("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page=2")
    response3 = urllib.request.urlopen("https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=1&page=3")
    
    data1 = json.load(response1)
    data2 = json.load(response2)
    data3 = json.load(response3)
    return data1, data2, data3

def pullChildId(dict1,dict2,dict3): # pulls child IDs
    childIdList = []
    for i in range(5):
        if dict1['menus'][i]['child_ids'] == []:
            childIdList.append([])
        else:
            #for j in range(len(dict1['menus'][i]['child_ids'])):
            if len(dict1['menus'][i]['child_ids']) == 1:
                childIdList.append(dict1['menus'][i]['child_ids'][0])
            else:
                childIdList.append(dict1['menus'][i]['child_ids'])
    for i in range(5):
        if dict2['menus'][i]['child_ids'] == []:
            childIdList.append([])
        else:
            #for j in range(len(dict2['menus'][i]['child_ids'])):
            if len(dict2['menus'][i]['child_ids']) == 1:
                childIdList.append(int(dict2['menus'][i]['child_ids'][0]))
            else:
                childIdList.append(dict2['menus'][i]['child_ids'])
    for i in range(5):
        if dict3['menus'][i]['child_ids'] == []:
            childIdList.append([])
        else:
            #for j in range(len(dict3['menus'][i]['child_ids'])):
            if len(dict3['menus'][i]['child_ids']) == 1:
                childIdList.append(int(dict3['menus'][i]['child_ids'][0]))
            else:
                childIdList.append(dict3['menus'][i]['child_ids']) 
    return childIdList

def pullParentId(dict1,dict2,dict3): # pulls parent IDs
    parentIdList = []
    for i in range(5):
        if bool("parent_id" in dict1['menus'][i]):
            parentIdList.append(dict1['menus'][i]['parent_id'])
        else:
            parentIdList.append([])
    for i in range(5):
        if bool("parent_id" in dict2['menus'][i]):
            parentIdList.append(dict2['menus'][i]['parent_id'])
        else:
            parentIdList.append([])
    for i in range(5):
        if bool("parent_id" in dict3['menus'][i]):
            parentIdList.append(dict3['menus'][i]['parent_id'])
        else:
            parentIdList.append([])
    return parentIdList

def ItemValidator(childIdList,parentIdList): #validates menu items
    validIdList = []
    invalidIdList = []
    for i in childIdList:
        if type(i) == int:
            if childIdList.index(i) + 1 == parentIdList[i-1]:
                validIdList.append(childIdList.index(i)+1)
        elif type(i) == list and len(i) >= 1:
            for j in i:
                if  childIdList.index(i) + 1 == parentIdList[j-1]:
                    validIdList.append(childIdList.index(i)+1)
        elif i == []:
            None
        
    validIdList = list(set(validIdList))
    
    for i in range(15):
        if i + 1 not in validIdList:
            invalidIdList.append(i+1)
                    
    return validIdList,invalidIdList

def CreateDictionary(validIdList,invalidIdList,dict1,dict2,dict3): #creates final dictionsary
    finalDictionary ={"valid_menus": [] ,"invalid_menus": []}
    for i in validIdList:
        if 0 < i <= 5:
            finalDictionary["valid_menus"].append({"root_id": i, "children": dict1['menus'][i-1]['child_ids']})
        elif 5 < i <= 10:
            finalDictionary["valid_menus"].append({"root_id": i, "children": dict2['menus'][i-6]['child_ids']})
        elif 10 < i <= 15:
            finalDictionary["valid_menus"].append({"root_id": i, "children": dict3['menus'][i-11]['child_ids']})
    
    for i in invalidIdList:
        if 0 < i <= 5:
            finalDictionary["invalid_menus"].append({"root_id": i, "children": dict1['menus'][i-1]['child_ids']})
        elif 5 < i <= 10:
            finalDictionary["invalid_menus"].append({"root_id": i, "children": dict2['menus'][i-6]['child_ids']})
        elif 10 < i <= 15:
            finalDictionary["invalid_menus"].append({"root_id": i, "children": dict3['menus'][i-11]['child_ids']})
            
    return finalDictionary
    

def main():
    data1, data2, data3 = initializeDictionaries()
    
    childIdList = pullChildId(data1,data2,data3)
    parentIdList = pullParentId(data1,data2,data3)

    validIdList,invalidIdList =  ItemValidator(childIdList,parentIdList)
    
    print("Child id:", childIdList)
    print("Parent id:",parentIdList)
    print(validIdList)
    print(invalidIdList)
    
    finalDictionary = CreateDictionary(validIdList,invalidIdList,data1,data2,data3)
    
    print(json.dumps(finalDictionary))
    
    with open('data.json', 'w') as outfile:
        json.dump(finalDictionary, outfile)
    
main()
                
                
            
    