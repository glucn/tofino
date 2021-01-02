import spacy
from spacy.tokens.doc import Doc

nlp = spacy.load('en_core_web_md')

jd = """

 
 Completed Bachelor’s Degree in Supply Chain Management, Business Administration, Engineering, IT, or related field, OR 2+ years of Amazon experience
 
 
 3+ years of experience in supply chain operations
 
 
 1+ years’ experience using Microsoft Office, particularly Excel and analytical platforms, including but not limited to the ability to analyze data using pivots and V-Lookups.
 
 
 1+ years of people management experience
 
 
 Experience understanding process flow and suggest improvements to deliver cost savings, inventory reduction, or other benefits to the site.
 
 
 Supplier/ vendor relationship management experience
 
 
 
 At Amazon, we're working to be the most customer-centric company on earth. To get there, we need exceptionally talented, bright, and driven people. If you'd like to help us build the place to find and buy anything online, this is your chance to make history.
 
 
 As a Procurement Operations Analyst for the Amazon Fulfillment Center team, you will own the site’s indirect procurement operation responsibilities, including forecasting, inventory management, purchase order management and Vendor management of 3rd party service providers. You will lead supplier management KPI and metrics reporting, and work with stakeholders to find and understand deviation and improvement areas. You will provide procurement leadership and align with the building leadership team to drive efficiencies and improvements at the site(s).
 
 
 
 MAIN RESPONSIBILITIES:
 
 
 
 
 In partnership with the Procurement Operations Manager, provide procurement operations support for the fulfillment center, including: forecasting of non-inventory products, inventory management, non-inventory flow and space models, cycle counts, supplier management, procurement transaction and expediting support
 
 
 Lead team of non-inventory receivers to ensure building has adequate resources and is set up for success
 
 
 Develop deep knowledge of non-inventory items and align with like buildings to drive best practices
 
 
 Manage KPI to measure, control and benchmark procurement processes including creation of recurring metrics reports to drive improvements for the Operations network
 
 
 Develop relationship across the building and network to ensure best practices are being shared and implemented
 
 
 Align with internal customers, Finance and Procurement Operations to understand budgetary targets by building and develop methods of measuring and defining savings, value and other category metrics
 
 
 Using input from the category team, build the category metrics model to track and monitor performance in relationship to the category strategy
 
 
 Measure actual vs planned savings; as savings trends are identified, own action plans to meet goals and develop solutions
 
 
 Work in partnership both internally and with suppliers to develop innovative solutions to provide Procurement support to the Operations network
 
 
 Develop and implement ways to measure suppliers to drive continuous performance improvement on behalf of Amazon
 
 
 Coordinate the demand identification, procurement, and inventory management of all non-merchandise items required for building operation. This includes corrugate, packing materials, labor and janitorial services, etc.
 
 
 Partner with Category team to manage and maintain supplier scorecards
 
 
 
 . Partner with AP, Suppliers and various internal teams to ensure timely resolution of vendor payment issues
 
 
 
 Support the procurement operations and category management teams
 
 
 Work is done in a warehouse environment that requires frequent walking around the building. You should feel comfortable working in an environment with varying temperatures as many buildings have dock doors that open throughout shifts.
 
 
 Procurement experience preferred
 
 
 Experience in Coupa or other financial management/procurement software
 
 
 Experience with cost accounting
 
 
 Lean / Six-Sigma knowledge
 
 
 Must be highly self-motivated and customer-centric
 
 
 Ability to work with ambiguity
 
 
 Provide a positive customer experience internally and externally
 
 
 
 Amazon offers competitive packages including comprehensive health care, 401(k), restricted stock units, growth potential and a challenging and exciting work environment.
 
 
 Amazon is an Equal Opportunity Employer – Minority / Women / Disability / Veteran / Gender Identity / Sexual Orientation / Age
"""

def match_skill(doc: Doc):
    list = ['Excel']

    return doc

nlp.add_pipe()

doc = nlp(jd)

for ent in doc.ents:
    print(ent.text, ent.label_)
