#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install matplotlib')
get_ipython().system('pip install reportlab')


# In[13]:


import matplotlib.pyplot as plt
from io import BytesIO
from pymongo import MongoClient
import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# In[14]:


client = MongoClient('mongodb+srv://sena:wersdf1425@cluster0.5ok5hne.mongodb.net/?retryWrites=true&w=majority')
db = client.analytics


# In[15]:


def get_event_counts(start_date, end_date):
    tracked_data = list(db.tracked.find({
        'timestamp': {'$gte': start_date, '$lte': end_date}
    }).sort("timestamp", -1))

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


def create_report(data):
    doc = SimpleDocTemplate("k.grafik_rapor.pdf", pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    title = "Event Count Report"
    elements.append(Paragraph(title, styles['Title']))

    for timestamp, camera_data in data.items():
        for uuid, counts in camera_data.items():
            camera_title = "Camera: {}".format(uuid)
            elements.append(Paragraph(camera_title, styles['Heading2']))

            plt.figure(figsize=(6, 3))
            identities = list(counts.keys())
            event_counts = list(counts.values())
            plt.bar(identities, event_counts)
            plt.xlabel('Identity')
            plt.ylabel('Event Count')
            plt.title('Event Counts for Camera: {}'.format(uuid))
            plt.xticks(rotation='vertical')
            plt.tight_layout()

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()

            img = Image(buffer)
            elements.append(img)
            elements.append(PageBreak())  
    
    doc.build(elements)


# In[17]:


one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)


# In[18]:


event_counts = get_event_counts(one_month_ago, datetime.datetime.now())


# In[19]:


create_report(event_counts)


# In[ ]:





# In[ ]:





# In[ ]:




