import pandas as pd
#from pandas_datareader import data
#from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

def bereken_uitgave_per_kostenpost(kostenpost):
    mask = bankafschrift_af["Naam / Omschrijving"].str.contains(kostenpost)
    bankafschrift_af_met_mask = bankafschrift_af[mask]
    return bankafschrift_af_met_mask["Bedrag (EUR)"].sum()


# Dit nog splitsen in 2 functies
def bereken_totaal(list):
    # Hier een dict aanmaken en ieder item in list is key en de sum van kostenpost wordt de value
    vr = {}
    for n in list:
        vr[n] = bereken_uitgave_per_kostenpost(n)

    # Hier loopen door de dict values en bij elkaar optellen
    n = 0
    for x in vr.values():
        n = n + x
    return n


### Importeren van CSV
# De code voor importeren
afschriften = pd.read_csv("bankafschrift_test.csv")
afschriften["Bedrag (EUR)"] = afschriften["Bedrag (EUR)"].str.replace(",", ".").astype("float")
# apart dataframe voor bijschrijvingen
mask_bij = afschriften["Af Bij"] == "Bij"
bankafschrift_bij = afschriften[mask_bij]
# apart dataframe voor afschrijvingen
mask_af = afschriften["Af Bij"] == "Af"
bankafschrift_af = afschriften[mask_af]

### SPAARREKENING BEREKENINGEN
# nog de .sum() aan variabele toekennen
# Totaal uitgave zonder afschrijvingen naar spaarrekening
bankafschrift_af_zonder_spaar_mask = ~bankafschrift_af["Mededelingen"].str.contains("Naar Oranje spaarrekening")
bankafschrift_af_zonder_naar_spaar = bankafschrift_af[bankafschrift_af_zonder_spaar_mask]
bankafschrift_af_zonder_naar_spaar["Bedrag (EUR)"].sum()
# Hoeveel opgenomen van spaarrekening?
bankafschrift_bij_van_spaar_mask = bankafschrift_bij["Mededelingen"].str.contains("Van Oranje spaarrekening")
bankafschrift_bij_van_spaar = bankafschrift_bij[bankafschrift_bij_van_spaar_mask]
bankafschrift_bij_van_spaar["Bedrag (EUR)"].sum()
# Hoeveel bijgeschreven naar spaarrekening?
bankafschrift_af_naar_spaar_mask = bankafschrift_af["Mededelingen"].str.contains("Naar Oranje spaarrekening")
bankafschrift_af_naar_spaar = bankafschrift_af[bankafschrift_af_naar_spaar_mask]
bankafschrift_af_naar_spaar["Bedrag (EUR)"].sum()
# Hoeveel gespaard?
bankafschrift_af_naar_spaar["Bedrag (EUR)"].sum() - bankafschrift_bij_van_spaar["Bedrag (EUR)"].sum()

###Hoeveel aan boodschappen totaal uitgegeven?
boodschappen_list = ["ALBERT", "DIRK", "Hoogvliet", "Versmarkt", "Bakker", "Jumbo"]
shoppen_list = ["Action", "HEMA", "Xenos", "KULK", "Gall", "Primera", "SoLow", "MAYFLOWER"]
kleding_list = ["PRIMARK", "Wehkamp", "KiK", "VANHAREN", "HM", "ZARA"]
eten_bestellen_list = ["Uber"]
verzorging_list = ["ETOS", "Trekpleister"]
eten_onderweg_list = ["MEERN", "Dunkin", "Vermolen", "Doner", "AH"]
geld_opgenomen_list = ["Geldmaat"]
uit_eten_list = ["EINSTEIN", "GRANDCAFE", "SLOT", "Hooiberg", 'CUBANITA', "ELLINIKO", "SumUp", "Studiozuidwest"]
baby_list = ["POORT", "PRENATAL", "BabyDump"]
betaalverzoeken_list = ["Betaalverzoek"]
zwangerschap_list = ["Zijl"]
dagje_uit_list = ["Madurodam"]
# Dit klopt alleen maar op dit dataframe en deze rekening, onder overig plaatsen?
af_naar_eigen_rekening_list = ["Land"]
kosten_ing_list = ["OranjePakket", "tweede rekeninghouder"]

