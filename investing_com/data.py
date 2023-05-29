import investpy as inv

tickers = {
    "Large Cap Growth" : "DJUSGL",
    "Large Cap Value" : "DJUSVL",
    "Small Cap Growth" : "DJUSGS",
    "Small Cap Value" : "DJUSVS",
    "Mid Cap" : "DJUSM",
    "International Stock" : "MIEA00000PUS",
    "Emerging Mkt Stock" : "MSCI",
    "Intermediate Gov Bonds" : "GVI",
    "Long Gov Bonds" : "ILTB",
    "Corporate Bonds" : "DJCBT",
    "High Yield Bonds" : "MUT",
    "Municipal Bonds" : "OMRXMUNI",
    "Foreign Bonds" : "GLAG",
    "Emerging Mkt Debt" : "EMB",
    "Real Estate" : "DJUSRE",
    "V.C." : "JVENC",
    "Commodities" : "DJCI",
    "Cash" : "BIL"
}

#print(inv.get_index_countries())
#inv.get_indices(country="united states").to_csv("indeces.csv")
print(inv.get_index_historical_data(index="DJ Large-Cap Growth",country="united states",from_date="01/01/2023",to_date="01/03/2023"))
