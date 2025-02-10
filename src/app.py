# Import required libraries
import customtkinter
from customtkinter import *
import json
import shutil

# Initialize the main window
root = CTk()
root.title("AC Paintjob Packer")
root.iconbitmap("../assets/themes/acpp.ico")
customtkinter.set_default_color_theme("../assets/themes/purple.json")

# Create the main tab view
tabview = CTkTabview(root)
tabview.pack(pady=20, padx=20)

# Add tabs for different sections of the application
welcomeTab = tabview.add("Welcome")
carChoiceTab = tabview.add("Choose Car")
jsonEditTab = tabview.add("Edit JSON")
exportTab = tabview.add("Export")

# Create and configure the welcome tab
welcomeFrame = CTkFrame(welcomeTab)
welcomeFrame.pack(fill=BOTH, pady=0, padx=0)

welcomeHeading = CTkLabel(welcomeFrame, text="Welcome to the AC Paintjob Packer!", font=('Arial Bold', 36))
welcomeHeading.pack(pady=20, padx=20)

welcomeText = CTkLabel(welcomeFrame, text="Welcome to AC Paintjob Packer,\na simple program that will make making\npaintjobs easier for you! Just fill in the information\nneeded and you'll have a ready-to-edit skin structure!", font=('Roboto', 24))
welcomeText.pack(pady=10, padx=10)

# Create frames for each tab
carChoiceFrame = CTkFrame(carChoiceTab)
carChoiceFrame.pack(fill=BOTH, pady=0, padx=0)

jsonEditFrame = CTkFrame(jsonEditTab)
jsonEditFrame.pack(fill=BOTH, pady=10, padx=10)

carChoiceFrameList = CTkScrollableFrame(carChoiceFrame)
carChoiceFrameList.pack(fill=BOTH, pady=10, padx=10)

exportTabFrame = CTkFrame(exportTab)
exportTabFrame.pack(fill=BOTH, pady=10, padx=10)

# Dictionary mapping car IDs to their display names
cars = {
  "bmw_m3_e3O": "BMW M3 E3O",
  "ferrari_f40": "Ferrari F40",
  "ks_abarth_595ss": "Fiat Abarth 595SS",
  "ks_audi_a1s1": "Audi S1",
  "ks_audi_r8_lms": "Audi R8 LMS Ultra",
  "ks_audi_r8_lms_2016": "Audi R8 LMS 2016 GT3",
  "ks_mazda_miata": "Mazda Miata MX5 NA",
  "ks_mazda_miata_mx5_cup": "Mazda Miata MX5 Cup"
}

# Dictionary mapping car IDs to their template file paths
carsTemplates = {
  "bmw_m3_e3O": "../assets/templates/bmw_m3_e30/Carpaint_D_white.dds",
  "ferrari_f40": "../assets/templates/ferrari_f40/Carpaint_skin2.dds",
  "ks_abarth_595ss": "../assets/templates/ks_abarth_595ss/Carpaint_Skin_00.dds",
  "ks_audi_a1s1": "../assets/templates/ks_audi_a1s1/Skin_00.dds",
  "ks_audi_r8_lms": "../assets/templates/ks_audi_r8_lms/Skin_00.dds",
  "ks_audi_r8_lms_2016": "../assets/templates/ks_audi_r8_lms_2016/EXT_skin00.dds",
  "ks_mazda_miata": "../assets/templates/ks_mazda_miata/Skin_00.dds",
  "ks_mazda_miata_mx5_cup": "../assets/templates/ks_mazda_mx5_cup/Skin_00.dds"  
}

# Variable to store the selected car
carChoice = StringVar()

# Create radio buttons for each car
for car in cars:
  carRadioButton = CTkRadioButton(carChoiceFrameList, text=cars[car], value=car, variable=carChoice)
  carRadioButton.pack(pady=5, padx=5, anchor=W)

# Lists containing UI element labels and their internal names
uiSkinVarNames = ["Skin Name", "Driver Name", "Country", "Team", "Number", "Skin Name Internal (no spaces allowed)"]
uiSkinVarNamesInt = ["skinname", "drivername", "country", "team", "number"]

# Create entry fields for skin customization
skinNameUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[0])
skinNameUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

skinNameIntUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[5])
skinNameIntUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

driverNameUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[1])
driverNameUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

countryUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[2])
countryUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

teamUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[3])
teamUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

numberUiSkinEntry = CTkEntry(jsonEditFrame, placeholder_text=uiSkinVarNames[4])
numberUiSkinEntry.pack(pady=5, padx=10, fill=X, expand=True)

# Function to create and save the JSON data file
def make_json_data():
  uiSkinDataList = [skinNameUiSkinEntry.get(), driverNameUiSkinEntry.get(), countryUiSkinEntry.get(), teamUiSkinEntry.get(), numberUiSkinEntry.get(), skinNameIntUiSkinEntry.get()]
  uiSkinJson = json.dumps({
    "skinname": uiSkinDataList[0],
    "drivername": uiSkinDataList[1],
    "country": uiSkinDataList[2],
    "team": uiSkinDataList[3],
    "number": uiSkinDataList[4]
    })
  
  jsonFile = open("../assets/ui_skin.json", "w")
  jsonFile.write(uiSkinJson)
  jsonFile.close()
  
  return uiSkinDataList

# Function to save the skin files to a selected directory
def save_to():
  uiSkinDataList = [skinNameUiSkinEntry.get(), driverNameUiSkinEntry.get(), countryUiSkinEntry.get(), teamUiSkinEntry.get(), numberUiSkinEntry.get(), skinNameIntUiSkinEntry.get()]
  asked_dir = filedialog.askdirectory()
  carChoiceGet = carChoice.get()
  dir = f"{asked_dir}/AC_Packer_Output/content/cars/{carChoiceGet}/skins/{uiSkinDataList[-1]}"
  if not os.path.exists(dir):
    os.makedirs(dir)
  else:
    print(f"{dir} exists")
  if carChoiceGet in carsTemplates:
    make_json_data()
    filesToCopy = [carsTemplates[carChoiceGet], "../assets/ac_crew.dds", "../assets/livery.png", "../assets/preview.jpg", "../assets/ui_skin.json"]
    for file in filesToCopy:
      shutil.copy(file, os.path.join(dir, os.path.basename(file)))
    
# Function to export the mod and display completion message
def export_mod():
  save_to()
  tutorialLabel = CTkLabel(exportTabFrame, text=f"Great! Your skin files are in {dir},\n to edit them just open up your\n file explorer and go to {dir}, and start editing AC_Crew.dds,\nlivery.png and the skin file, next go back to\n'AC_Packer_Output' and compress the 'content' folder\n drag and drop into CM, install, in CM go to Content > Cars > the car your skin is for\nand click on update previews, enjoy!")
  tutorialLabel.pack

# Create export button
exportButton = CTkButton(exportTabFrame, text="Save To", command=export_mod)
exportButton.pack(padx=20, pady=20)

# Start the main application loop
root.mainloop()