#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install reportlab')


# In[10]:


from pymongo import MongoClient
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, timedelta


# In[11]:


client = MongoClient('mongodb+srv://sena:wersdf1425@cluster0.5ok5hne.mongodb.net/?retryWrites=true&w=majority')
db = client.analytics


# In[12]:


one_month_ago = datetime.now() - timedelta(days=30)


# In[13]:


tracked_data = list(db.tracked.find({"timestamp": {"$gte": one_month_ago}}).sort("timestamp", -1))


# In[14]:


event_counts = {}
for doc in tracked_data:
    if 'timestamp' in doc and isinstance(doc['timestamp'], datetime):
        timestamp = doc['timestamp'].date()
        boxes = doc.get('box', [])
        
        for box in boxes:
            identity = box.get('identity')
            if identity is not None:
                if timestamp not in event_counts:
                    event_counts[timestamp] = {}
                if identity not in event_counts[timestamp]:
                    event_counts[timestamp][identity] = 0
                event_counts[timestamp][identity] += 1


# In[15]:


def create_pdf_report(data):
    doc = SimpleDocTemplate("aylik_rapor.pdf", pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Monthly Event Count Report", styles['Title']))

    for timestamp, counts in data.items():
        table_data = [['Date', 'Identity', 'Event Count']]
        for identity, count in counts.items():
            date_str = timestamp.strftime('%Y-%m-%d')
            table_data.append([date_str, identity, count])

        table = Table(table_data, colWidths=[100, 200, 100])
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

    doc.build(elements)


# In[16]:


create_pdf_report(event_counts)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




