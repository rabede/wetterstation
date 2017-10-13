time = "1h"       #Mögliche Werte d für Tag und h für Stunde, y ghet nicht!

REQUEST_PARAMETERS = [
    {
        "value":"r_no",  #Widerstand NO-Sensor
        "time": time  
    },
    {
        "value":"r_co",  #Widerstand CO-Sensor
        "time": time
    },
    {
        "value":"t_cpu", #CPU-Temperatur
        "time": time
    }                      
]

OK_STATIONEN = [
    {
        "Station":"F686E2",
        "Straße": "Leverkusen, Gustav-Heinemann-Straße"
'''        
    },
    {
        "Station":"F68735",
        "Straße": "Piccoloministraße Holweide"
    },       
    {
        "Station":"F686D9",
        "Straße": "Widdersdorf, Blaugasse"
    },
    {
        "Station":"F686D6",
        "Straße": "Dellbrück, Krokusweg"
    },
    {
        "Station":"F686D0",
        "Straße": "Nippes, Usambarastraße"
    },
    {
        "Station":"F686A1",
        "Straße": "Mülheim, Berliner Straße"
    },
    {
        "Station":"F68654",
        "Straße": "Horrem"
    },
    {
        "Station":"CA28DB",
        "Straße": "Eigelstein, Lübeckerstraße"
    },
    {
        "Station":"CA2898",
        "Straße": "Sülz, Mommsenstraße"
'''        
    }
]

LANUV_STATIONEN = [
    {
        "Ort": "Leverkusen",
        "Straße": "Gustav-Heinemann-Straße",
        "Station": "VLEG",
        "PLZ": "51377",
        "Standort": "Verkehr",
        "csv": "True"
    },
    {
        "Ort": "Leverkusen-Manfort",
        "Straße": "",
        "Station": "LEV2",
        "PLZ": "51373",
        "Standort": "Hintergrund",
        "csv": "True"
'''	
    };
    {
		"Ort": "Köln",
		"Straße": "Bergisch-Gladbacher Straße",
		"Station": "KOBG",
		"PLZ": "51067",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Clevischer Ring",
		"Station": "VKCL",
		"PLZ": "51065",
		"Standort": "Verkehr",
		"csv": "True"
	},
	{
		"Ort": "Köln",
		"Straße": "Dellbücker Hauptstraße",
		"Station": "KODH",
		"PLZ": "51069",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Hauptstraße",
		"Station": "KOHA",
		"PLZ": "51143",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Justinianstraße",
		"Station": "KJUS",
		"PLZ": "50679",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Lindweilerweg 144",
		"Station": "KLLW",
		"PLZ": "50739",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Luxemburger Straße",
		"Station": "VKLS",
		"PLZ": "50939",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Neumarkt",
		"Station": "KNEU",
		"PLZ": "50667",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln",
		"Straße": "Turiner Straße",
		"Station": "VKTU",
		"PLZ": "50668",
		"Standort": "Verkehr",
		"csv": "True"
	},
	{
		"Ort": "Köln-Chorweiler",
		"Straße": "",
		"Station": "CHOR",
		"PLZ": "50765",
		"Standort": "Hintergrund",
		"csv": "True"
	},
	{
		"Ort": "Köln-Godorf",
		"Straße": "",
		"Station": "KGOD",
		"PLZ": "50997",
		"Standort": "Industrie",
		"csv": "False"
	},
	{
		"Ort": "Köln-Meschenich",
		"Straße": "Brühler Landstraße",
		"Station": "KMEB",
		"PLZ": "50997",
		"Standort": "Verkehr",
		"csv": "False"
	},
	{
		"Ort": "Köln-Rodenkirchen",
		"Straße": "",
		"Station": "RODE",
		"PLZ": "50996",
		"Standort": "Hintergrund",
		"csv": "True"
	},
	{
		"Ort": "Köln-Weiden",
		"Straße": "",
		"Station": "KWEI",
		"PLZ": "50858",
		"Standort": "Verkehr",
		"csv": "False"
'''		
	}
]
