#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install pymongo')
get_ipython().system('pip install reportlab')


# In[5]:


from pymongo import MongoClient
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# In[7]:


client = MongoClient("mongodb+srv://sena:wersdf1425@cluster0.5ok5hne.mongodb.net/?retryWrites=true&w=majority")
db = client["analytics"]


# In[8]:


tracked_data = db.tracked.find({})


# In[10]:


counts = {}
for doc in tracked_data:
    boxes = doc["box"]
    for box in boxes:
        identity = box["identity"]
        counts[identity] = counts.get(identity, 0) + 1


# In[16]:


def create_report(data):
    doc = SimpleDocTemplate("rapor.pdf", pagesize=letter)
    elements =[]
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Count Report", styles["Title"]))
    
    table_data = [["Identity","Count"]]
    for identity , count in data.items():
        table_data.append([identity, count])
        
    table = Table(table_data, colWidths=[200, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    elements.append(table)
    
    doc.build(elements)


# In[17]:


create_report(counts)

