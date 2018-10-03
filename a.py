import csv,pymysql

db = pymysql.connect("localhost","root","root","Inventory" )
sql_insert = "INSERT INTO devices( propertyID, propertyName, \
         labelType, cost, buyDate, yearMonths, custodian, \
         storagePlace, scrapped, InventoryStatus) \
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 

sql_search = "select propertyID from devices"

cursor = db.cursor()
propertyID=[]
# 開啟 CSV 檔案
with open('demo.csv', newline='') as csvfile:
  count=0
  InventoryStatus=0
  scrapped=0
  data=[]
  transfer=""
  insert_status=0
  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)
  # 以迴圈輸出每一列
  for row in rows:
    # remove ',' in cost
    for i in row[3]:
      if i != ',':
        transfer=transfer+i
    row[3]=transfer
    transfer=""
    # remove ' ' in propertyID
    for i in row[0]:
      if i != ' ':
        transfer=transfer+i
    row[0]=transfer
    transfer=""
    # replace '.' to '-' in buyDate
    for i in row[5]:
      if i == '.':
        transfer=transfer+'-'
      else:
        transfer=transfer+i
    row[5]=transfer
    transfer=""

    # create data for db
    if count > 2:
      data.append([row[0], row[1], row[2], int(row[3]), row[5],int(row[6]), row[7],\
                   row[9], scrapped, InventoryStatus ])
    count=count+1
  print('Excel data :')
  print(data)
  # search
  try:
    cursor.execute(sql_search)
    transfer = cursor.fetchall()
    for i in transfer:
      propertyID= propertyID+list(i)
    print('Now propertyID: ')
    print(propertyID) 
    transfer=""
  except:
    print('select error')

  # decide insert 
  for i in range(len(data)):
    # decide insert status
    for j in propertyID:
      if data[i][0] == j:
        insert_status = 1
    # insert data
    if insert_status ==0:
      try:
        print('Insert propertyID:')
        print(data[i][0])
        cursor.execute(sql_insert,data[i])
        db.commit()
      except:
        print('insert error')
        db.rollback() 
    insert_status = 0


