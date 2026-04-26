import csv
import io

data = """1	Hostel	What are the main gate timings?	The main gate closes at 10:00 PM. Late entries require a written permit from the warden.
2	Hostel	How do I report a maintenance issue?	Log into the Student Portal under 'Maintenance' or write in the register kept at the hostel warden's office.
3	Hostel	Are guests allowed in rooms?	Day guests are allowed until 6:00 PM. Overnight stays are strictly prohibited without prior Dean of Students approval.
4	Hostel	What appliances are banned?	Electric heaters, induction stoves, and air conditioners are prohibited due to fire safety regulations.
5	Hostel	Where is the laundry facility?	The laundry room is located in the basement of Block B, open from 8:00 AM to 8:00 PM.
6	Academics	What is the minimum attendance?	Students must maintain at least 75% attendance in each subject to be eligible for final exams.
7	Academics	How do I apply for a leave?	Submit a leave application through the ERP portal at least 24 hours in advance for planned absences.
8	Academics	Where is the exam schedule?	The official timetable is posted on the college notice board and emailed to students 15 days before exams start.
9	Academics	How is the CGPA calculated?	CGPA is the weighted average of your grade points across all semesters. Check the Student Handbook for the formula.
10	Academics	Can I change my elective?	Elective changes are permitted only within the first week of the semester via the Registrar's office.
11	Library	What are the library hours?	The library is open Monday–Saturday, 9:00 AM to 9:00 PM. During finals, it stays open until midnight.
12	Library	How many books can I borrow?	Undergraduates can borrow up to 4 books for a period of 14 days.
13	Library	Is there a fine for late books?	Yes, a fine of ₹10 per day is charged for books returned after the due date.
14	Library	How do I access E-journals?	Use your student ID to log into the library portal (OPAC) from any campus Wi-Fi network.
15	Library	Are there private study rooms?	Yes, group study rooms are available on the 3rd floor and can be booked at the front desk.
16	Dining	What are the mess timings?	Breakfast: 7:30-9:00 AM; Lunch: 12:30-2:00 PM; Snacks: 5:00-6:00 PM; Dinner: 7:30-9:00 PM.
17	Dining	Can I skip the mess fee?	Mess fees are mandatory for all residents. Rebates are only given for absences exceeding 5 consecutive days.
18	Dining	Is there a night canteen?	Yes, the cafeteria near the Sports Complex is open until 2:00 AM for snacks and beverages.
19	Dining	Who do I contact for food quality?	Please report concerns to the Mess Committee or drop a note in the suggestion box at the entrance.
20	Dining	Are outside deliveries allowed?	Yes, food delivery is allowed but must be collected at the Main Gate security post.
21	IT Support	How do I connect to Wi-Fi?	Select the 'Campus_WiFi' network and log in using your Roll Number and system password.
22	IT Support	I forgot my portal password.	Click 'Forgot Password' on the login page or visit the IT Helpdesk in the Admin Block.
23	IT Support	Where can I print documents?	Printing stations are available in the Library and the Computer Lab on the 1st floor.
24	IT Support	Is there a student email ID?	Yes, every student is issued a @college.edu email. Check your admission kit for login details.
25	IT Support	Can I use the lab after hours?	Late-night lab access requires a signed letter of recommendation from your HOD.
26	Medical	Where is the health center?	The Medical Room is located next to the Girls' Hostel and is staffed 24/7 by a nurse.
27	Medical	What if there is an emergency?	Call the campus ambulance at 9999-XXX-XXX or notify the nearest security guard immediately.
28	Medical	Is the doctor available daily?	The general physician visits Monday–Friday from 4:00 PM to 6:00 PM.
29	Medical	Does the college provide insurance?	Yes, all enrolled students are covered under a basic Group Medical Insurance policy.
30	Medical	Where is the nearest pharmacy?	The campus store stocks basic OTC medicine. The nearest 24hr pharmacy is 1km outside the gate.
31	Finance	When is the fee deadline?	Semester fees must be paid within 10 days of the session start to avoid late fines.
32	Finance	Can I pay fees in installments?	Installment requests must be submitted to the Accounts Office for approval before the deadline.
33	Finance	Where do I get a fee receipt?	Receipts are generated automatically on the ERP portal after a successful transaction.
34	Finance	Are there merit scholarships?	Yes, students in the top 5% of their branch receive a tuition waiver. Applications open in October.
35	Finance	How do I claim a security deposit?	Deposits are refunded only after graduation and upon submission of the 'No Dues' certificate.
36	Campus Life	How do I join a club?	You can sign up during the 'Club Fair' held in the first month of the academic year.
37	Campus Life	Where is the Lost and Found?	Items found on campus should be deposited at the Main Security Office in the Admin Block.
38	Campus Life	Is there a gym on campus?	Yes, the gym is in the Sports Center. Monthly membership is ₹200 for students.
39	Campus Life	Can I bring a vehicle?	Only 2-wheelers are allowed for students. You must register your vehicle at the security office.
40	Campus Life	Where is the ATM?	There is an HDFC Bank ATM located right next to the Cafeteria.
41	Placements	Who is the placement head?	Prof. [Name] is the Head of Training & Placements. The office is on the 2nd floor, Admin Block.
42	Placements	When do internships start?	Summer internship drives typically begin in January for the following June break.
43	Placements	What is the dress code for interviews?	Business formal attire is mandatory for all placement activities and guest lectures.
44	Placements	How do I register for placements?	Final year students must register via the Placement Portal and upload a verified resume.
45	Placements	Are there mock interviews?	Yes, the Career Cell organizes mock interviews and GD sessions every Saturday.
46	General	What is the college address?	[Insert College Name], [Street], [City], [State], [Zip Code].
47	General	How do I contact the Principal?	Meetings are by appointment only. Email secretary@college.edu to request a time.
48	General	Is the campus ragging-free?	Yes, the college has a zero-tolerance policy. Report issues to the Anti-Ragging Squad immediately.
49	General	Where can I get an ID card?	New or replacement ID cards are issued at the Registrar’s Office. Replacement fee is ₹500.
50	General	Is there a campus shuttle?	Yes, a shuttle runs from the Main Gate to the Metro Station every 30 minutes."""

    output_file = os.path.join(os.path.dirname(__file__), "../data/faqs.csv")

# Load into CSV
rows = []
for line in data.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) == 4:
        # topic, question, answer
        rows.append([parts[1].lower(), parts[2], parts[3]])

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['topic', 'question', 'answer'])
    writer.writerows(rows)

print(f"Successfully wrote {len(rows)} entries to {output_file}")
