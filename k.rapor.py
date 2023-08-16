#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install reportlab')


# In[13]:


from pymongo import MongoClient
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet


# In[14]:


client = MongoClient('mongodb+srv://sena:wersdf1425@cluster0.5ok5hne.mongodb.net/?retryWrites=true&w=majority')
db = client.analytics


# In[15]:


def get_event_counts(start_date, end_date):
    tracked_data = list(db.tracked.find({
        'timestamp': {'$gte': start_date, '$lte': end_date}
    }))

    event_counts = {}
    for doc in tracked_data:
        if 'timestamp' in doc and isinstance(doc['timestamp'], datetime.datetime):
            timestamp = doc['timestamp'].date()
            boxes = doc.get('box', [])
            for box in boxes:
                identity = box.get('identity', None)
                uuid = doc.get('uuid', None) 
                if identity is not None and uuid is not None:
                    if timestamp not in event_counts:
                        event_counts[timestamp] = {}
                    if uuid not in event_counts[timestamp]:
                        event_counts[timestamp][uuid] = {}
                    event_counts[timestamp][uuid][identity] = event_counts[timestamp][uuid].get(identity, 0) + 1

    return event_counts


# In[16]:


start_date_input = input("Başlangıç tarihini girin (yyyy-mm-dd): ")
end_date_input = input("Bitiş tarihini girin (yyyy-mm-dd): ")


# In[17]:


start_date = datetime.datetime.strptime(start_date_input, "%Y-%m-%d")
end_date = datetime.datetime.strptime(end_date_input, "%Y-%m-%d")


# In[18]:


event_counts = get_event_counts(start_date, end_date)


# In[19]:


def create_report(data, start_date, end_date):
    doc = SimpleDocTemplate("rapor.pdf", pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    title = "Event Count Report - {} / {}".format(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    elements.append(Paragraph(title, styles['Title']))

    for timestamp, camera_data in data.items():
        for uuid, counts in camera_data.items():
            camera_title = "Camera: {}".format(uuid)
            elements.append(Paragraph(camera_title, styles['Heading2']))
            table_data = [['Date', 'Identity', 'Event Count']]
            for identity, count in counts.items():
                table_data.append([timestamp.strftime("%Y-%m-%d"), identity, count])

            table = Table(table_data, colWidths=[100, 100, 200, 100])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            elements.append(table)
            elements.append(PageBreak())  
    
    doc.build(elements)


# In[20]:


create_report(event_counts, start_date, end_date)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




