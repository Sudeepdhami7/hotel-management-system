import random
from tkinter import *
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk


class Cus_Win:

    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x580+230+220")

        # ---------------- variables ----------------
        self.var_ref = StringVar()
        x = random.randint(1000, 9999)
        self.var_ref.set(str(x))

        self.var_cust_name = StringVar()

        # Master Global Address Data (Provinces/States & Districts/Cities)
        self.global_address_data = {
            "Nepalese": {
                "Koshi Province": [
                    "Bhojpur",
                    "Dhankuta",
                    "Ilam",
                    "Jhapa",
                    "Khotang",
                    "Morang",
                    "Okhaldhunga",
                    "Panchthar",
                    "Sankhuwasabha",
                    "Solukhumbu",
                    "Sunsari",
                    "Taplejung",
                    "Terhathum",
                    "Udayapur",
                ],
                "Madhesh Province": [
                    "Bara",
                    "Dhanusha",
                    "Mahottari",
                    "Parsa",
                    "Rautahat",
                    "Saptari",
                    "Sarlahi",
                    "Siraha",
                ],
                "Bagmati Province": [
                    "Bhaktapur",
                    "Chitwan",
                    "Dhading",
                    "Dolakha",
                    "Kathmandu",
                    "Kavrepalanchok",
                    "Lalitpur",
                    "Makwanpur",
                    "Nuwakot",
                    "Ramechhap",
                    "Rasuwa",
                    "Sindhuli",
                    "Sindhupalchok",
                ],
                "Gandaki Province": [
                    "Baglung",
                    "Gorkha",
                    "Kaski",
                    "Lamjung",
                    "Manang",
                    "Mustang",
                    "Myagdi",
                    "Nawalpur",
                    "Parbat",
                    "Syangja",
                    "Tanahun",
                ],
                "Lumbini Province": [
                    "Arghakhanchi",
                    "Banke",
                    "Bardiya",
                    "Dang",
                    "Gulmi",
                    "Kapilvastu",
                    "Parasi",
                    "Palpa",
                    "Pyuthan",
                    "Rolpa",
                    "Rukum East",
                    "Rupandehi",
                ],
                "Karnali Province": [
                    "Dailekh",
                    "Dolpa",
                    "Humla",
                    "Jajarkot",
                    "Jumla",
                    "Kalikot",
                    "Mugu",
                    "Rukum West",
                    "Salyan",
                    "Surkhet",
                ],
                "Sudurpashchim Province": [
                    "Achham",
                    "Baitadi",
                    "Bajhang",
                    "Bajura",
                    "Dadeldhura",
                    "Darchula",
                    "Doti",
                    "Kailali",
                    "Kanchanpur",
                ],
            },
            "Indian": {
                "Maharashtra": [
                    "Mumbai",
                    "Pune",
                    "Nagpur",
                    "Thane",
                    "Nashik",
                    "Aurangabad",
                ],
                "Delhi": [
                    "New Delhi",
                    "North Delhi",
                    "South Delhi",
                    "East Delhi",
                    "West Delhi",
                ],
                "Punjab": [
                    "Amritsar",
                    "Ludhiana",
                    "Jalandhar",
                    "Patiala",
                    "Bathinda",
                    "Mohali",
                ],
                "Karnataka": [
                    "Bengaluru",
                    "Mysuru",
                    "Mangaluru",
                    "Hubballi",
                    "Belagavi",
                ],
                "Tamil Nadu": [
                    "Chennai",
                    "Coimbatore",
                    "Madurai",
                    "Tiruchirappalli",
                    "Salem",
                ],
                "Uttar Pradesh": [
                    "Lucknow",
                    "Kanpur",
                    "Varanasi",
                    "Agra",
                    "Noida",
                    "Ghaziabad",
                ],
                "West Bengal": [
                    "Kolkata",
                    "Howrah",
                    "Darjeeling",
                    "Siliguri",
                    "Asansol",
                ],
                "Gujarat": [
                    "Ahmedabad",
                    "Surat",
                    "Vadodara",
                    "Rajkot",
                    "Gandhinagar",
                ],
            },
            "American": {
                "California": [
                    "Los Angeles",
                    "San Francisco",
                    "San Diego",
                    "San Jose",
                ],
                "New York": [
                    "New York City",
                    "Buffalo",
                    "Rochester",
                    "Albany",
                ],
                "Texas": ["Houston", "Dallas", "Austin", "San Antonio"],
                "Florida": ["Miami", "Orlando", "Tampa", "Jacksonville"],
                "Illinois": ["Chicago", "Aurora", "Naperville", "Joliet"],
            },
            "British": {
                "England": [
                    "London",
                    "Manchester",
                    "Birmingham",
                    "Liverpool",
                    "Leeds",
                ],
                "Scotland": [
                    "Edinburgh",
                    "Glasgow",
                    "Aberdeen",
                    "Dundee",
                ],
                "Wales": ["Cardiff", "Swansea", "Newport", "Bangor"],
                "Northern Ireland": [
                    "Belfast",
                    "Derry",
                    "Lisburn",
                    "Newry",
                ],
            },
            "Bangladeshi": {
                "Dhaka Division": [
                    "Dhaka",
                    "Gazipur",
                    "Narayanganj",
                    "Tangail",
                ],
                "Chittagong Division": [
                    "Chittagong",
                    "Cox's Bazar",
                    "Comilla",
                    "Feni",
                ],
                "Rajshahi Division": [
                    "Rajshahi",
                    "Bogra",
                    "Pabna",
                    "Natore",
                ],
                "Sylhet Division": [
                    "Sylhet",
                    "Moulvibazar",
                    "Habiganj",
                    "Sunamganj",
                ],
            },
            "Pakistani": {
                "Punjab": [
                    "Lahore",
                    "Faisalabad",
                    "Rawalpindi",
                    "Multan",
                    "Gujranwala",
                ],
                "Sindh": ["Karachi", "Hyderabad", "Sukkur", "Larkana"],
                "Khyber Pakhtunkhwa": [
                    "Peshawar",
                    "Abbottabad",
                    "Mardan",
                    "Swat",
                ],
                "Balochistan": ["Quetta", "Gwadar", "Turbat", "Khuzdar"],
            },
            "Chinese": {
                "Guangdong": [
                    "Guangzhou",
                    "Shenzhen",
                    "Dongguan",
                    "Foshan",
                ],
                "Zhejiang": ["Hangzhou", "Ningbo", "Wenzhou", "Jiaxing"],
                "Jiangsu": ["Nanjing", "Suzhou", "Wuxi", "Changzhou"],
                "Beijing Municipality": [
                    "Chaoyang",
                    "Haidian",
                    "Dongcheng",
                    "Xicheng",
                ],
                "Shanghai Municipality": [
                    "Pudong",
                    "Huangpu",
                    "Xuhui",
                    "Jingan",
                ],
            },
            "Japanese": {
                "Tokyo Metropolis": [
                    "Shinjuku",
                    "Shibuya",
                    "Minato",
                    "Chiyoda",
                ],
                "Osaka Prefecture": ["Osaka City", "Sakai", "Higashiosaka"],
                "Kanagawa Prefecture": [
                    "Yokohama",
                    "Kawasaki",
                    "Sagamihara",
                ],
                "Aichi Prefecture": ["Nagoya", "Toyota", "Okazaki"],
                "Hokkaido Prefecture": [
                    "Sapporo",
                    "Asahikawa",
                    "Hakodate",
                ],
            },
            "Australian": {
                "New South Wales": [
                    "Sydney",
                    "Newcastle",
                    "Wollongong",
                ],
                "Victoria": ["Melbourne", "Geelong", "Ballarat"],
                "Queensland": ["Brisbane", "Gold Coast", "Cairns"],
                "Western Australia": ["Perth", "Mandurah", "Bunbury"],
            },
            "Canadian": {
                "Ontario": ["Toronto", "Ottawa", "Hamilton", "London"],
                "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau"],
                "British Columbia": [
                    "Vancouver",
                    "Victoria",
                    "Surrey",
                    "Burnaby",
                ],
                "Alberta": ["Calgary", "Edmonton", "Red Deer"],
            },
            "Emirati": {
                "Abu Dhabi": ["Abu Dhabi City", "Al Ain", "Al Dhafra"],
                "Dubai": ["Deira", "Bur Dubai", "Downtown Dubai", "Jumeirah"],
                "Sharjah": ["Sharjah City", "Khor Fakkan", "Kalba"],
                "Ajman": ["Ajman City", "Manama", "Masfout"],
            },
            "Saudi": {
                "Riyadh Region": ["Riyadh", "Al Kharj", "Diriyah"],
                "Makkah Region": ["Jeddah", "Makkah", "Taif"],
                "Eastern Province": ["Dammam", "Khobar", "Jubail", "Dhahran"],
                "Madinah Region": ["Madinah", "Yanbu", "Badr"],
            },
            "Qatari": {
                "Doha": ["West Bay", "Al Dafna", "The Pearl", "Al Sadd"],
                "Al Rayyan": ["Al Rayyan City", "Abu Hamour", "Al Waab"],
                "Al Wakrah": ["Al Wakrah City", "Mesaieed"],
            },
            "German": {
                "Bavaria": ["Munich", "Nuremberg", "Augsburg", "Regensburg"],
                "North Rhine-Westphalia": [
                    "Cologne",
                    "Düsseldorf",
                    "Dortmund",
                    "Essen",
                ],
                "Baden-Württemberg": [
                    "Stuttgart",
                    "Karlsruhe",
                    "Mannheim",
                    "Freiburg",
                ],
                "Berlin": ["Mitte", "Pankow", "Charlottenburg", "Kreuzberg"],
            },
            "French": {
                "Île-de-France": ["Paris", "Boulogne-Billancourt", "Saint-Denis"],
                "Auvergne-Rhône-Alpes": ["Lyon", "Grenoble", "Saint-Étienne"],
                "Provence-Alpes-Côte d'Azur": [
                    "Marseille",
                    "Nice",
                    "Toulon",
                ],
            },
            "Italian": {
                "Lombardy": ["Milan", "Brescia", "Monza", "Bergamo"],
                "Lazio": ["Rome", "Latina", "Frosinone"],
                "Campania": ["Naples", "Salerno", "Caserta"],
            },
            "Spanish": {
                "Madrid Community": ["Madrid", "Getafe", "Alcalá de Henares"],
                "Catalonia": ["Barcelona", "Girona", "Tarragona"],
                "Andalusia": ["Seville", "Málaga", "Granada", "Cordoba"],
            },
            "Russian": {
                "Moscow Federal City": [
                    "Central District",
                    "Northern District",
                    "Southern District",
                ],
                "Saint Petersburg": [
                    "Centralny",
                    "Admiralteysky",
                    "Vasileostrovsky",
                ],
                "Moscow Oblast": ["Khimki", "Balashikha", "Podolsk"],
            },
            "Brazilian": {
                "São Paulo": ["São Paulo City", "Campinas", "Guarulhos"],
                "Rio de Janeiro": ["Rio de Janeiro City", "Niterói", "Duque de Caxias"],
                "Minas Gerais": ["Belo Horizonte", "Uberlândia", "Juiz de Fora"],
            },
            "South African": {
                "Gauteng": ["Johannesburg", "Pretoria", "Soweto"],
                "Western Cape": ["Cape Town", "Stellenbosch", "George"],
                "KwaZulu-Natal": ["Durban", "Pietermaritzburg", "Richards Bay"],
            },
            "Singaporean": {
                "Central Region": ["Downtown Core", "Orchard", "Bukit Merah"],
                "East Region": ["Tampines", "Bedok", "Changi"],
                "West Region": ["Jurong East", "Clementi", "Choa Chu Kang"],
            },
            "Malaysian": {
                "Kuala Lumpur": ["Bukit Bintang", "Cheras", "Kepong"],
                "Selangor": ["Petaling Jaya", "Shah Alam", "Subang Jaya"],
                "Penang": ["George Town", "Butterworth", "Bayan Lepas"],
                "Johor": ["Johor Bahru", "Iskandar Puteri", "Batu Pahat"],
            },
            "Thai": {
                "Bangkok Metropolis": [
                    "Phra Nakhon",
                    "Sukhumvit",
                    "Bang Rak",
                ],
                "Chiang Mai": ["Mueang Chiang Mai", "Mae Rim", "Hang Dong"],
                "Phuket": ["Mueang Phuket", "Kathu", "Thalang"],
            },
            "South Korean": {
                "Seoul Special City": ["Gangnam-gu", "Jongno-gu", "Mapo-gu"],
                "Gyeonggi-do": ["Suwon", "Seongnam", "Goyang"],
                "Busan Metropolitan City": ["Haeundae-gu", "Busanjin-gu"],
            },
            "Sri Lankan": {
                "Western Province": ["Colombo", "Gampaha", "Kalutara"],
                "Central Province": ["Kandy", "Matale", "Nuwara Eliya"],
                "Southern Province": ["Galle", "Matara", "Hambantota"],
            },
            "Bhutanese": {
                "Thimphu District": ["Thimphu City", "Chango", "Kawang"],
                "Paro District": ["Paro Town", "Dogar", "Lamgong"],
                "Punakha District": ["Punakha Town", "Barp", "Chhubu"],
            },
            "Maldivian": {
                "Kaafu Atoll": ["Malé", "Hulhumalé", "Maafushi"],
                "Addu Atoll": ["Hithadhoo", "Feydhoo", "Maradhoo"],
            },
            "Kuwaiti": {
                "Al Asimah": ["Kuwait City", "Dasman", "Sharq"],
                "Hawalli": ["Hawalli City", "Salmiya", "Jabriya"],
                "Farwaniya": ["Farwaniya City", "Khaitan", "Jleeb Al-Shuyoukh"],
            },
            "Omani": {
                "Muscat Governorate": ["Muscat", "Seeb", "Muttrah", "Bawshar"],
                "Dhofar Governorate": ["Salalah", "Taqah", "Mirbat"],
            },
            "Bahraini": {
                "Capital Governorate": ["Manama", "Juffair", "Seef"],
                "Muharraq Governorate": ["Muharraq City", "Amwaj Islands"],
            },
            "Indonesian": {
                "DKI Jakarta": [
                    "Central Jakarta",
                    "South Jakarta",
                    "West Jakarta",
                ],
                "West Java": ["Bandung", "Bekasi", "Depok", "Bogor"],
                "Bali": ["Denpasar", "Badung", "Gianyar"],
            },
            "Filipino": {
                "Metro Manila": ["Manila", "Quezon City", "Makati", "Taguig"],
                "Cebu": ["Cebu City", "Mandaue", "Lapu-Lapu"],
                "Davao del Sur": ["Davao City", "Digos"],
            },
            "Vietnamese": {
                "Hanoi": ["Hoan Kiem", "Ba Dinh", "Tay Ho"],
                "Ho Chi Minh City": ["District 1", "District 3", "Thu Duc"],
                "Da Nang": ["Hai Chau", "Thanh Khe", "Son Tra"],
            },
            "Dutch": {
                "North Holland": ["Amsterdam", "Haarlem", "Hilversum"],
                "South Holland": ["Rotterdam", "The Hague", "Leiden"],
                "Utrecht": ["Utrecht City", "Amersfoort"],
            },
            "Swiss": {
                "Zurich": ["Zurich City", "Winterthur", "Uster"],
                "Geneva": ["Geneva City", "Vernier", "Lancy"],
                "Vaud": ["Lausanne", "Montreux", "Vevey"],
            },
        }

        # Master mapping: Country Code -> (Nationality, List of ID Proofs)
        self.phone_code_data = {
            "India (+91)": (
                "Indian",
                [
                    "Aadhaar Card",
                    "Voter ID",
                    "PAN Card",
                    "Driving License",
                    "Passport",
                ],
            ),
            "Nepal (+977)": (
                "Nepalese",
                [
                    "Citizenship Card",
                    "National ID Card",
                    "Voter Card",
                    "Driving License",
                    "Passport",
                ],
            ),
            "USA (+1)": (
                "American",
                ["SSN", "State ID", "Driving License", "Passport"],
            ),
            "UK (+44)": (
                "British",
                ["National Insurance No", "Driving License", "Passport"],
            ),
            "BD (+880)": (
                "Bangladeshi",
                [
                    "National ID (NID)",
                    "Birth Certificate",
                    "Driving License",
                    "Passport",
                ],
            ),
            "PK (+92)": (
                "Pakistani",
                ["CNIC", "NICOP", "Driving License", "Passport"],
            ),
            "China (+86)": ("Chinese", ["Resident Identity Card", "Passport"]),
            "Japan (+81)": (
                "Japanese",
                ["My Number Card", "Driver's License", "Passport"],
            ),
            "Australia (+61)": (
                "Australian",
                ["Medicare Card", "Driver's Licence", "Passport"],
            ),
            "Canada (+1)": (
                "Canadian",
                ["Health Card", "Driver's Licence", "Passport"],
            ),
            "UAE (+971)": ("Emirati", ["Emirates ID", "Passport"]),
            "Saudi Arabia (+966)": ("Saudi", ["Iqama", "National ID", "Passport"]),
            "Qatar (+974)": ("Qatari", ["Qatar ID", "Passport"]),
            "Germany (+49)": (
                "German",
                [
                    "Personalausweis (ID Card)",
                    "Führerschein",
                    "Passport",
                ],
            ),
            "France (+33)": (
                "French",
                ["Carte Nationale d'Identité", "Passport"],
            ),
            "Italy (+39)": ("Italian", ["Carta d'Identità", "Passport"]),
            "Spain (+34)": ("Spanish", ["DNI", "NIE", "Passport"]),
            "Russia (+7)": (
                "Russian",
                ["Internal Passport", "Foreign Passport"],
            ),
            "Brazil (+55)": ("Brazilian", ["CPF", "RG Card", "Passport"]),
            "South Africa (+27)": (
                "South African",
                ["Smart ID Card", "Driver's License", "Passport"],
            ),
            "Singapore (+65)": ("Singaporean", ["NRIC / FIN", "Passport"]),
            "Malaysia (+60)": ("Malaysian", ["MyKad", "Passport"]),
            "Thailand (+66)": ("Thai", ["Thai National ID Card", "Passport"]),
            "South Korea (+82)": (
                "South Korean",
                ["Resident Registration Card", "Passport"],
            ),
            "Sri Lanka (+94)": (
                "Sri Lankan",
                ["National ID Card (NIC)", "Passport"],
            ),
            "Bhutan (+975)": (
                "Bhutanese",
                ["Citizenship Identity Card", "Passport"],
            ),
            "Maldives (+960)": (
                "Maldivian",
                ["National Identity Card", "Passport"],
            ),
            "Kuwait (+965)": ("Kuwaiti", ["Civil ID", "Passport"]),
            "Oman (+968)": ("Omani", ["Civil ID Card", "Passport"]),
            "Bahrain (+973)": ("Bahraini", ["CPR Card", "Passport"]),
            "Indonesia (+62)": ("Indonesian", ["KTP Card", "Passport"]),
            "Philippines (+63)": (
                "Filipino",
                ["PhilID / SSS Card", "Passport"],
            ),
            "Vietnam (+84)": (
                "Vietnamese",
                ["Citizen Identification Card", "Passport"],
            ),
            "Netherlands (+31)": ("Dutch", ["Identiteitskaart", "Passport"]),
            "Switzerland (+41)": ("Swiss", ["Identitätskarte", "Passport"]),
        }

        self.all_country_codes = list(self.phone_code_data.keys())

        # ---------------- Title Banner ----------------
        lbl_title = Label(
            self.root,
            text="ADD CUSTOMER DETAILS",
            font=("times new roman", 18, "bold"),
            bg="black",
            fg="gold",
            bd=4,
            relief=RIDGE,
        )
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # Logo Image
        try:
            img2 = Image.open(
                r"C:\Users\sudee\OneDrive\Desktop\DATA SCIENCE\Hotel Management System\photos\logo.jpg"
            )
            img2 = img2.resize((100, 40), Image.Resampling.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img2)
            lblimg2 = Label(
                self.root, image=self.photoimg2, bd=0, relief=RIDGE
            )
            lblimg2.place(x=5, y=5, width=100, height=40)
        except Exception:
            pass

        # ---------------- LabelFrame for Customer Details Form ----------------
        self.labelframeleft = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="Customer Details",
            font=("times new roman", 12, "bold"),
            padx=2,
        )
        self.labelframeleft.place(x=5, y=50, width=425, height=520)

        # Customer Ref
        lbl_cust_ref = Label(
            self.labelframeleft,
            text="Customer Ref",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_cust_ref.grid(row=0, column=0, sticky=W)
        self.entry_ref = Entry(
            self.labelframeleft,
            font=("times new roman", 12, "bold"),
            width=20,
            textvariable=self.var_ref,
            state="readonly",
        )
        self.entry_ref.grid(row=0, column=1)

        # Customer Name
        cname = Label(
            self.labelframeleft,
            text="Customer Name:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        cname.grid(row=1, column=0, sticky=W)
        self.txtcname = Entry(
            self.labelframeleft,
            font=("times new roman", 12, "bold"),
            width=20,
            textvariable=self.var_cust_name,
        )
        self.txtcname.grid(row=1, column=1)

        # Gender
        label_gender = Label(
            self.labelframeleft,
            text="Gender:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        label_gender.grid(row=2, column=0, sticky=W)
        self.combo_gender = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 12, "bold"),
            width=18,
            state="readonly",
        )
        self.combo_gender["values"] = ("Male", "Female", "Other")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=2, column=1)

        # Relation Type Dropdown & Name Entry
        self.combo_relation = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 10, "bold"),
            width=13,
            state="readonly",
        )
        self.combo_relation["values"] = (
            "Father Name",
            "Mother Name",
            "Husband Name",
            "Wife Name",
        )
        self.combo_relation.current(0)
        self.combo_relation.grid(row=3, column=0, sticky=W, padx=2, pady=3)

        self.txt_relation_name = Entry(
            self.labelframeleft, font=("times new roman", 12, "bold"), width=20
        )
        self.txt_relation_name.grid(row=3, column=1)

        # --- Relative Contact with LIVE FILTER SEARCH ---
        lbl_relation_no = Label(
            self.labelframeleft,
            text="Relative Contact:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_relation_no.grid(row=4, column=0, sticky=W)

        relation_frame = Frame(self.labelframeleft)
        relation_frame.grid(row=4, column=1, sticky=W)

        self.combo_rel_country_code = ttk.Combobox(
            relation_frame, font=("times new roman", 9, "bold"), width=11
        )
        self.combo_rel_country_code["values"] = self.all_country_codes
        self.combo_rel_country_code.current(0)
        self.combo_rel_country_code.pack(side=LEFT, padx=(0, 2))

        self.combo_rel_country_code.bind(
            "<KeyRelease>",
            lambda event: self.filter_combobox(
                event, self.combo_rel_country_code
            ),
        )

        self.txt_relation_no = Entry(
            relation_frame, font=("times new roman", 11, "bold"), width=12
        )
        self.txt_relation_no.pack(side=LEFT)
        self.txt_relation_no.bind(
            "<FocusIn>", lambda event: self.select_all_text(self.txt_relation_no)
        )

        # --- Mobile Number with LIVE FILTER SEARCH ---
        lbl_mobile = Label(
            self.labelframeleft,
            text="Mobile No:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_mobile.grid(row=5, column=0, sticky=W)

        mobile_frame = Frame(self.labelframeleft)
        mobile_frame.grid(row=5, column=1, sticky=W)

        self.combo_country_code = ttk.Combobox(
            mobile_frame, font=("times new roman", 9, "bold"), width=11
        )
        self.combo_country_code["values"] = self.all_country_codes
        self.combo_country_code.current(0)
        self.combo_country_code.pack(side=LEFT, padx=(0, 2))

        self.combo_country_code.bind(
            "<KeyRelease>",
            lambda event: self.filter_combobox(event, self.combo_country_code),
        )
        self.combo_country_code.bind(
            "<<ComboboxSelected>>", self.on_country_code_change
        )

        self.txtmobile = Entry(
            mobile_frame, font=("times new roman", 11, "bold"), width=12
        )
        self.txtmobile.pack(side=LEFT)
        self.txtmobile.bind(
            "<FocusIn>", lambda event: self.select_all_text(self.txtmobile)
        )

        # Email
        lbl_email = Label(
            self.labelframeleft,
            text="Email:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_email.grid(row=6, column=0, sticky=W)
        self.txtemail = Entry(
            self.labelframeleft, font=("times new roman", 12, "bold"), width=20
        )
        self.txtemail.grid(row=6, column=1)
        self.txtemail.bind("<KeyRelease>", self.auto_complete_gmail)

        # --- Nationality Dropdown ---
        lbl_nationality = Label(
            self.labelframeleft,
            text="Nationality:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_nationality.grid(row=7, column=0, sticky=W)

        self.combo_nationality = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 12, "bold"),
            width=18,
            state="readonly",
        )
        nationalities = sorted(
            list(set([item[0] for item in self.phone_code_data.values()]))
        )
        self.combo_nationality["values"] = nationalities
        self.combo_nationality.grid(row=7, column=1)

        self.combo_nationality.bind(
            "<<ComboboxSelected>>", self.on_nationality_change
        )

        # --- Dynamic ID Proof Type Dropdown ---
        lbl_id_type = Label(
            self.labelframeleft,
            text="ID Proof Type:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_id_type.grid(row=8, column=0, sticky=W)

        self.combo_id = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 12, "bold"),
            width=18,
            state="readonly",
        )
        self.combo_id.grid(row=8, column=1)

        # ID Number
        lbl_id_number = Label(
            self.labelframeleft,
            text="ID Number:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        lbl_id_number.grid(row=9, column=0, sticky=W)
        self.txtid_number = Entry(
            self.labelframeleft, font=("times new roman", 12, "bold"), width=20
        )
        self.txtid_number.grid(row=9, column=1)

        # --- Dynamic Address System for ALL Countries ---
        self.lbl_province = Label(
            self.labelframeleft,
            text="State/Province:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        self.combo_province = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 10, "bold"),
            width=18,
            state="readonly",
        )
        self.combo_province.bind(
            "<<ComboboxSelected>>", self.on_province_change
        )

        self.lbl_district = Label(
            self.labelframeleft,
            text="District/City:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        self.combo_district = ttk.Combobox(
            self.labelframeleft,
            font=("times new roman", 10, "bold"),
            width=18,
            state="readonly",
        )

        self.lbl_address = Label(
            self.labelframeleft,
            text="Street/Address:",
            font=("times new roman", 12, "bold"),
            padx=2,
            pady=3,
        )
        self.txtaddress = Entry(
            self.labelframeleft, font=("times new roman", 12, "bold"), width=20
        )

        # Initialize defaults
        self.on_country_code_change()

        # ---------------- Buttons Frame ----------------
        btn_frame = Frame(self.labelframeleft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=440, width=412, height=40)

        btn_add = Button(
            btn_frame,
            text="Add",
            font=("times new roman", 11, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.add_data,
        )
        btn_add.grid(row=0, column=0, padx=1, pady=1)

        btn_update = Button(
            btn_frame,
            text="Update",
            font=("times new roman", 11, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.update_data,
        )
        btn_update.grid(row=0, column=1, padx=1, pady=1)

        btn_delete = Button(
            btn_frame,
            text="Delete",
            font=("times new roman", 11, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.delete_data,
        )
        btn_delete.grid(row=0, column=2, padx=1, pady=1)

        btn_reset = Button(
            btn_frame,
            text="Reset",
            font=("times new roman", 11, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.reset_data,
        )
        btn_reset.grid(row=0, column=3, padx=1, pady=1)

        # ---------------- Table Frame for View Details and Search System ----------------
        Table_Frame = LabelFrame(
            self.root,
            bd=2,
            relief=RIDGE,
            text="View Details and Search System",
            font=("times new roman", 12, "bold"),
            padx=2,
        )
        Table_Frame.place(x=435, y=50, width=850, height=520)

        # Search Bar Controls
        lblSearchBy = Label(
            Table_Frame,
            font=("times new roman", 11, "bold"),
            text="Search By:",
            bg="red",
            fg="white",
        )
        lblSearchBy.grid(row=0, column=0, sticky=W, padx=2)

        self.combo_search = ttk.Combobox(
            Table_Frame,
            font=("times new roman", 11, "bold"),
            width=12,
            state="readonly",
        )
        self.combo_search["values"] = ("Mobile", "Ref", "Name")
        self.combo_search.current(0)
        self.combo_search.grid(row=0, column=1, padx=2)

        self.txt_search = Entry(
            Table_Frame, font=("times new roman", 11, "bold"), width=15
        )
        self.txt_search.grid(row=0, column=2, padx=2)

        btnSearch = Button(
            Table_Frame,
            text="Search",
            font=("times new roman", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.search_data,
        )
        btnSearch.grid(row=0, column=3, padx=2)

        btnShowAll = Button(
            Table_Frame,
            text="Show All",
            font=("times new roman", 10, "bold"),
            bg="black",
            fg="gold",
            width=9,
            command=self.show_all,
        )
        btnShowAll.grid(row=0, column=4, padx=2)

        # ---------------- Table Display Area ----------------
        details_table_frame = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table_frame.place(x=0, y=35, width=835, height=450)

        scroll_x = ttk.Scrollbar(details_table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table_frame, orient=VERTICAL)

        self.Cust_Details_Table = ttk.Treeview(
            details_table_frame,
            column=(
                "ref",
                "name",
                "gender",
                "relation",
                "rel_name",
                "rel_mobile",
                "mobile",
                "email",
                "nationality",
                "idproof",
                "idnumber",
                "address",
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set,
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.Cust_Details_Table.xview)
        scroll_y.config(command=self.Cust_Details_Table.yview)

        # Headers Setup
        self.Cust_Details_Table.heading("ref", text="Ref No")
        self.Cust_Details_Table.heading("name", text="Name")
        self.Cust_Details_Table.heading("gender", text="Gender")
        self.Cust_Details_Table.heading("relation", text="Relation")
        self.Cust_Details_Table.heading("rel_name", text="Rel Name")
        self.Cust_Details_Table.heading("rel_mobile", text="Rel Mobile")
        self.Cust_Details_Table.heading("mobile", text="Mobile")
        self.Cust_Details_Table.heading("email", text="Email")
        self.Cust_Details_Table.heading("nationality", text="Nationality")
        self.Cust_Details_Table.heading("idproof", text="ID Proof")
        self.Cust_Details_Table.heading("idnumber", text="ID No")
        self.Cust_Details_Table.heading("address", text="Address")

        self.Cust_Details_Table["show"] = "headings"

        # Column Formatting
        self.Cust_Details_Table.column("ref", width=80)
        self.Cust_Details_Table.column("name", width=100)
        self.Cust_Details_Table.column("gender", width=70)
        self.Cust_Details_Table.column("relation", width=90)
        self.Cust_Details_Table.column("rel_name", width=100)
        self.Cust_Details_Table.column("rel_mobile", width=100)
        self.Cust_Details_Table.column("mobile", width=100)
        self.Cust_Details_Table.column("email", width=120)
        self.Cust_Details_Table.column("nationality", width=90)
        self.Cust_Details_Table.column("idproof", width=100)
        self.Cust_Details_Table.column("idnumber", width=100)
        self.Cust_Details_Table.column("address", width=120)

        self.Cust_Details_Table.pack(fill=BOTH, expand=1)

        self.Cust_Details_Table.bind("<ButtonRelease-1>", self.get_cursor)

        self.show_all()

    # =========================================================
    #                    HELPER FEATURES
    # =========================================================
    def select_all_text(self, widget):
        """Highlight/select all text inside an entry widget when focused."""
        widget.after(10, widget.select_range, 0, END)

    def auto_complete_gmail(self, event):
        """Appends @gmail.com automatically when '@' is typed."""
        if event.char == "@":
            current_text = self.txtemail.get()
            if current_text.count("@") == 1:
                prefix = current_text.split("@")[0]
                self.txtemail.delete(0, END)
                self.txtemail.insert(0, f"{prefix}@gmail.com")

    def toggle_address_view(self, nationality):
        """Dynamically builds address UI based on the selected nationality."""
        if nationality in self.global_address_data:
            provinces = list(self.global_address_data[nationality].keys())
            self.combo_province["values"] = provinces
            self.combo_province.current(0)

            self.lbl_province.grid(row=10, column=0, sticky=W)
            self.combo_province.grid(row=10, column=1, sticky=W)

            self.lbl_district.grid(row=11, column=0, sticky=W)
            self.combo_district.grid(row=11, column=1, sticky=W)

            self.lbl_address.grid(row=12, column=0, sticky=W)
            self.txtaddress.grid(row=12, column=1)

            self.on_province_change()
        else:
            self.lbl_province.grid_forget()
            self.combo_province.grid_forget()
            self.lbl_district.grid_forget()
            self.combo_district.grid_forget()

            self.lbl_address.grid(row=10, column=0, sticky=W)
            self.txtaddress.grid(row=10, column=1)

    def on_province_change(self, event=None):
        """Loads districts/cities when a state/province is selected."""
        selected_nat = self.combo_nationality.get()
        selected_province = self.combo_province.get()

        if (
            selected_nat in self.global_address_data
            and selected_province in self.global_address_data[selected_nat]
        ):
            districts = self.global_address_data[selected_nat][
                selected_province
            ]
            self.combo_district["values"] = districts
            self.combo_district.current(0)

    # =========================================================
    #                   COMBOBOX LOGIC
    # =========================================================
    def filter_combobox(self, event, combobox_widget):
        """Universal search filter: Filters combobox options as you type."""
        if event.keysym in ("Up", "Down", "Return", "Tab", "Escape"):
            if event.keysym in ("Return", "Tab"):
                if combobox_widget == self.combo_country_code:
                    self.on_country_code_change()
            return

        typed_text = combobox_widget.get().lower()

        if typed_text == "":
            combobox_widget["values"] = self.all_country_codes
        else:
            filtered_list = [
                code
                for code in self.all_country_codes
                if typed_text in code.lower()
            ]
            combobox_widget["values"] = filtered_list

        if combobox_widget == self.combo_country_code:
            self.on_country_code_change()

    def on_country_code_change(self, event=None):
        """Updates nationality, ID proof options, and address UI when country code changes."""
        selected_code = self.combo_country_code.get()
        if selected_code in self.phone_code_data:
            nationality, id_list = self.phone_code_data[selected_code]
            self.combo_nationality.set(nationality)
            self.combo_id["values"] = id_list
            self.combo_id.current(0)
            self.toggle_address_view(nationality)

    def on_nationality_change(self, event=None):
        """Syncs country code, ID proof options, and address UI back when nationality is selected."""
        selected_nat = self.combo_nationality.get()
        self.toggle_address_view(selected_nat)

        for code, (nat, id_list) in self.phone_code_data.items():
            if nat == selected_nat:
                self.combo_country_code.set(code)
                self.combo_id["values"] = id_list
                self.combo_id.current(0)
                break

    # =========================================================
    #                   DATABASE HELPERS
    # =========================================================
    def connect_database(self):
        conn = mysql.connector.connect(
            host="localhost",
            username="root",
            password="2333438",  # Replace with your MySQL password
            database="hotel_management",
        )
        return conn

    def ensure_table_exists(self):
        try:
            conn = self.connect_database()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS customer (
                    ref VARCHAR(20) PRIMARY KEY,
                    name VARCHAR(100),
                    gender VARCHAR(20),
                    relation_type VARCHAR(30),
                    relation_name VARCHAR(100),
                    relation_mobile VARCHAR(30),
                    mobile VARCHAR(30),
                    email VARCHAR(100),
                    nationality VARCHAR(50),
                    idproof VARCHAR(50),
                    idnumber VARCHAR(50),
                    address VARCHAR(255)
                )
                """
            )
            conn.commit()
            conn.close()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Could not verify/create table.\n{e}"
            )

    # =========================================================
    #                   FORM <-> FIELDS
    # =========================================================
    def get_form_values(self):
        selected_nat = self.combo_nationality.get()

        if selected_nat in self.global_address_data:
            full_address = f"{self.combo_district.get()}, {self.combo_province.get()} - {self.txtaddress.get()}".strip(
                " -,"
            )
        else:
            full_address = self.txtaddress.get()

        return {
            "ref": self.var_ref.get(),
            "name": self.txtcname.get(),
            "gender": self.combo_gender.get(),
            "relation_type": self.combo_relation.get(),
            "relation_name": self.txt_relation_name.get(),
            "relation_mobile": f"{self.combo_rel_country_code.get()} {self.txt_relation_no.get()}".strip(),
            "mobile": f"{self.combo_country_code.get()} {self.txtmobile.get()}".strip(),
            "email": self.txtemail.get(),
            "nationality": selected_nat,
            "idproof": self.combo_id.get(),
            "idnumber": self.txtid_number.get(),
            "address": full_address,
        }

    def get_cursor(self, event=None):
        try:
            selected_row = self.Cust_Details_Table.focus()
            data = self.Cust_Details_Table.item(selected_row)
            row = data.get("values")
            if not row:
                return

            self.var_ref.set(row[0])
            self.txtcname.delete(0, END)
            self.txtcname.insert(0, row[1])
            self.combo_gender.set(row[2])
            self.combo_relation.set(row[3])
            self.txt_relation_name.delete(0, END)
            self.txt_relation_name.insert(0, row[4])

            rel_mobile_parts = str(row[5]).split(" ", 1)
            if len(rel_mobile_parts) == 2:
                self.combo_rel_country_code.set(f"{rel_mobile_parts[0]}")
                self.txt_relation_no.delete(0, END)
                self.txt_relation_no.insert(0, rel_mobile_parts[1])

            mobile_parts = str(row[6]).split(" ", 1)
            if len(mobile_parts) == 2:
                self.combo_country_code.set(mobile_parts[0])
                self.txtmobile.delete(0, END)
                self.txtmobile.insert(0, mobile_parts[1])

            self.txtemail.delete(0, END)
            self.txtemail.insert(0, row[7])
            self.combo_nationality.set(row[8])
            self.on_nationality_change()

            self.combo_id.set(row[9])
            self.txtid_number.delete(0, END)
            self.txtid_number.insert(0, row[10])

            self.txtaddress.delete(0, END)
            self.txtaddress.insert(0, row[11])
        except Exception as e:
            messagebox.showerror("Error", f"Could not load selected row.\n{e}")

    # =========================================================
    #                   CRUD OPERATIONS
    # =========================================================
    def add_data(self):
        values = self.get_form_values()

        mob_num = self.txtmobile.get().strip()
        rel_num = self.txt_relation_no.get().strip()

        if values["name"] == "" or mob_num == "":
            messagebox.showerror(
                "Error", "Customer Name and Mobile Number are required."
            )
            return

        if rel_num != "" and mob_num == rel_num:
            messagebox.showerror(
                "Error",
                "Customer Mobile Number and Relative Contact Number cannot be identical.",
            )
            return

        try:
            conn = self.connect_database()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM customer WHERE mobile = %s OR relation_mobile = %s",
                (values["mobile"], values["mobile"]),
            )
            if cur.fetchone():
                messagebox.showerror(
                    "Duplicate Entry",
                    "This mobile number is already registered in the database.",
                )
                conn.close()
                return

            cur.execute(
                """
                INSERT INTO customer
                (ref, name, gender, relation_type, relation_name, relation_mobile,
                 mobile, email, nationality, idproof, idnumber, address)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    values["ref"],
                    values["name"],
                    values["gender"],
                    values["relation_type"],
                    values["relation_name"],
                    values["relation_mobile"],
                    values["mobile"],
                    values["email"],
                    values["nationality"],
                    values["idproof"],
                    values["idnumber"],
                    values["address"],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer added successfully.")
            self.reset_data()
            self.show_all()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Could not add customer.\n{e}"
            )

    def update_data(self):
        values = self.get_form_values()

        if values["ref"] == "":
            messagebox.showerror(
                "Error", "Select a customer from the table to update."
            )
            return

        mob_num = self.txtmobile.get().strip()
        rel_num = self.txt_relation_no.get().strip()

        if rel_num != "" and mob_num == rel_num:
            messagebox.showerror(
                "Error",
                "Customer Mobile Number and Relative Contact Number cannot be identical.",
            )
            return

        try:
            conn = self.connect_database()
            cur = conn.cursor()
            cur.execute(
                """
                UPDATE customer SET
                    name=%s, gender=%s, relation_type=%s, relation_name=%s,
                    relation_mobile=%s, mobile=%s, email=%s, nationality=%s,
                    idproof=%s, idnumber=%s, address=%s
                WHERE ref=%s
                """,
                (
                    values["name"],
                    values["gender"],
                    values["relation_type"],
                    values["relation_name"],
                    values["relation_mobile"],
                    values["mobile"],
                    values["email"],
                    values["nationality"],
                    values["idproof"],
                    values["idnumber"],
                    values["address"],
                    values["ref"],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer updated successfully.")
            self.reset_data()
            self.show_all()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Could not update customer.\n{e}"
            )

    def delete_data(self):
        ref = self.var_ref.get()
        if ref == "":
            messagebox.showerror(
                "Error", "Select a customer from the table to delete."
            )
            return

        if not messagebox.askyesno(
            "Confirm", f"Delete customer with Ref {ref}?"
        ):
            return

        try:
            conn = self.connect_database()
            cur = conn.cursor()
            cur.execute("DELETE FROM customer WHERE ref=%s", (ref,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Customer deleted successfully.")
            self.reset_data()
            self.show_all()
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Could not delete customer.\n{e}"
            )

    def reset_data(self):
        self.var_ref.set(str(random.randint(1000, 9999)))
        self.txtcname.delete(0, END)
        self.combo_gender.current(0)
        self.combo_relation.current(0)
        self.txt_relation_name.delete(0, END)
        self.combo_rel_country_code.set(self.all_country_codes[0])
        self.txt_relation_no.delete(0, END)
        self.combo_country_code.set(self.all_country_codes[0])
        self.txtmobile.delete(0, END)
        self.txtemail.delete(0, END)
        self.on_country_code_change()
        self.txtid_number.delete(0, END)
        self.txtaddress.delete(0, END)

    def show_all(self):
        try:
            conn = self.connect_database()
            cur = conn.cursor()
            cur.execute("SELECT * FROM customer")
            rows = cur.fetchall()
            conn.close()

            self.Cust_Details_Table.delete(
                *self.Cust_Details_Table.get_children()
            )
            for row in rows:
                self.Cust_Details_Table.insert("", END, values=row)
        except Exception as e:
            messagebox.showerror(
                "Database Error", f"Could not load customers.\n{e}"
            )

    def search_data(self):
        search_by = self.combo_search.get()
        search_value = self.txt_search.get().strip()

        if search_value == "":
            messagebox.showerror("Error", "Enter a value to search for.")
            return

        column_map = {"Mobile": "mobile", "Ref": "ref", "Name": "name"}
        column = column_map.get(search_by, "name")

        try:
            conn = self.connect_database()
            cur = conn.cursor()
            cur.execute(
                f"SELECT * FROM customer WHERE {column} LIKE %s",
                (f"%{search_value}%",),
            )
            rows = cur.fetchall()
            conn.close()

            self.Cust_Details_Table.delete(
                *self.Cust_Details_Table.get_children()
            )
            for row in rows:
                self.Cust_Details_Table.insert("", END, values=row)

            if not rows:
                messagebox.showinfo(
                    "No Results", "No matching customer records found."
                )
        except Exception as e:
            messagebox.showerror("Database Error", f"Search failed.\n{e}")


if __name__ == "__main__":
    root = Tk()
    obj = Cus_Win(root)
    obj.ensure_table_exists()
    root.mainloop()