boodschappen_totaal = bereken_totaal(boodschappen_list)
shoppen_totaal = bereken_totaal(shoppen_list)
eten_bestellen_totaal = bereken_totaal(eten_bestellen_list)
verzorging_totaal = bereken_totaal(verzorging_list)
eten_onderweg_totaal = bereken_totaal(eten_onderweg_list)
# bij kleding moet tinka er eigenlijk nog van af, of ga ik dit anders verwerken?
# Tinka moet eigenlijk anders verwerkt worden anders verdwijnt er teveel geld bij overig.
kleding_totaal = bereken_totaal(kleding_list)
geld_opgenomen_totaal = bereken_totaal(geld_opgenomen_list)
uit_eten_totaal = bereken_totaal(uit_eten_list)
baby_totaal = bereken_totaal(baby_list)
betaalverzoeken_totaal = bereken_totaal(betaalverzoeken_list)
zwangerschap_totaal = bereken_totaal(zwangerschap_list)
dagje_uit_totaal = bereken_totaal(dagje_uit_list)
# Dit klopt alleen maar op dit dataframe (ook uit totaal halen bij andere)
af_naar_eigen_rekening_totaal = bereken_totaal(af_naar_eigen_rekening_list) - bankafschrift_af_naar_spaar[
    "Bedrag (EUR)"].sum()
kosten_ing_totaal = (bereken_totaal(kosten_ing_list))

uitgaven_totaal = boodschappen_totaal + shoppen_totaal + kleding_totaal + verzorging_totaal + geld_opgenomen_totaal + uit_eten_totaal + baby_totaal + betaalverzoeken_totaal + zwangerschap_totaal + eten_onderweg_totaal + dagje_uit_totaal + af_naar_eigen_rekening_totaal + kosten_ing_totaal
uitgaven_overig = bankafschrift_af_zonder_naar_spaar["Bedrag (EUR)"].sum() - uitgaven_totaal
#  print(uitgaven_overig)

# MATPLOTLIB TEST
# Define what we want to graph
x = ["Boodschappen", "shoppen", "kleding", "verzorging", "geldautomaat", "uit eten", "bebe", "betaalverzoeken", "zwanger", "onderweg eten", "dagje uit", "eigen rekening", "ing kosten", "eten bestellen"]
y = [boodschappen_totaal, shoppen_totaal, kleding_totaal, verzorging_totaal, geld_opgenomen_totaal, uit_eten_totaal, baby_totaal, betaalverzoeken_totaal, zwangerschap_totaal, eten_onderweg_totaal, dagje_uit_totaal, af_naar_eigen_rekening_totaal, kosten_ing_totaal, eten_bestellen_totaal]

plt.plot(x, y)
#plt.bar(x, y)
#plt.pie(y, labels=x)
plt.ylabel("Bedrag in euro's")
plt.xlabel("Kostenpost")
plt.title("Uitgaven per kostenpost")


class Matty(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        box = self.ids.box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def save_it(self):
        name = self.ids.namer.text
        if name:
            plt.savefig(name)


#  WORDT NU NIET GEBRUIKT
class MyGrid(Widget):
    inkomsten = ObjectProperty(None)
    uitgaven = ObjectProperty(None)
    #  print(uitgaven_totaal)

    def btn(self):
        #  print("Name:", self.name.text, "email:", self.email.text)
        self.inkomsten.text = str(bankafschrift_bij["Bedrag (EUR)"].sum())
        self.uitgaven.text = str(uitgaven_totaal)


class ExcelFinancienApp(MDApp):
    def build(self):
        #  return MyGrid()

        #  self.theme_cls.theme_style = "Dark"
        #  self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file('matplotlibtest.kv')
        return Matty()


if __name__ == "__main__":
    ExcelFinancienApp().run()
